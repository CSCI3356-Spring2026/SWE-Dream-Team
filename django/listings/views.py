from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from user_profile.models import Profile


def _listing_queryset():
    return (
        Profile.objects.filter(user_type="sublettor")
        .filter(
            Q(preferred_location__gt="")
            | (Q(listing_image__isnull=False) & ~Q(listing_image="")),
        )
        .select_related("user")
        .order_by("-id")
    )


def explore_housing(request):
    """
    Public grid of sublettor listings backed by Profile rows
    (house location, listing photo, lease dates, match scores).
    """
    profiles = _listing_queryset()

    q = (request.GET.get("q") or "").strip()
    if q:
        profiles = profiles.filter(preferred_location__icontains=q)

    return render(
        request,
        "listings/explore_housing.html",
        {"profiles": profiles, "search_query": q},
    )


def listing_detail(request, pk):
    """Single listing: image, location, lease, amenities, matches, related listings."""
    profile = get_object_or_404(
        _listing_queryset(),
        pk=pk,
    )

    other_listings = list(
        _listing_queryset().exclude(pk=profile.pk)[:3],
    )

    return render(
        request,
        "listings/listing_detail.html",
        {
            "profile": profile,
            "other_listings": other_listings,
        },
    )
