from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_auth import serializers

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

        setting = Setting.objects.filter(user__setting = user.id).first()
        if setting.is_deactivated:
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

# TODO: save wish-> save wish+ get course+dump course in notification table

