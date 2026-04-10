from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

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
