from django.shortcuts import render, reverse
from django.views.generic import UpdateView

from .models import Profile
from .forms import ProfileUpdateForm


class ProfileView(UpdateView):
    model = Profile
    form_class = ProfileUpdateForm

    def get_success_url(self):
        return reverse('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['profile_pk'] = self.kwargs['pk']
        return context
