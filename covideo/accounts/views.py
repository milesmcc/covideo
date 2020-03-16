from django.views.generic import CreateView, TemplateView
from django.shortcuts import reverse, redirect
from core.models import User
from django.contrib.auth import login
from . import forms

class RegisterView(CreateView):
    form_class = forms.UserForm
    model = User
    template_name = "accounts/views/register.html"
    success_path = "accounts:register_complete"

    def get_success_url(self):
        login(self.request, self.object)
        return reverse(self.success_path)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_path)
        return super().dispatch(request, *args, **kwargs)

class RegisterCompleteView(TemplateView):
    template_name = "accounts/views/register.html"