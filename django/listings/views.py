from django.db.models import Q
from django.shortcuts import render

from user_profile.models import Profile


def explore_housing(request):
    """
    Public grid of sublettor listings backed by Profile rows
    (house location, listing photo, lease dates, match scores).
    """
    profiles = (
        Profile.objects.filter(user_type="sublettor")
        .filter(
            Q(preferred_location__gt="")
            | (Q(listing_image__isnull=False) & ~Q(listing_image="")),
        )
        .select_related("user")
        .order_by("-id")
    )

    q = (request.GET.get("q") or "").strip()
    if q:
        profiles = profiles.filter(preferred_location__icontains=q)

    return render(
        request,
        "listings/explore_housing.html",
        {"profiles": profiles, "search_query": q},
    )
