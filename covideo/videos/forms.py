from django.utils import timezone
from django import forms
from core.models import Video, Prompt


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "prompt", "video"]
        widgets = {"title": forms.TextInput(), "prompt": forms.Select()}
        labels = {"title": "Short description"}

    field_order = ["prompt", "title", "video"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        prompt_queryset = Prompt.objects.filter(day=timezone.now().date())
        self.fields["prompt"].queryset = prompt_queryset
        self.fields["prompt"].empty_label = "Open prompt (anything you want)"
        self.fields["video"].widget.attrs.update({"accept": "video/*"})
        if prompt_queryset.count() == 0:
            self.fields["prompt"].widget = forms.HiddenInput()

    def clean_video(self):
        video = self.cleaned_data["video"]
        if video.split(".")[-1] not in [
            "webm",
            "flv",
            "avi",
            "mov",
            "qt",
            "wmv",
            "mp4",
            "m4p",
            "m4v",
            "mpg",
            "mpeg",
            "m2v",
            "svi",
            "3gp",
            "3g2",
            "mxf",
        ]:
            raise forms.ValidationError("Please upload a valid video!")
        return video

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user

        if commit:
            obj.save()

        return obj
