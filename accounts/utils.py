import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(email):
    otp = generate_otp()

    send_mail(
        subject="Email tasdiqlash kodi",
        message=f"Sizning tasdiqlash kodingiz: {otp}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )

    return otp

def send_otp_phone_number(phone_number):
    otp = generate_otp()
    return otp