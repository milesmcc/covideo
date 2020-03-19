from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.contrib import messages
from core.models import Video
from . import forms


class SubmitView(LoginRequiredMixin, CreateView):
    form_class = forms.VideoForm
    model = Video
    template_name = "videos/views/submit.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        messages.success(
            self.request,
            "Thank you for your video! We will process and publish it shortly.",
        )
        return reverse("videos:personal")


class PersonalVideosView(LoginRequiredMixin, TemplateView):
    template_name = "videos/views/personal_videos.html"

class BrowseView(TemplateView):
    template_name = "videos/views/browse.html"
