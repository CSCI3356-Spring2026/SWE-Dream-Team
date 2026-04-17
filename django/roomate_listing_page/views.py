from django.db.models import Q
from django.shortcuts import get_object_or_404, render

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

    return render(
        request,
        "roomate_listing_page/explore_roommates.html",
        {
            "profiles": profiles,
            "search_query": q,
            "filters": checkbox_filters,
        },
    )


def roommate_detail(request, pk):
    """Single renter profile for sublettors; related renters at bottom."""
    profile = get_object_or_404(_renter_queryset(), pk=pk)
    other_roommates = list(_renter_queryset().exclude(pk=profile.pk)[:3])

    return render(
        request,
        "roomate_listing_page/roommate_detail.html",
        {
            "profile": profile,
            "other_roommates": other_roommates,
        },
    )
