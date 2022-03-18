from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_auth import serializers
import stripe
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import action
from stripe.error import CardError
from django.utils.translation import ugettext_lazy as _
import sendgrid
import os

stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY if settings.STRIPE_LIVE_MODE else settings.STRIPE_SECRET_KEY
# stripe.api_key = "sk_test_9lLAbsWDtg9r5B17jYWGaJsb002b4FqMAZ"

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    AccountSerializer,
    WishSerializer,
    AlertSerializer,
    CourseSerializer,
    SettingSerializer
)
from home.models import Alert, Course, Wish, Setting
from users.models import User

class SignupViewSet(ModelViewSet):
    serializer_class = SignupSerializer
    http_method_names = ["post"]


class LoginViewSet(ViewSet):
    """Based on rest_framework.authtoken.views.ObtainAuthToken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UserSerializer(user)

        setting = Setting.objects.filter(user = user).first()
        if setting and setting.is_deactivated:
            raise serializers.ValidationError(
                _("Account is deactivated"))

        return Response({"token": token.key, "user": user_serializer.data})

class AccountViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = User.objects.all()
    http_method_names = ['patch']

    def partial_update(self, request, *args, **kwargs):
        user = self.queryset.get(pk=self.request.user.pk)
        if user.username != request.user.username:
            raise serializers.ValidationError(
                _("Cannot update other user's data"))
        return super().partial_update(request, self.request.user.pk)

class WishViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wish.objects.all()
    serializer_class = WishSerializer

    # def create(self, request, *args, **kwargs):
    #     try:
    #         if not request.data._mutable:
    #             request.data._mutable = True
    #     except:
    #         pass
    #     request.data['user'] = request.user.pk
    #     response = super().create(request, *args, **kwargs)
    #     return response

    def create(self, request, *args, **kwargs):
        resp = super().create(request, args, kwargs)
        if resp.status_code == 201:
            wish_id = resp.data['id']
            wish = Wish.objects.get(id=wish_id)
            if wish.is_before_selected:
                course = Course.objects.filter(tee_datetime__lte=wish.from_date).order_by('-id').first()
            else:
                course = Course.objects.filter(tee_datetime__gte=wish.from_date, tee_datetime__lte=wish.to_date).order_by('-id').first()

            if course:
                # send push notification
                # if notification: then insert
                Alert.objects.create(user=self.request.user, wish=wish, course=course, is_read=False)

                # SendGrid Integration
                sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
                data = {
                    "personalizations": [
                        {
                            "to": [
                                {
                                    "email": self.request.user.email
                                }
                            ],
                            "subject": "Golf Course Notification"
                        }
                    ],
                    "from": {
                        "email": settings.EMAIL_HOST_USER
                    },
                    "content": [
                        {
                            "type": "An alert has been added in your application against your wish. Please check your application.",
                            "value": "and easy to do anywhere, even with Python"
                        }
                    ]
                }
                response = sg.client.mail.send.post(request_body=data)
                print(response.status_code)
                print(response.body)
                print(response.headers)

        return resp

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlertViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AlertSerializer
    queryset = Alert.objects.all()


class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class SettingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SettingSerializer
    queryset = Setting.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        try:
            user = self.request.user
            email = user.email
            payment_method_id = request.data['payment_method_id']
            customer_data = stripe.Customer.list(email=email).data
            # if the array is empty it means the email has not been used yet
            if len(customer_data) == 0:
                # creating customer
                customer = stripe.Customer.create(email=email, payment_method=payment_method_id,
                                                  invoice_settings={'default_payment_method': payment_method_id})
            else:
                customer = customer_data[0]

            # Create PaymentIntent — charge the customer with a one-time fee
            stripe.PaymentIntent.create(
                customer=customer,
                payment_method=payment_method_id,
                currency='usd',  # you can provide any currency you want
                amount=6.98,
                confirm=True
            )

            stripe.Subscription.create(
                customer=customer,
                items=[{
                    'price': 'price_1JSoiFGRbb2vDACC2Fa23PAQ'  # here paste your price id
                }]
            )
            user.is_subscribe = True
            user.subscription_using_payment = True
            user.subscription_using_code = False
            user.save()
            return Response(status=status.HTTP_201_CREATED)
        except CardError as e:
            return Response(data=e.error, status=e.http_status)

    def create_customer_id(self, request):
        customer = stripe.Customer.create(
            description="Customer for {}".format(request.user.email),
            email=request.user.email
        )
        request.user.stripe_customer_id = customer.id
        request.user.save()

    @action(detail=False, methods=['get'])
    def get_customer_id(self, request):
        if not request.user.stripe_customer_id:
            customer = stripe.Customer.create(
                description="Customer for {}".format(request.user.email),
                email=request.user.email
            )
            request.user.stripe_customer_id = customer.id
            request.user.save()
        return Response({"customer_id": request.user.stripe_customer_id})

    @action(detail=False, methods=['get'])
    def get_cards(self, request):
        if request.user.stripe_customer_id:
            cards = stripe.Customer.list_sources(
                request.user.stripe_customer_id,
                object="card",
            )
            customer = stripe.Customer.retrieve(request.user.stripe_customer_id)
            # return Response(cards)
            return Response({
                "cards": cards.data,
                "default_card": customer.default_source
            })
        return Response("User not a customer", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_card(self, request):
        try:
            if not request.user.stripe_customer_id:
                self.create_customer_id(request)
            if request.user.stripe_customer_id:
                card = stripe.Customer.create_source(
                    request.user.stripe_customer_id,
                    source=request.data['card_token'],
                )
                default_card = request.data.get('default_card', False)
                if default_card:
                    stripe.Customer.modify(request.user.stripe_customer_id,
                                           default_source=card.id)

                return Response(card)
        # return Response("User not a customer", status=status.HTTP_400_BAD_REQUEST)
        except CardError as e:
            return Response(data=e.error, status=e.http_status)
        # except Exception as e:
        #     return Response(data={
        #         "error" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['post'])
    def set_default_card(self, request):
        try:
            if request.user.stripe_customer_id:
                # default_card = request.data.get('default_card', False)
                # if default_card:
                stripe.Customer.modify(request.user.stripe_customer_id, source=request.data['card_token'])
                return Response()
            return Response("User not a customer", status=status.HTTP_400_BAD_REQUEST)
        except CardError as e:
            return Response(data=e.error, status=e.http_status)

    @action(detail=False, methods=['post'])
    def update_card(self, request):
        data = {}
        if 'address_city' in request.data:
            data['address_city'] = request.data['address_city']
        if 'address_country' in request.data:
            data['address_country'] = request.data['address_country']
        if 'address_line1' in request.data:
            data['address_line1'] = request.data['address_line1']
        if 'address_line2' in request.data:
            data['address_line2'] = request.data['address_line2']
        if 'address_state' in request.data:
            data['address_state'] = request.data['address_state']
        if 'address_zip' in request.data:
            data['address_zip'] = request.data['address_zip']
        if 'exp_month' in request.data:
            data['exp_month'] = request.data['exp_month']
        if 'exp_year' in request.data:
            data['exp_year'] = request.data['exp_year']
        if 'name' in request.data:
            data['name'] = request.data['name']
        if request.user.stripe_customer_id:
            card = stripe.Customer.modify_source(
                request.user.stripe_customer_id,
                request.data['card_id'],
                **data
            )
            default_card = request.data.get('default_card', False)
            if default_card:
                stripe.Customer.modify(request.user.stripe_customer_id,
                                       default_source=request.data['card_id'])
            return Response(card)
        return Response("User not a customer", status=status.HTTP_400_BAD_REQUEST)

        @action(detail=False, methods=['post'])
        def delete_card(self, request):
            if request.user.stripe_customer_id:
                response = stripe.Customer.delete_source(
                    request.user.stripe_customer_id,
                    request.data['card_id']
                )
                return Response(response)
            return Response("User not a customer", status=status.HTTP_400_BAD_REQUEST)

# TODO: save wish-> save wish+ get course+dump course in notification table

