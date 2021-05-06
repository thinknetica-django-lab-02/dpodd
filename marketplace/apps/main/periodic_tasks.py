import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import UTC


from apps.main.models import Goods, Subscriber
from django.core.mail import send_mail


def notify_subscribers_on_the_new_goods():
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
                    'from@example.oom',
                    [subscriber.user.email],
                    fail_silently=False
                )


def start_scheduler():
    logging.warning('Starting background scheduler.')
    scheduler = BackgroundScheduler(timezone=UTC)

    every_friday = CronTrigger(day_of_week=5, hour=12, timezone=UTC)

    scheduler.add_job(notify_subscribers_on_the_new_goods, every_friday)
    scheduler.start()
