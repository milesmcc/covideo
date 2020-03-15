from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Email
    # Username (auto-generated)
    # Password (won't use)
    # First name (won't use)
    # Last name (won't use)
    display_name = models.TextField(max_length=64)
    verified_email = models.BooleanField(default=False)
    subscriptions = models.ManyToManyField("User")
