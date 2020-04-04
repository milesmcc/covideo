from django.views.generic import CreateView, TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse, get_object_or_404
from django.contrib import messages
from core.models import Video

import random
from . import forms


class SubmitView(LoginRequiredMixin, CreateView):
    form_class = forms.VideoForm
    model = Video
    template_name = "videos/views/submit.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["initial"] = {"name": self.request.user.display_name}
        return kwargs

    def get_success_url(self):
        messages.success(
            self.request,
            "Thank you for your video! We will process and publish it shortly.",
        )
        return reverse("videos:personal")


class VideoView(DetailView):
    model = Video
    template_name = "videos/views/video.html"

    def get_object(self):
        return get_object_or_404(Video, uuid=self.kwargs["uuid"])

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = self.get_object().title
        data["recommended"] = (
            Video.objects.filter(status="PUBLISHED")
            .exclude(pk=self.get_object().pk)
            .order_by("?")[:4]
        )
        return data


class PersonalVideosView(LoginRequiredMixin, TemplateView):
    template_name = "videos/views/personal_videos.html"


class BrowseView(ListView):
    template_name = "videos/views/browse.html"
    model = Video
    paginate_by = 10

    def get_queryset(self):
        filters = {"featured": True, "status": "PUBLISHED"}
        if self.request.GET.get("day", "None") != "None":
            filters["created__date"] = self.request.GET.get("day")
        if self.request.GET.get("featured") == "False":
            del filters["featured"]
        if self.request.GET.get("search", "None") != "None":
            filters["title__icontains"] = self.request.GET.get("search")
        if self.request.GET.get("user", "None") != "None":
            filters["user__username"] = self.request.GET.get("user")
        return Video.objects.filter(**filters).order_by("-created")

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(*args, object_list=object_list, **kwargs)
        data["url_parameters"] = ""
        for i in ["day", "featured", "search", "user"]:
            if self.request.GET.get(i, "None") != "None":
                data["url_parameters"] += f"&{i}={self.request.GET.get(i)}"
        data["expanded"] = len(self.request.GET.keys()) == 0
        return data
