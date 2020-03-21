from django.views.generic import CreateView, TemplateView, ListView
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
        kwargs["initial"] = {"name": self.request.user.display_name}
        return kwargs

    def get_success_url(self):
        messages.success(
            self.request,
            "Thank you for your video! We will process and publish it shortly.",
        )
        return reverse("videos:personal")


class PersonalVideosView(LoginRequiredMixin, TemplateView):
    template_name = "videos/views/personal_videos.html"


class BrowseView(ListView):
    template_name = "videos/views/browse.html"
    model = Video
    paginate_by = 10

    def get_queryset(self):
        filters = {"featured": True, "status": "PUBLISHED"}
        if "day" in self.request.GET:
            filters["day"] = self.request.GET.get("day")
        if "featured" in self.request.GET:
            filters["featured"] = self.request.GET.get("featured") == "True"
        if "search" in self.request.GET:
            filters["title__icontains"] = self.request.GET.get("search")
        if "user" in self.request.GET:
            filters["user__username"] = self.request.GET.get("user")
        return Video.objects.filter(**filters).order_by("-created")

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(*args, object_list=object_list, **kwargs)
        data["url_parameters"] = (
            f'&day=self.request.GET.get("day")&featured={self.request.GET.get("featured")}'
            + f'&search={self.request.GET.get("search")}&user={self.request.GET.get("user")}'
        )
        data["expanded"] = len(self.request.GET.keys()) == 0
        return data
