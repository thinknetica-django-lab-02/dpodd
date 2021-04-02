from django.shortcuts import render, reverse
from django.views.generic import UpdateView
from django.contrib import messages

from .models import Profile, User
from .forms import ProfileUpdateForm, ProfileFormset


class ProfileView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profiles/profile_form.html'

    def get_success_url(self):
        return reverse('profiles:profile', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['profileformset'] = ProfileFormset(self.request.POST)
        else:
            context['profileformset'] = ProfileFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profileformset = context.get('profileformset')

        self.object = form.save()

        if profileformset.is_valid():
            profileformset.instance = self.object
            profileformset.save()

        messages.success(self.request, 'Profile details updated.')
        return super().form_valid(form)
