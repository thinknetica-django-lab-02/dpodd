from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail

from apps.main.models import Goods, Subscriber


@receiver(post_save, sender=Goods)
def send_mail_when_goods_add(sender, instance, created, **kwargs):
    """Send an email notification to Subscribers when a new item of Goods has been added to site."""
    if created:
        subscribers = Subscriber.objects.select_related('user').all()
        for subscriber in subscribers:
            if subscriber.user.email:
                send_mail(
                    "NEW item added",
                    f"{instance.title} has been added to the site.",
                    'from@example.oom',
                    [subscriber.user.email],
                    fail_silently=True
                )
