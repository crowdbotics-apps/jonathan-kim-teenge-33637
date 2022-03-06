from django.urls import path, include
from rest_framework.routers import DefaultRouter

from home.api.v1.viewsets import (
    SignupViewSet,
    LoginViewSet,
    AccountViewSet,
    WishViewSet,
    NotificationViewSet,
    CourseViewSet
)

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")
router.register("accounts", AccountViewSet, basename="accounts")
router.register("wishes", WishViewSet, basename="wishes")
router.register("notifications", NotificationViewSet, basename="notifications")
router.register("courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("", include(router.urls)),
]
