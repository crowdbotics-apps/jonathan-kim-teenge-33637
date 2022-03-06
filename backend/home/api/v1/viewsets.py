from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from home.api.v1.serializers import (
    SignupSerializer,
    UserSerializer,
    AccountSerializer,
    WishSerializer,
    NotificationSerializer,
    CourseSerializer
)
from home.wish import Wish
from users.models import User
from home.notifications import Notification
from home.courses import Course

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
        return Response({"token": token.key, "user": user_serializer.data})

class AccountViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer
    queryset = User.objects.all()

class WishViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wish.objects.all()
    serializer_class = WishSerializer

    def create(self, request, *args, **kwargs):
        try:
            if not request.data._mutable:
                request.data._mutable = True
        except:
            pass
        request.data['user'] = request.user.pk
        response = super().create(request, *args, **kwargs)
        return response

class NotificationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

class CourseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()



