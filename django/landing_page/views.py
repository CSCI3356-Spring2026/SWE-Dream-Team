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

    email = user_data.get('email')
    first_name = user_data.get('given_name', '')
    last_name = user_data.get('family_name', '')
    
    # generate user username if needed in future
    user, created = User.objects.get_or_create(
        email=email,
        defaults={'username': email, 'first_name': first_name, 'last_name': last_name}
    )

    profile, p_created = Profile.objects.get_or_create(user=user)

    # login user in django session

    login(request, user)

    request.session["google_picture"] = user_data.get("picture")

    return redirect("home")


def sign_out(request):
    request.session.pop("user_data", None)
    request.session.flush()
    return redirect("landing")

