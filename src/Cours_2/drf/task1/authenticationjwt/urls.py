from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LoginView, LogoutView, ProtectedView, RefreshTokenView, RegisterView

router = DefaultRouter()

router.register(r"register", RegisterView, basename="register")
router.register(r"users", LoginView, basename="users")
router.register(r"users", RefreshTokenView, basename="refresh")

urlpatterns = [
    path("", include(router.urls)),
    path("protected/", ProtectedView.as_view(), name="protected_resource"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
