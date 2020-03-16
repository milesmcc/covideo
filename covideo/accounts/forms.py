from django import forms
from core.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["display_name", "email"]
        widgets = {
            "display_name": forms.TextInput(),
        }
        labels = {
            "display_name": "Name"
        }

    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("That email address is already registered.")
        return self.cleaned_data["email"]
