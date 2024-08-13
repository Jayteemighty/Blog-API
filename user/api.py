from ninja import Router
from ninja.security import HttpBearer
from pydantic import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser

router = Router()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            RefreshToken(token)
            return token
        except Exception:
            raise AuthenticationFailed("Invalid token")

class RegisterSchema(BaseModel):
    email: str
    password: str
    username: str
    first_name: str
    last_name: str
    phone_number: str

class LoginSchema(BaseModel):
    email: str
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
    user = CustomUser.objects.create_user(
        email=data.email,
        password=data.password,
        username=data.username,
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number
    )
    tokens = get_tokens_for_user(user)
    return tokens

@router.post("/login/", response=TokenResponseSchema)
def login(request, data: LoginSchema):
    user = CustomUser.objects.filter(email=data.email).first()
    if user is None or not user.check_password(data.password):
        raise AuthenticationFailed("Invalid credentials")
    tokens = get_tokens_for_user(user)
    return tokens

@router.get("/profile/", auth=AuthBearer())
def profile(request):
    user = CustomUser.objects.get(email=request.auth)
    return {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
    }
