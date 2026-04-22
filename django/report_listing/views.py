from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import ListingReport
from user_profile.models import Profile


@login_required
def report_listing_form(request, listing_id):
    """Report form page for a specific listing profile."""
    profile = get_object_or_404(Profile, pk=listing_id)

    if request.method == "POST":
        ListingReport.objects.create(
            reported_listing=profile,
            reporter=request.user,
            reason=request.POST.get("reason", "").strip(),
            speed=request.POST.get("speed", "normal"),
        )
        return redirect("report_listing:report-listing-thank-you")

    return render(
        request,
        "report_listing/report_listing.html",
        {
            "profile": profile,
        },
    )


@login_required
def report_listing_thank_you(request):
    """Confirmation page shown after listing report submission."""
    return render(request, "report_listing/report_listing_thank_you.html")
