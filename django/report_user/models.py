from django.conf import settings
from django.db import models

from user_profile.models import Profile

SPEED_CHOICES = [
	("asap", "As fast as possible"),
	("fast", "Fast"),
	("normal", "Normal"),
	("less_than_normal", "Less than normal"),
	("no_rush", "No Rush"),
]

REPORT_TYPE_CHOICES = [
	("profile", "Profile"),
	("listing", "Listing"),
]


class Report(models.Model):
	reported_profile = models.ForeignKey(
		Profile,
		on_delete=models.CASCADE,
		related_name="reports_received",
	)
	reporter = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="reports_submitted",
	)
	report_type = models.CharField(
		max_length=10,
		choices=REPORT_TYPE_CHOICES,
		default="profile",
	)
	reason = models.TextField(blank=True, max_length=300)
	speed = models.CharField(max_length=32, choices=SPEED_CHOICES, default="normal")
	created_at = models.DateTimeField(auto_now_add=True)
	archived = models.BooleanField(default=False, editable=False)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Report({self.report_type}, profile={self.reported_profile_id}, speed={self.speed})"
