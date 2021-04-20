from django.dispatch import receiver
from django.db.models.signals import post_save

from apps.main.models import Goods, Subscriber
from .tasks import notify_new_item_added


@receiver(post_save, sender=Goods)
def send_mail_when_goods_add(sender, instance, created, **kwargs):
    """Send an email notification to Subscribers when a new item of Goods has been added to site."""
    if created:
        subscribers = Subscriber.objects.select_related('user').all()
        for subscriber in subscribers:
            if subscriber.user.email:
                # async task:
                notify_new_item_added.delay(instance.title, subscriber.user.email)
