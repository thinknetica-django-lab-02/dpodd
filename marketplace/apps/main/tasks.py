from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.conf import settings

from pytz import UTC

from config import celery_app
from apps.main.models import Goods, Subscriber


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


@celery_app.task()
def notify_subscribers_week_additions():
    """Send an email to subscribers about new goods additions in the last week."""

    week_ago = datetime.utcnow().replace(tzinfo=UTC) - timedelta(days=7)
    new_goods_last7days = Goods.objects.filter(created_on__gte=week_ago)
    if new_goods_last7days.exists():
        message = "We have new additions in our collection!\nJust see:\n" + \
              '\n'.join([item.title for item in new_goods_last7days])
    else:
        message = ''
    subscribers = Subscriber.objects.select_related('user').all()

    # send mail
    if message:
        for subscriber in subscribers:
            if subscriber.user.email:
                send_mail(
                    "[Marketplace] NEW additions in the last week",
                    message,
                    settings.EMAIL_DEFAULT_FROM,
                    [subscriber.user.email],
                    fail_silently=True
                )
