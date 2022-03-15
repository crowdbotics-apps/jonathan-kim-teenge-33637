from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    AccountViewSet,
    WishViewSet,
    AlertViewSet,
    CourseViewSet,
    SettingViewSet
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("accounts", AccountViewSet, basename="accounts")
router.register("wishes", WishViewSet, basename="wishes")
router.register("alerts", AlertViewSet, basename="alerts")
router.register("courses", CourseViewSet, basename="courses")
router.register("settings", SettingViewSet, basename="settings")

urlpatterns = [
    path("", include(router.urls)),
]
