from celery import shared_task
from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string
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

