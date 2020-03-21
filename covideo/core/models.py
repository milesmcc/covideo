from django.contrib.auth.models import AbstractUser
from django.core.signing import TimestampSigner
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.http import urlquote
from django.shortcuts import reverse
from .tasks import send_email
import uuid

# USERS


def username_generator():
    return str(uuid.uuid4())


class User(AbstractUser):
    # Email
    # Password (won't use)
    # First name (won't use)
    # Last name (won't use)
    username = models.TextField(default=username_generator, unique=True)

    # CORE INFO
    display_name = models.TextField(max_length=64, blank=True)
    verified_email = models.BooleanField(default=False)
    email_opt_out = models.BooleanField(default=False)

    # ADD'L BIOGRAPHICAL INFO
    location = models.TextField(max_length=64, blank=True, default="")
    age = models.IntegerField(null=True, blank=True)

    def ak_param(self):
        return TimestampSigner().sign(str(self.username))

    def send_welcome_email(self, request=None):
        send_email.delay(
            self,
            "Verify your email",
            "accounts/emails/welcome.html",
            {},
            request=request,
            override_opt_out=True,
        )

    def send_login_email(self, request=None, redirect=None):
        if redirect == None:
            redirect = "/"
        send_email.delay(
            self,
            "Making sure it's you",
            "accounts/emails/login.html",
            {"redirect": redirect,},
            request=request,
            override_opt_out=True,
        )

    def __str__(self):
        if self.display_name != "":
            return self.display_name
        if self.email != "":
            return str(self.email)
        return self.username


class Prompt(models.Model):
    day = models.DateField()
    text = models.TextField()

    def __str__(self):
        return self.text


# VIDEOS


def video_upload_location(i, k):
    return f"videos/{i.user.pk}/{get_random_string()}_{k}"


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=128)
    status = models.CharField(
        max_length=16,
        default="PENDING",
        choices=[
            ("PENDING", "Pending"),
            ("PROCESSED", "Processed"),
            ("PUBLISHED", "Published"),
            ("HIDDEN", "Hidden"),
            ("INVALID", "Invalid"),
        ],
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    prompt = models.ForeignKey(Prompt, on_delete=models.SET_NULL, null=True, blank=True)
    video = models.FileField(upload_to=video_upload_location, help_text="Try to keep your video concise&mdash;aim for two minutes or less.")
    duration = models.IntegerField(null=True, blank=True)
    featured = models.BooleanField(default=False)
