from django.shortcuts import render, reverse
from django.views.generic import UpdateView

from .models import Profile
from .forms import ProfileUpdateForm


class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse('index')
