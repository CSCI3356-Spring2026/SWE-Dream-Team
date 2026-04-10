from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ("user", "user_type", "has_onboarded", "grad_year")
	list_filter = ("user_type", "has_onboarded", "grad_year")
	search_fields = ("user__username", "user__email", "major_minor", "bio")
