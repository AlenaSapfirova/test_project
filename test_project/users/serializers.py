from datetime import timedelta, timezone, datetime
# from django.utils import timezone
from rest_framework import serializers
from rest_framework.views import Response, status
from rest_framework.serializers import ValidationError
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404


from .models import CustomUser, Token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'id']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data) 
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()
    
    def validate(self, data):
        if CustomUser.objects.filter(email = data.get('email')).exists():
            user = CustomUser.objects.get(email=data.get('email'))
            if user.check_password(data.get('password')):
                return data
            raise ValidationError('password is uncorrect')
        raise ValidationError('user was not found')


class CheckOtpCodeSerializer(serializers.Serializer):
    token = serializers.CharField()
    
    def validate(self, data):
        token = data.get('token', None)
        user_token = Token.objects.filter(token=token).first()
        if user_token:
            time_live = user_token.created_at + user_token.expire
            if datetime.now(timezone.utc) <= time_live:
                return data
            raise ValidationError('the token was transferred incorrectly or expired')
        raise ValidationError('the token was transferred incorrectly or expired')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username']
