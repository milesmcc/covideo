from django.utils import timezone
from django import forms
from core.models import Video, Prompt


class VideoForm(forms.ModelForm):
    name = forms.CharField(max_length=64, min_length=1, label="Your display name", help_text="This and future videos by you will show up under this name.")

    class Meta:
        model = Video
        fields = ["title", "prompt", "video"]
        widgets = {"title": forms.TextInput(), "prompt": forms.CheckboxInput()}
        labels = {"title": "Short description"}

    field_order = ["prompt", "title", "video", "name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        prompt_queryset = Prompt.objects.filter(day=timezone.now().date())
        self.fields["prompt"].queryset = prompt_queryset
        self.fields["prompt"].empty_label = "Open prompt (anything you want)"
        self.fields["video"].widget.attrs.update({"accept": "video/mp4,video/x-m4v,video/*"})

        if prompt_queryset.count() == 0:
            self.fields["prompt"].widget = forms.HiddenInput()
        if self.user.display_name != "":
            self.fields["name"].widget = forms.HiddenInput()

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user

        if self.cleaned_data["name"] != obj.user.display_name:
            obj.user.display_name = self.cleaned_data["name"]
            if commit:
                obj.user.save()

        if commit:
            obj.save()

        return obj
