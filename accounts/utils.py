import random
from django.core.mail import EmailMessage
from .models import User, OneTimePassword
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html


def generateOtp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(i, 9))
    return otp


def send_code_to_user(email):
    Subject = "Email Verification"
    otp_code = generateOtp()
    verification_url = f"https://www.connectjcu.org/email-verification/{otp_code}"
    print(otp_code)
    user = User.objects.get(email=email)
    email_body = format_html(
        "<p>Dear {0},</p>"
        "<p>Thank you for registering on the ConnectJCU Platform.</p>"
        "<p>To complete your registration, please verify your email address by clicking the link below:</p>"
        "<p><a href='{1}'>{1}</a></p><br>"
        "<p>If you did not create an account on ConnectJCU, you can ignore this email.</p>"
        "<p>Best regards,</p>"
        "<p>The ConnectJCU Team</p>",
        user.first_name,
        verification_url,
    )
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)
    send_mail(
        subject=Subject,
        message="",
        html_message=email_body,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=False,
    )

    # sd_email = EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email] )
    # sd_email.send(fail_silently=True)


def send_normal_email(data):
    email = EmailMessage(
        subject=data["email_subject"],
        body=data["email_body"],
        from_email=settings.EMAIL_HOST_USER,
        to=[data["to_email"]],
    )
    email.send()