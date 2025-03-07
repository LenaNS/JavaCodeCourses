from django.contrib.auth import authenticate
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RefreshTokenSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)


class RegisterView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": "User created successfully",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericViewSet):
    serializer_class = UserLoginSerializer

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)

        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        response = Response(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "access_token", access_token, httponly=True, secure=True, samesite="Strict"
        )
        response.set_cookie(
            "refresh_token",
            refresh_token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        return response


class RefreshTokenView(GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    @action(detail=False, methods=["post"], url_path="refresh")
    def refresh(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProtectedView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Только для аутентифицированных пользователей

    def get(self, request):
        return Response(
            {
                "message": "This is a protected resource.",
                "user": str(
                    request.user
                ),  # Информация о текущем аутентифицированном пользователе
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def get(self, request):
        response = Response({"message": "Logged out successfully"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
