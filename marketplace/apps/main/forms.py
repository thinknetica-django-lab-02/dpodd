from django.forms import ModelForm

from .models import Goods


class AddItemOfGoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'description', 'category', 'price']