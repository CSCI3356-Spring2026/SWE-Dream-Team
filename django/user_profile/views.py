from django.shortcuts import render

from .models import Profile


def profile_card_preview(request):
    """Serves the profile card template for local preview."""
    # Demo scores when not logged in; logged-in users use DB (— if unset)
    roommate_match = 9.5
    housing_match = 9.5
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile is not None:
            roommate_match = profile.roommate_match
            housing_match = profile.housing_match
    return render(
        request,
        "user_profile/profile.html",
        {
            "roommate_match": roommate_match,
            "housing_match": housing_match,
        },
    )
