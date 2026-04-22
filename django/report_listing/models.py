from django.conf import settings
from django.db import models

from user_profile.models import Profile


class ListingReport(models.Model):
	SPEED_CHOICES = [
		("asap", "As fast as possible"),
		("fast", "Fast"),
		("normal", "Normal"),
		("less_than_normal", "Less than normal"),
		("no_rush", "No Rush"),
	]

	reported_listing = models.ForeignKey(
		Profile,
		on_delete=models.CASCADE,
		related_name="listing_reports_received",
	)
	reporter = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="listing_reports_submitted",
	)
	reason = models.TextField(blank=True)
	speed = models.CharField(max_length=32, choices=SPEED_CHOICES, default="normal")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"ListingReport(listing={self.reported_listing_id}, speed={self.speed})"
