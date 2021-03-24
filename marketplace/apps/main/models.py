from django.db import models
from django.conf import settings


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Goods(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='goods_sell', on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, related_name='goods_buy', on_delete=models.SET_NULL,
                                 null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title[:30]

    @property
    def is_ordered(self):
        return self.customer is not None
