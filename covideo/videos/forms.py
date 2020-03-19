from django.utils import timezone
from django import forms
from core.models import Video, Prompt

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "prompt", "video"]
        widgets = {
            "title": forms.TextInput(),
            "prompt": forms.Select()
        }
        labels = {
            "title": "Short description"
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        prompt_queryset = Prompt.objects.filter(day=timezone.now().date())
        self.fields["prompt"].queryset = prompt_queryset
        self.fields["prompt"].empty_label = "Open prompt (anything you want)"
        if prompt_queryset.count() == 0:
            self.fields["prompt"].widget = forms.HiddenInput()

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.user = self.user
        
        if commit:
            obj.save()	
        
        return obj
