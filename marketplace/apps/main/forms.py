from django import forms

from .models import Goods


class AddItemOfGoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'description', 'category', 'price', 'image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'required': False}),
        }


class EditItemOfGoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title', 'description', 'category', 'price', 'image']
