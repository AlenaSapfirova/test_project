from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.views import APIView
from rest_framework.views import Response, status
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, inline_serializer, OpenApiResponse
)
from drf_spectacular.types import OpenApiTypes

from .serializers import (RegisterSerializer, LoginSerializer,
                          CheckOtpCodeSerializer, ProfileSerializer)
from .models import CustomUser, Token
from .tasks import send_code_for_authentication
from .utils import get_otp_token, get_tokens_for_user

@extend_schema(
    summary='Authenticated',
    description='Registration an account',
    tags=['Authenticated'],
    request=RegisterSerializer(),
    responses={
        201: OpenApiResponse(description="your account created"),
        400: OpenApiResponse(description="user with this user email already exists.")
    },
)

class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'your account created'},
                        status=status.HTTP_201_CREATED)

@extend_schema(
    summary='Authenticated',
    description='Entrance to the account',
    tags=['Authenticated'],
    request=LoginSerializer(),
    responses={
        200: OpenApiResponse(description="you are logged in successfully"),
        400: OpenApiResponse(description="password is uncorrect or user was not found"),
    },
)
class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'],
                            password=serializer.validated_data['password'])
        code = str(get_otp_token(user))
        send_code_for_authentication.delay(user.email, code)
        return Response({'code': code, 'message': 'logged in successfully'},
                        status=status.HTTP_200_OK)


@extend_schema(
    summary='Authenticated',
    description='Check time mark',
    tags=['Authenticated'],
    request=CheckOtpCodeSerializer(),
    responses={
        200: OpenApiResponse(description="token is correct"),
        400: OpenApiResponse(description="the token was transferred incorrectly or expired")
    },
)

class CheckOtpCodeAPIView(APIView):
    serializer_class = CheckOtpCodeSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CheckOtpCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = Token.objects.filter(token=serializer.validated_data['token']).first()
        tokens = get_tokens_for_user(token.user)
        login(request, token.user)
        token.delete()
        return Response({'message':tokens}, status=status.HTTP_200_OK)

@extend_schema(
    summary='Profile',
    description='Get, patch, delete profile',
    tags=['Profile'],
    request=ProfileSerializer(),
    responses=ProfileSerializer()
)
        
class ProfileAPIView(APIView):
    serializer_class = ProfileSerializer
    
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response({'me': serializer.data}, status=status.HTTP_200_OK)
    
    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data,
                                       partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'me': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        serializer = ProfileSerializer(request.user)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LogoutAPIVIew(APIView):

    def post(self, request):
        logout(request)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        return response
