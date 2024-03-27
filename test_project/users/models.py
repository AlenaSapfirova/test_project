from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[
        RegexValidator(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')],
        verbose_name='user email')
    username = models.CharField(max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Token(models.Model):
    token = models.CharField(max_length=6, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    expire = models.DurationField(default=timedelta(minutes=5))

    def __str__(self):
        return self.token
    
    class Meta:
        verbose_name='token'
        verbose_name_plural='tokens'

