from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Token

def get_otp_token(user):
    token = get_random_string(length=6, allowed_chars='1234567890')
    user_token = Token(user=user, token=token)
    user_token.save()
    return user_token

def get_tokens_for_user(user):
    """Method of getting token for user."""
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
