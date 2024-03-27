from celery import shared_task
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings

from .models import CustomUser

@shared_task
def send_code_for_authentication(email, code):
    user = get_object_or_404(CustomUser, email=email)
    subject = f'for {user.username}'
    message = f'Dear friend! In this letter the code for your authorized: {code}'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email], fail_silently=False)
