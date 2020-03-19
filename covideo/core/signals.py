from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import User

def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        instance.send_welcome_email()

post_save.connect(send_welcome_email, sender=User, dispatch_uid="send_welcome_email")
