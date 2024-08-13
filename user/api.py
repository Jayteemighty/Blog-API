from typing import List
from ninja import NinjaAPI
from ninja.security import BearerAuth
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer, CreateAccountSerializer, LoginSerializer,
    UserDetailsSerializer, ChangePasswordSerializer
)

api = NinjaAPI()

User = get_user_model()

class JWTAuth(BearerAuth):
    def authenticate(self, request, token):
        try:
            refresh_token = RefreshToken(token)
            user_id = refresh_token.payload.get('user_id')
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            return None

@api.post("/register", response=UserSerializer)
def register(request, data: CreateAccountSerializer):
    """Register a new user."""
    serializer = CreateAccountSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return user

@api.post("/login")
def login(request, data: LoginSerializer):
    """Login an existing user."""
    serializer = LoginSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    refresh_token = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh_token),
        'access': str(refresh_token.access_token),
    })

@api.get("/users/{user_id}", response=UserDetailsSerializer, auth=JWTAuth())
def get_user(request, user_id: str):
    """Retrieve user details."""
    user = get_object_or_404(User, id=user_id)
    return user

@api.put("/users/{user_id}", response=UserDetailsSerializer, auth=JWTAuth())
def update_user(request, user_id: str, data: UserDetailsSerializer):
    """Update user details."""
    user = get_object_or_404(User, id=user_id)
    serializer = UserDetailsSerializer(user, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return user

@api.delete("/users/{user_id}", auth=JWTAuth())
def delete_user(request, user_id: str):
    """Delete a user."""
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return Response({"message": "User deleted successfully"})

@api.post("/change-password", auth=JWTAuth())
def change_password(request, data: ChangePasswordSerializer):
    """Change the password for a user."""
    serializer = ChangePasswordSerializer(data=data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    user = request.user
    serializer.update(user, serializer.validated_data)
    return Response({"message": "Password changed successfully"})