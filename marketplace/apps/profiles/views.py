from django.views.generic import UpdateView
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import User
from .forms import ProfileFormset


class ProfileView(UpdateView):
    """A view for editing user profile at `/accounts/profile/`."""
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profiles/profile_form.html'
    success_url = '/accounts/profile/'

    def get_object(self, **kwargs):
        """Get user object from the request. Overridden because we don't need to hit the database again, we already have
        the `User` object in `self.request'."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Add new form to a context."""
        context = super().get_context_data(**kwargs)

        profileformset = ProfileFormset(instance=self.get_object(kwargs['request']))
        profileformset.can_delete = False
        context['profileformset'] = profileformset

        return context

    def get(self, request, *args, **kwargs):
        """Process a GET request.
        Overridden only because of self.get_object(request)
        """
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(request=request))

    def form_valid(self, form, formset):
        """Validate the inline form and save both forms provided."""
        if formset.is_valid():
            formset.save()
        else:
            messages.error(self.request, 'Incorrect data provided.')
            return HttpResponseRedirect(self.get_success_url())
        form.save()
        messages.success(self.request, 'Profile details has been updated.')
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        """Process a POST request.
        Validate the main form anf create an instance of the inline formset with POST data.
        """
        self.object = self.get_object()

        form = self.get_form()
        profile_form = ProfileFormset(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            messages.error(self.request, 'Incorrect data provided.')
            return self.form_invalid(form)
