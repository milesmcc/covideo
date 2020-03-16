from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    # Email
    # Password (won't use)
    # First name (won't use)
    # Last name (won't use)
    username = models.TextField(default=uuid.uuid4, unique=True)
    
    # CORE INFO
    display_name = models.TextField(max_length=64)
    verified_email = models.BooleanField(default=False)
    
    # ADD'L BIOGRAPHICAL INFO
    location = models.TextField(max_length=64, blank=True, default="")
    age = models.IntegerField(null=True)
