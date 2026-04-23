from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from report_user.models import Report
from user_profile.models import Profile


def _get_report_context(request, profile):
    """Return a report from ?report=<id> if the user is staff and it belongs to this profile."""
    if not request.user.is_staff:
        return None
    report_id = request.GET.get("report")
    if not report_id:
        return None
    return Report.objects.filter(pk=report_id, reported_profile=profile).first()


@login_required
def profile_card_preview(request):
    """Serves the profile card template for the logged-in user."""
    profile = get_object_or_404(Profile, user=request.user)
    return render(
        request,
        "user_profile/profile.html",
        {
            "profile": profile,
        },
    )


def public_profile_by_user(request, user_id):
    """Read-only profile for a listing owner (lessor / sublettor)."""
    user = get_object_or_404(get_user_model(), pk=user_id)
    qs = Profile.objects if request.user.is_staff else Profile.objects.filter(banned=False)
    profile = get_object_or_404(qs, user=user)
    return render(request, "user_profile/profile.html", {
        "profile": profile,
        "report": _get_report_context(request, profile),
    })


def profile_detail(request, pk):
    """Backward-compatible profile detail route by Profile primary key."""
    qs = Profile.objects if request.user.is_staff else Profile.objects.filter(banned=False)
    profile = get_object_or_404(qs, pk=pk)
    return render(request, "user_profile/profile.html", {
        "profile": profile,
        "report": _get_report_context(request, profile),
    })


@require_POST
@login_required
def toggle_ban(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    profile = get_object_or_404(Profile, pk=pk)
    profile.banned = not profile.banned
    profile.hidden = profile.banned
    profile.save()
    return redirect(request.POST.get("next", "/"))


@require_POST
@login_required
def dismiss_report(request, report_pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    report = get_object_or_404(Report, pk=report_pk)
    profile = report.reported_profile
    report.delete()
    if not Report.objects.filter(reported_profile=profile).exists():
        profile.hidden = False
        profile.save()
    return redirect(request.POST.get("next", "/"))


@require_POST
@login_required
def toggle_hidden(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    profile = get_object_or_404(Profile, pk=pk)
    profile.hidden = not profile.hidden
    profile.save()
    return redirect(request.POST.get("next", "/"))
