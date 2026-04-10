from django.db.models import Q
from django.shortcuts import render

from user_profile.models import Profile


def explore_roommates(request):
    """
    Grid of renter profiles for sublettors (name, BC + grad year, major, matches).
    """
    profiles = (
        Profile.objects.filter(user_type="renter")
        .select_related("user")
        .order_by("-id")
    )

    q = (request.GET.get("q") or "").strip()
    if q:
        profiles = profiles.filter(
            Q(user__username__icontains=q)
            | Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(major_minor__icontains=q)
            | Q(grad_year__icontains=q),
        )

    return render(
        request,
        "roomate_listing_page/explore_roommates.html",
        {"profiles": profiles, "search_query": q},
    )
