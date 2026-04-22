from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import UserReport
from user_profile.models import Profile


@login_required
def report_user_form(request, user_id):
    """Report form page for a specific user profile."""
    user = get_object_or_404(get_user_model(), pk=user_id)
    profile = get_object_or_404(Profile, user=user)

    if user == request.user:
        return redirect("profile-public-by-user", request.user.id)

    if request.method == "POST":
        UserReport.objects.create(
            reported_user=user,
            reporter=request.user,
            reason=request.POST.get("reason", "").strip(),
            speed=request.POST.get("speed", "normal"),
        )
        return redirect("report_user:report-user-thank-you")

    return render(
        request,
        "report_user/report_user.html",
        {
            "profile": profile,
        },
    )


@login_required
def report_user_thank_you(request):
    """Confirmation page shown after report submission."""
    return render(request, "report_user/report_user_thank_you.html")
