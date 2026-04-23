from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.shortcuts import render

from report_user.models import Report
from user_profile.models import Profile


staff_only = user_passes_test(lambda user: user.is_authenticated and user.is_staff, login_url="landing")


@staff_only
def dashboard(request):
	user_model = get_user_model()
	context = {
		"user_count": user_model.objects.count(),
		"profile_count": Profile.objects.count(),
		"onboarded_count": Profile.objects.filter(has_onboarded=True).count(),
		"image_count": Profile.objects.exclude(photo="").exclude(photo__isnull=True).count(),
	}
	return render(request, "admin_panel/dashboard.html", context)


@staff_only
def image_library(request):
	profiles = (
		Profile.objects.select_related("user")
		.exclude(photo="")
		.exclude(photo__isnull=True)
		.order_by("user__username")
	)
	return render(request, "admin_panel/image_library.html", {"profiles": profiles})


@staff_only
def reported_accounts(request):
	mode = request.GET.get("mode", "users")
	if mode not in {"users", "listings"}:
		mode = "users"

	selected_speed = request.GET.get("speed", "all")
	speed_choices = [
		("all", "All"),
		("asap", "As fast as possible"),
		("fast", "Fast"),
		("normal", "Normal"),
		("less_than_normal", "Less than normal"),
		("no_rush", "No Rush"),
	]
	valid_speeds = {choice[0] for choice in speed_choices}
	if selected_speed not in valid_speeds:
		selected_speed = "all"

	report_type = "profile" if mode == "users" else "listing"
	reports = Report.objects.filter(report_type=report_type).select_related("reported_profile__user", "reporter")
	if selected_speed != "all":
		reports = reports.filter(speed=selected_speed)

	rows = []
	for report in reports[:200]:
		profile = report.reported_profile
		base_link = (
			reverse("profile-public-by-user", args=[profile.user.pk])
			if mode == "users"
			else reverse("listings-detail", args=[profile.pk])
		)
		link = f"{base_link}?report={report.pk}"
		rows.append(
			{
				"name": profile.user.get_full_name() or profile.user.username,
				"link": link,
				"speed": report.get_speed_display(),
				"reason": report.reason,
				"created_at": report.created_at,
				"hidden": profile.hidden,
				"banned": profile.banned,
				"reporter_name": (report.reporter.get_full_name() or report.reporter.username) if report.reporter else "-",
				"reporter_link": reverse("profile-public-by-user", args=[report.reporter.pk]) if report.reporter else None,
			}
		)

	context = {
		"mode": mode,
		"rows": rows,
		"speed_choices": speed_choices,
		"selected_speed": selected_speed,
		"reported_label": "Reported Houses" if mode == "listings" else "Reported Roommates",
		"empty_label": "No reported houses match the current filter." if mode == "listings" else "No reported roommates match the current filter.",
	}
	return render(request, "admin_panel/reported_accounts.html", context)
