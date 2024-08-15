from ninja import Router
from ninja.security import HttpBearer
from pydantic import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser
from .schemas import RegisterSchema, LoginSchema, TokenResponseSchema, ProfileSchema
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken

router = Router()

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            # Validate the token
            UntypedToken(token)
            validated_token = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated_token)
            return user
        except Exception:
            raise AuthenticationFailed("Invalid token")

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

@router.get("/profile/", response=ProfileSchema, auth=AuthBearer())
def profile(request):
    try:
        # Extract the token from the request
        token = request.auth
        
        # Decode the token
        validated_token = JWTAuthentication().get_validated_token(token)
        
        # Retrieve the user associated with the token
        user_id = validated_token.payload.get('user_id')
        user = CustomUser.objects.get(id=user_id)
        
        return user

    except CustomUser.DoesNotExist:
        raise AuthenticationFailed("User not found")

    except (TokenError, InvalidToken):
        raise AuthenticationFailed("Invalid or expired token")

