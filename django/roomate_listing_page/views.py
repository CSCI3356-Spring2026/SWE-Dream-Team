from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from user_profile.matching import (
    attach_pairwise_to_profiles,
    pairwise_housing_score,
    pairwise_roommate_score,
    sort_profiles_by_pairwise,
    viewer_profile_for_pairwise,
)
from user_profile.models import Profile


def _renter_queryset():
    return (
        Profile.objects.filter(user_type="renter", has_onboarded=True)
        .select_related("user")
        .order_by("-id")
    )


def explore_roommates(request):
    """
    Grid of renter profiles for sublettors (name, BC + grad year, major, matches).
    """
    profiles = _renter_queryset()

    q = (request.GET.get("q") or "").strip()
    if q:
        profiles = profiles.filter(
            Q(user__username__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(major_minor__icontains=q)
            | Q(grad_year__icontains=q),
        )

    checkbox_fields = ["live_opposite_sex", "share_double", "okay_smoking", "okay_pets"]
    checkbox_filters = {}
    for field in checkbox_fields:
        if request.GET.get(field) == "yes":
            profiles = profiles.filter(**{field: "yes"})
            checkbox_filters[field] = True
        else:
            checkbox_filters[field] = False

    profile_rows = list(profiles)
    seeker = viewer_profile_for_pairwise(request.user)
    profile_rows = sort_profiles_by_pairwise(profile_rows, seeker)

    return render(
        request,
        "roomate_listing_page/explore_roommates.html",
        {
            "profiles": profile_rows,
            "search_query": q,
            "filters": checkbox_filters,
        },
    )


def roommate_detail(request, pk):
    """Single renter profile for sublettors; related renters at bottom."""
    profile = get_object_or_404(_renter_queryset(), pk=pk)
    other_roommates = list(_renter_queryset().exclude(pk=profile.pk)[:3])

    seeker = viewer_profile_for_pairwise(request.user)
    if seeker:
        profile.pairwise_roommate_score = pairwise_roommate_score(seeker, profile)
        profile.pairwise_housing_score = pairwise_housing_score(seeker, profile)
    else:
        profile.pairwise_roommate_score = None
        profile.pairwise_housing_score = None
    attach_pairwise_to_profiles(other_roommates, seeker)

    return render(
        request,
        "roomate_listing_page/roommate_detail.html",
        {
            "profile": profile,
            "other_roommates": other_roommates,
        },
    )
