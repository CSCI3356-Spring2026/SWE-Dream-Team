from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from user_profile.models import Profile


@login_required
def profile_card_preview(request):
    """Serves the profile card template for the logged-in user."""
    profile = get_object_or_404(Profile, user=request.user)
    return render(
        request,
        "user_profile/profile.html",
        {
            "profile": profile,
        },
    )


def public_profile_by_user(request, user_id):
    """Read-only profile for a listing owner (lessor / sublettor)."""
    user = get_object_or_404(get_user_model(), pk=user_id)
    profile = get_object_or_404(Profile, user=user)
    return render(
        request,
        "user_profile/profile.html",
        {
            "profile": profile,
        },
    )


def profile_detail(request, pk):
    """Backward-compatible profile detail route by Profile primary key."""
    profile = get_object_or_404(Profile, pk=pk)
    return render(
        request,
        "user_profile/profile.html",
        {
            "profile": profile,
        },
    )


@require_POST
@login_required
def toggle_ban(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    profile = get_object_or_404(Profile, pk=pk)
    profile.banned = not profile.banned
    profile.save()
    return redirect(request.POST.get("next", "/"))


@require_POST
@login_required
def toggle_hidden(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    profile = get_object_or_404(Profile, pk=pk)
    profile.hidden = not profile.hidden
    profile.save()
    return redirect(request.POST.get("next", "/"))
