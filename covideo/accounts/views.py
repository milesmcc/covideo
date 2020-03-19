from django.views.generic import FormView, TemplateView, RedirectView
from django.shortcuts import reverse, redirect
from django.contrib import messages
from core.models import User, username_generator
from django.contrib.auth import login, logout
from . import forms


class LoginView(FormView):
    form_class = forms.AbridgedUserForm
    template_name = "accounts/views/login.html"
    success_path = "index"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            user = User.objects.filter(email__iexact=email).first()
            user.send_login_email(redirect=self.request.GET.get("next"))
            messages.success(self.request, f"We've sent a login link to {email}. Click it to log in.")
            self.success_path = "accounts:login"
        else:
            user = User.objects.create_user(username_generator(), email)
            self.success_path = "accounts:register_complete"
        return super().form_valid(form)

    def get_success_url(self):
        redirect = ""
        if "next" in self.request.GET:
            redirect = f"?next={self.request.GET.get('next')}"
        return reverse(self.success_path) + redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return super().dispatch(request, *args, **kwargs)


class RegisterCompleteView(TemplateView):
    template_name = "accounts/views/login.html"


class LogoutView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "You have been successfully logged out.")
        return reverse("index")


class UnsubscribeEmailView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        self.request.user.email_opt_out = True
        self.request.user.save()
        messages.success(
            self.request,
            "You have been unsubscribed from all non-essentiall communications.",
        )
        return reverse("index")

class AuthenticatedRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.GET.get("next", "/")
