from datetime import datetime, timedelta
import random
import json

from django.core.mail import send_mail
from django.conf import settings
from pytz import UTC
import vonage

from config import celery_app
from config.settings.base import env
from apps.main.models import Goods, Subscriber, SMSLog


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


@celery_app.task()
def send_test_sms():
    """Send test sms to developer's number via Vonage. """

    client = vonage.Client(key=env('VONAGE_API_KEY'), secret=env('VONAGE_API_SECRET'))
    sms = vonage.Sms(client)

    # generate verification code
    code = random.randint(1000, 9999)

    # send sms
    responseData = sms.send_message(
        {
            "from": settings.SMS_FROM_DEFAULT,
            "to": settings.SMS_PHONE_NUMBER_TEST,
            "text": f"You verification code is {code}.",
        }
    )

    # some prints to celery console
    print(responseData)
    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    smslog = SMSLog(code=code, response=json.dumps(responseData))
    smslog.save()
