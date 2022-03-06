from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    AccountViewSet,
    WishViewSet
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("account", AccountViewSet, basename="account")
router.register("wish", WishViewSet, basename="wish")

urlpatterns = [
    path("", include(router.urls)),
]
