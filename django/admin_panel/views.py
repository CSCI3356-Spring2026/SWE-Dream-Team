from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.shortcuts import render

from report_listing.models import ListingReport
from report_user.models import UserReport
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

	rows = []
	if mode == "users":
		reports = UserReport.objects.select_related("reported_user")
		if selected_speed != "all":
			reports = reports.filter(speed=selected_speed)

		for report in reports[:200]:
			reported_user = report.reported_user
			rows.append(
				{
					"name": reported_user.get_full_name() or reported_user.username,
					"link": reverse("profile-public-by-user", args=[reported_user.pk]),
					"speed": report.get_speed_display(),
					"reason": report.reason,
					"created_at": report.created_at,
				}
			)
	else:
		reports = ListingReport.objects.select_related("reported_listing__user")
		if selected_speed != "all":
			reports = reports.filter(speed=selected_speed)

		for report in reports[:200]:
			listing = report.reported_listing
			rows.append(
				{
					"name": listing.user.get_full_name() or listing.user.username,
					"link": reverse("listings-detail", args=[listing.pk]),
					"speed": report.get_speed_display(),
					"reason": report.reason,
					"created_at": report.created_at,
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
