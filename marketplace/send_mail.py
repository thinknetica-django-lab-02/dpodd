from django.core.mail import send_mail
from django.contrib.auth import get_user_model


def send_mail_2_all_users(subject: str, message: str) -> None:
    """Send mail to all registered users who specified the email."""
    User = get_user_model()

    users = User.objects.all()

    for user in users:
        if user.email:
            send_mail(
                subject,
                message,
                'from@example.com',
                [user.email],
                fail_silently=False,
            )


def send_welcome_letter() -> None:
    """Send welcome letter to all users."""
    subject = "Welcome to <Marketplace>!"
    msg = "We hope you will enjoy everything."
    send_mail_2_all_users(subject, msg)


send_welcome_letter()
