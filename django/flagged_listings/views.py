from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from user_profile.models import Profile


def _flagged_queryset():
    return (
        Profile.objects.filter(user_type="sublettor", has_onboarded=True)
        .filter(
            Q(preferred_location__gt="")
            | (Q(listing_image__isnull=False) & ~Q(listing_image="")),
        )
        .select_related("user")
        .order_by("-id")
    )


def explore_flagged_listings(request):
    profiles = _flagged_queryset()

    q = (request.GET.get("q") or "").strip()
    if q:
        profiles = profiles.filter(preferred_location__icontains=q)

    max_rent = (request.GET.get("max_rent") or "").strip()
    if max_rent.isdigit():
        profiles = profiles.filter(min_monthly_rent__lte=int(max_rent))

    date_from = (request.GET.get("date_from") or "").strip()
    if date_from:
        profiles = profiles.filter(rent_end_date__gte=date_from)

    date_to = (request.GET.get("date_to") or "").strip()
    if date_to:
        profiles = profiles.filter(rent_start_date__lte=date_to)

    no_smoking = request.GET.get("no_smoking") == "yes"
    no_pets = request.GET.get("no_pets") == "yes"
    no_doubles = request.GET.get("no_doubles") == "yes"
    no_mixed_gender = request.GET.get("no_mixed_gender") == "yes"

    if no_smoking:
        profiles = profiles.filter(okay_smoking="no")
    if no_pets:
        profiles = profiles.filter(okay_pets="no")
    if no_doubles:
        profiles = profiles.filter(share_double="no")
    if no_mixed_gender:
        profiles = profiles.filter(live_opposite_sex="no")
        viewer_gender = None
        if request.user.is_authenticated:
            try:
                viewer_gender = request.user.profile.gender
            except Exception:
                pass
        if viewer_gender and viewer_gender not in ("prefer_not_to_say", ""):
            profiles = profiles.filter(gender=viewer_gender)

    checkbox_filters = {
        "no_smoking": no_smoking,
        "no_pets": no_pets,
        "no_doubles": no_doubles,
        "no_mixed_gender": no_mixed_gender,
    }

    return render(
        request,
        "flagged_listings/explore_flagged_listings.html",
        {
            "profiles": profiles,
            "search_query": q,
            "filters": {
                "max_rent": max_rent,
                "date_from": date_from,
                "date_to": date_to,
                **checkbox_filters,
            },
        },
    )


def flagged_listings_detail(request, pk):
    profile = get_object_or_404(_flagged_queryset(), pk=pk)
    other_listings = list(_flagged_queryset().exclude(pk=profile.pk)[:3])
    return render(
        request,
        "flagged_listings/flagged_listings_detail.html",
        {
            "profile": profile,
            "other_listings": other_listings,
        },
    )
