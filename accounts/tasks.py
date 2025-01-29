
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
import logging

logger = logging.getLogger(__name__)


# Задача по отправлению писем, после успешной регистрации пользователя
@shared_task
def send_registration_email(user_pk):
    try:
        user = CustomUser.objects.get(pk=user_pk)
    except CustomUser.DoesNotExist:
        print(f"Пользователь с id {user_pk} не найден")
    mail_subject = 'Регистрация на сайте - успешна!'  
    message = render_to_string('registration/registration_email.txt', {
        'user': user,
    })
    to_email = user.email
    
    try:
        send_mail( subject=mail_subject, message=message, from_email=settings.EMAIL_HOST_USER, 
              recipient_list=[to_email], fail_silently=False)
        logger.info(f'Письмо успешно отправлено на {to_email}.')
    except Exception as e:
        logger.error(f'Не удалось отправить письмо: {e}')
        

# Задача отправлению письма для изменения пароля 
@shared_task
def send_password_reset_email(user_email, subject, message):
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )

