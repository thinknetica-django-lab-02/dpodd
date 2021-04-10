from django import forms
from django.forms import inlineformset_factory

from .models import Profile, User


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Select a date.',
                    'type': 'date',
                },
            ),
        }


ProfileFormset = inlineformset_factory(User, Profile, form=ProfileUpdateForm, extra=1)
