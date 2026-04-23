from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from report_user.models import Report
from user_profile.models import Profile

def _listing_queryset():
    return (
        Profile.objects.filter(user_type="sublettor", has_onboarded=True, banned=False, hidden=False)
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

    max_rent = (request.GET.get("max_rent") or "").strip()
    if max_rent.isdigit():
        profiles = profiles.filter(min_monthly_rent__lte=int(max_rent))

    date_from = (request.GET.get("date_from") or "").strip()
    if date_from:
        profiles = profiles.filter(rent_end_date__gte=date_from)

    date_to = (request.GET.get("date_to") or "").strip()
    if date_to:
        profiles = profiles.filter(rent_start_date__lte=date_to)

    # Inverted checkbox filters — checking means "exclude" the trait
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
        # Also match the viewer's gender so only same-gender listings appear
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
        "listings/explore_housing.html",
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


def _sublettor_queryset():
    return (
        Profile.objects.filter(user_type="sublettor", has_onboarded=True, banned=False, hidden=False)
        .filter(
            Q(preferred_location__gt="")
            | (Q(listing_image__isnull=False) & ~Q(listing_image=""))
        )
        .select_related("user")
        .order_by("-id")
    )


def listing_detail(request, pk):
    """Single listing: image, location, lease, amenities, matches, related listings."""
    qs = Profile.objects.filter(user_type="sublettor", has_onboarded=True) if request.user.is_staff else _listing_queryset()
    profile = get_object_or_404(qs, pk=pk)
    other_listings = list(_listing_queryset().exclude(pk=profile.pk)[:3])

    report = None
    if request.user.is_staff:
        report_id = request.GET.get("report")
        if report_id:
            report = Report.objects.filter(pk=report_id, reported_profile=profile).first()

    return render(
        request,
        "listings/listing_detail.html",
        {
            "profile": profile,
            "other_listings": other_listings,
            "report": report,
        },
    )
