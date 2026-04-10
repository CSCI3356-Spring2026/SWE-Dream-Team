from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from google.auth.transport import requests
from google.oauth2 import id_token


# user specific
from django.contrib.auth import login
from django.contrib.auth.models import User
from user_profile.models import Profile


def _build_unique_username(email: str, fallback_seed: str) -> str:
    base = (email.split("@", 1)[0] or fallback_seed or "google_user").strip()
    candidate = base[:150]
    suffix = 1
    while User.objects.filter(username=candidate).exists():
        suffix_str = str(suffix)
        candidate = f"{base[:150-len(suffix_str)-1]}_{suffix_str}"
        suffix += 1
    return candidate

def landing(request):
    return render(
        request,
        "landing_page/landing.html",
        {
            "google_oauth_client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "auth_receiver_url": request.build_absolute_uri("/auth-receiver"),
        },
    )


@csrf_exempt
def auth_receiver(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    token = request.POST.get("credential")
    if not token:
        return HttpResponse(status=400)

    if not settings.GOOGLE_OAUTH_CLIENT_ID:
        return HttpResponse("GOOGLE_OAUTH_CLIENT_ID is not configured.", status=500)

    try:
        user_data = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
        )
    except ValueError:
        return HttpResponse(status=403)

    request.session["user_data"] = user_data

    email = (user_data.get("email") or "").strip().lower()
    hosted_domain = (user_data.get("hd") or "").strip().lower()
    allowed_domain = getattr(settings, "GOOGLE_ALLOWED_DOMAIN", "bc.edu")
    admin_emails = set(getattr(settings, "ADMIN_PANEL_EMAILS", []))
    first_name = user_data.get('given_name', '')
    last_name = user_data.get('family_name', '')

    if not email:
        return HttpResponse("Google account email is required.", status=400)

    if not user_data.get("email_verified", False):
        return HttpResponse("Google account email must be verified.", status=403)

    email_domain = email.rsplit("@", 1)[-1]
    if email_domain != allowed_domain:
        return HttpResponse(f"Only @{allowed_domain} accounts are allowed.", status=403)

    if hosted_domain and hosted_domain != allowed_domain:
        return HttpResponse(f"Only @{allowed_domain} accounts are allowed.", status=403)

    # Multiple local users may share one email in legacy data.
    # Prefer superusers/staff first so admin accounts keep admin access.
    matching_users = list(User.objects.filter(email__iexact=email))
    user = None
    if matching_users:
        user = sorted(
            matching_users,
            key=lambda account: (
                not account.is_superuser,
                not account.is_staff,
                account.id,
            ),
        )[0]
    if user is None:
        username = _build_unique_username(email=email, fallback_seed=user_data.get("sub", "google"))
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=email in admin_emails,
        )
    else:
        updates = []
        if first_name and user.first_name != first_name:
            user.first_name = first_name
            updates.append("first_name")
        if last_name and user.last_name != last_name:
            user.last_name = last_name
            updates.append("last_name")
        if email in admin_emails and not user.is_staff:
            user.is_staff = True
            updates.append("is_staff")
        if updates:
            user.save(update_fields=updates)

    profile, p_created = Profile.objects.get_or_create(user=user)

    # login user in django session

    login(request, user)

    request.session["google_picture"] = user_data.get("picture")

    return redirect("home")


def sign_out(request):
    request.session.pop("user_data", None)
    request.session.flush()
    return redirect("landing")

