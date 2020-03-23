from django.core.signing import TimestampSigner
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from core.models import User


def authkey_middleware(get_response):
    signer = TimestampSigner()

    def middleware(request):
        ak = request.GET.get("ak", None)
        if ak != None:
            try:
                username = signer.unsign(ak, max_age=72 * 24 * 60 * 60)
                user = User.objects.filter(username=username).first()
                if request.user != user:
                    if not user.verified_email:
                        user.verified_email = True
                        user.save()
                        messages.success(
                            request,
                            "Your email address has been successfully verified.",
                        )
                    messages.success(
                        request,
                        f"You've been logged in as {user.email}. You're good to go."
                    )
                    login(request, user)
            except:
                if not request.user.is_authenticated:
                    messages.warning(
                        request,
                        "We weren't able to sign you in using the link in the email. It was probably sent too long ago.",
                    )
        return get_response(request)

    return middleware
