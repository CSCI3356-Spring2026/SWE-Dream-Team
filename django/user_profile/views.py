from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
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
