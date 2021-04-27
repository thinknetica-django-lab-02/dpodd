from django.db import models
from django.conf import settings
from django.urls import reverse

from sorl.thumbnail import ImageField


class Tag(models.Model):
    """
    A class used to represent a tag for an item of goods

    Attributes:
        name (str): the name of the tag, should be unique
    """
    name = models.CharField("name of the tag", max_length=30, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    A class used to represent a category for an item of goods

    Attributes:
        name (str): the name of the category, should be unique
    """
    name = models.CharField("name of the category", max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """
    A customer model stores the customer-related info and logic

    Attributes:
        user (class User): A registered user that is linked to this customer
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="related user model")

    def __str__(self):
        return self.user.username


class Goods(models.Model):
    """
    A model that represents an item of goods

    Attributes:
        title (str): A title of an item of goods
        description (str): A detailed description of an item of goods
        category (class Category): A category that an item of goods belongs to
        seller (class User): A seller of an item of goods
        customer (class Customer): A customer of an item of goods
        tags (list of class Tags): A list of tags for an item of goods
    """
    title = models.CharField("item's title", max_length=150)
    description = models.TextField("item's description")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="item's category")
    price = models.DecimalField("item's price (RUB)", max_digits=10, decimal_places=2, default=0.0)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='goods_sell', on_delete=models.CASCADE, null=True,
                               verbose_name="item's seller")
    customer = models.ForeignKey(Customer, related_name='goods_buy', on_delete=models.SET_NULL,
                                 null=True, verbose_name="item's customer")
    image = ImageField(upload_to='goods', null=True)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="item's tags")
    created_on = models.DateTimeField("created on", auto_now_add=True)

    class Meta:
        verbose_name = 'an item of goods'
        verbose_name_plural = 'items of goods'

    def __str__(self):
        return self.title[:30]

    def get_absolute_url(self):
        return reverse('main:goods-detail', args=[str(self.pk)])

    @property
    def is_ordered(self):
        return self.customer is not None


class Subscriber(models.Model):
    """
        Subscriber is a user that receive email notification when Goods collection changes.

        Attributes:
            user (class User): A subscribed user.
        """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="subscribed user")


class SMSLog(models.Model):
    """
    A model for saving SMS logs from Vonage.

    Attributes:
        code (4-digit int): A verification code that was sent to user via SMS provider.
        response (json): A json response from SMS provider.
    """
    code = models.IntegerField(verbose_name="verification code")
    response = models.JSONField(verbose_name="json response from SMS provider")
    created = models.DateTimeField(auto_now_add=True, verbose_name="code created")
