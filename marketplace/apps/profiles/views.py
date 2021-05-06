from typing import Any, Dict, Union, TYPE_CHECKING

from django.views.generic import UpdateView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.db.models import QuerySet
from django.db import models

from apps.profiles.forms import ProfileFormset

if TYPE_CHECKING:
    # workaround for mypy
    # https://github.com/typeddjango/django-stubs/issues/599#issuecomment-824056866
    from django.contrib.auth.models import User as UserType, AnonymousUser

User = get_user_model()


class ProfileView(LoginRequiredMixin, UpdateView):
    """A view for editing user profile at `/accounts/profile/`."""
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profiles/profile_form.html'
    success_url = '/accounts/profile/'

    def get_object(self, queryset: Any = None) -> "Union[UserType, AnonymousUser]":
        """Get User object for Profile view.
        Overridden because there is no `pk` or `slug` in the Profile url."""
        return self.request.user

    def get_context_data(self, **kwargs: Any) -> Dict[str, str]:
        """Add new form to a context."""
        context = super().get_context_data(**kwargs)

        if 'profileformset' not in kwargs:
            context['profileformset'] = ProfileFormset(instance=self.get_object())

        return context

    def form_valid(self, form):
        """If the main form is valid, validate the inline form."""
        # instantiate an inline form with POST data:
        profile_form = ProfileFormset(self.request.POST, self.request.FILES, instance=self.object)

        if profile_form.is_valid():
            profile_form.save()
        else:
            self.profile_form_invalid(form, profile_form)

        form.save()
        messages.success(self.request, 'Profile details has been updated.')
        return HttpResponseRedirect(self.get_success_url())

    def profile_form_invalid(self, form: Any, profile_form: ProfileFormset) -> HttpResponse:
        """Render the profile page with our form instances."""
        messages.error(self.request, 'Incorrect data provided.')
        return self.render_to_response(self.get_context_data(form=form, profileformset=profile_form))

    def form_invalid(self, form: Any) -> HttpResponse:
        """Process an invalid main form. Overridden only because of the message."""
        messages.error(self.request, 'Incorrect data provided.')
        return super().form_invalid(form)
