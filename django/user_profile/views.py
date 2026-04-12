<<<<<<< HEAD
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Profile
=======
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
>>>>>>> listing_individual_card

def profile_card_preview(request):
    """Serves the profile card template for local preview."""
    roommate_match = 9.5
    housing_match = 9.5
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if profile is not None:
            roommate_match = profile.roommate_match
            housing_match = profile.housing_match

    profile = get_object_or_404(Profile, user=request.user)
    return render(
        request,
        "user_profile/profile.html",
        {
            "roommate_match": roommate_match,
            "housing_match": housing_match,
            "profile": profile,
        },
    )

<<<<<<< HEAD
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

=======

def public_profile_by_user(request, user_id):
    """Read-only profile for a listing owner (lessor / sublettor)."""
    user = get_object_or_404(get_user_model(), pk=user_id)
    profile = get_object_or_404(Profile, user=user)
>>>>>>> listing_individual_card
    return render(
        request,
        "user_profile/profile.html",
        {
<<<<<<< HEAD
            "profile": profile,
        },
    )
=======
            "roommate_match": profile.roommate_match,
            "housing_match": profile.housing_match,
            "profile": profile,
        },
    )
>>>>>>> listing_individual_card
