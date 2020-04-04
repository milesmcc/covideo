from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from .models import User, Video
from .tasks import process_video, send_email


def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        instance.send_welcome_email()


post_save.connect(send_welcome_email, sender=User, dispatch_uid="send_welcome_email")


def process_video_upload(sender, instance, created, **kwargs):
    if created:
        process_video.delay(instance.pk)


post_save.connect(
    process_video_upload, sender=Video, dispatch_uid="process_video_upload"
)


def notify_on_video_status_change(sender, instance, **kwargs):
    if not hasattr(instance, "pk"):
        return
    current = Video.objects.filter(pk=instance.pk).first()
    if current == None:
        return

    if current.status != "PROCESSED" and instance.status == "PROCESSED":
        for admin in User.objects.filter(is_superuser=True):
            send_email.delay(
                admin,
                "Video awaiting approval",
                "core/emails/new_upload.html",
                {"video": instance},
                override_opt_out=True,
            )

    if current.status != "PUBLISHED" and instance.status == "PUBLISHED":
        send_email.delay(
            instance.user,
            f"Your {instance.created.strftime('%x')} video is live",
            "core/emails/published.html",
            {"video": instance},
        )

    if current.status != "INVALID" and instance.status == "INVALID":
        send_email.delay(
            instance.user,
            f"Problem with your {instance.created.strftime('%x')} video",
            "core/emails/processing_error.html",
            {"video": instance},
        )

        for admin in User.objects.filter(is_superuser=True):
            send_email.delay(
                admin,
                f"Problem with {instance.created.strftime('%x')} video",
                "core/emails/processing_error.html",
                {"video": instance},
            )


pre_save.connect(
    notify_on_video_status_change,
    sender=Video,
    dispatch_uid="notify_on_video_status_change",
)
