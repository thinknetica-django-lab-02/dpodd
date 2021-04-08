from datetime import date
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

    @staticmethod
    def calculate_age(birth_date):
        today = date.today()
        age = today.year - birth_date.year
        full_year_passed = (today.month, today.day) < (birth_date.month, birth_date.day)
        if not full_year_passed:
            age -= 1
        return age

    def clean_birthday(self):
        date_of_birth = self.cleaned_data.get('birthday')

        if self.calculate_age(date_of_birth) < 18:
            raise forms.ValidationError("You must be at least 18 of age.")

        return date_of_birth


ProfileFormset = inlineformset_factory(User, Profile, form=ProfileUpdateForm, extra=1, can_delete=False)
