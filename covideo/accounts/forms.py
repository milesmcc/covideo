from django import forms
from core.models import User

class AbridgedUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]
        help_texts = {
            "email": "On Covideo, your email is your account. There are no passwords to deal with&mdash;you just give us your email, and we'll send you a special link to log in."
        }