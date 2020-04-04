from celery import shared_task
from django.core import mail
from django.conf import settings
from django.apps import apps
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.files import File
import os
import subprocess
import html2text


@shared_task
def send_email(user, subject, template, context, request=None, override_opt_out=False):
    if not user.email_opt_out or override_opt_out:
        context["to"] = user.email
        context["base_url"] = settings.ROOT_PATH
        context["user"] = user
        context["ak"] = f"ak={user.ak_param()}"
        richtext = render_to_string(template, context=context, request=request)
        plaintext = html2text.HTML2Text().handle(richtext)
        mail.send_mail(
            subject,
            plaintext,
            "Covideo <hello@covideo.org>",
            [user.email],
            html_message=richtext,
        )

@shared_task
def process_video(video_pk):
    Video = apps.get_model('core', 'Video')
    video = Video.objects.get(pk=video_pk)

    def expect_zero(call):
        if call != 0:
            video.status = "INVALID"
            video.save()
            raise "error occured while processing"

    temp_id = get_random_string()

    input_video_location = f"/tmp/{temp_id}_down"

    output_video_location = f"/tmp/{temp_id}_processed.mp4"
    output_thumbnail_location = f"/tmp/{temp_id}_thumbnail.png"

    # Download video from s3
    expect_zero(subprocess.call(["wget", video.video.url, "-O", input_video_location]))

    # Compress video
    expect_zero(subprocess.call(["ffmpeg", "-i", input_video_location, "-vcodec", "libx264", "-crf", "23", output_video_location]))

    # Get thumbnail
    expect_zero(subprocess.call(["ffmpeg", "-i", output_video_location, "-ss", "00:00:01.000", "-vframes", "1", output_thumbnail_location]))

    # Upload to remote storage
    video.video.save("{temp_id}_processed.mp4", File(open(output_video_location, "rb")))
    video.thumbnail.save("{temp_id}_thumbnail.png", File(open(output_thumbnail_location, "rb")))

    # Update statuses
    if video.status == "PENDING" or video.status == "INVALID":
        video.status = "PROCESSED"
    video.save()

    # Cleanup
    subprocess.call(["rm", output_video_location])
    subprocess.call(["rm", output_thumbnail_location])
    subprocess.call(["rm", input_video_location])
