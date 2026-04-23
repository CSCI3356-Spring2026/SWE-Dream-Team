from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from user_profile.models import Profile
from .models import Report, REPORT_TYPE_CHOICES


@login_required
def report_form(request, report_type, profile_id):
    """Shared report form for both user profiles and listings."""
    valid_types = {key for key, _ in REPORT_TYPE_CHOICES}
    if report_type not in valid_types:
        return redirect("home")

    profile = get_object_or_404(Profile, pk=profile_id)

    if profile.user == request.user:
        return redirect("home")

    if request.method == "POST":
        Report.objects.create(
            reported_profile=profile,
            reporter=request.user,
            report_type=report_type,
            reason=request.POST.get("reason", "").strip(),
            speed=request.POST.get("speed", "normal"),
        )
        return redirect("report_user:report-thank-you")

    return render(request, "report_user/report.html", {
        "profile": profile,
        "report_type": report_type,
    })


@login_required
def report_thank_you(request):
    """Confirmation page shown after any report submission."""
    return render(request, "report_user/report_thank_you.html")