from django.core.mail import send_mail
from django.conf import settings

from config import celery_app


@celery_app.task()
def notify_new_item_added(email_title: str, to_email: str):
    """Notify a subscriber that a new item in Goods is added."""
    send_mail(
        "NEW item added",
        f"{email_title} has been added to the site.",
        settings.EMAIL_DEFAULT_FROM,
        [to_email],
        fail_silently=True
    )

