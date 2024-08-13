from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from ninja import Router
from ninja.security import HttpBearer
from pydantic import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

router = Router()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            RefreshToken(token)
            return token
        except Exception:
            raise AuthenticationFailed("Invalid token")

class RegisterSchema(BaseModel):
    username: str
    password: str
    email: str

class LoginSchema(BaseModel):
    username: str
    password: str

class TokenResponseSchema(BaseModel):
    access: str
    refresh: str

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@router.post("/register/", response=TokenResponseSchema)
def register(request, data: RegisterSchema):
    user = User.objects.create_user(username=data.username, password=data.password, email=data.email)
    tokens = get_tokens_for_user(user)
    return tokens

@router.post("/login/", response=TokenResponseSchema)
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if user is None:
        raise AuthenticationFailed("Invalid credentials")
    tokens = get_tokens_for_user(user)
    return tokens

@router.get("/profile/", auth=AuthBearer())
def profile(request):
    user = request.user
    return {"username": user.username, "email": user.email}
