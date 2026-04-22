from django.conf import settings
from django.db import models


class UserReport(models.Model):
	SPEED_CHOICES = [
		("asap", "As fast as possible"),
		("fast", "Fast"),
		("normal", "Normal"),
		("less_than_normal", "Less than normal"),
		("no_rush", "No Rush"),
	]

	reported_user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="user_reports_received",
	)
	reporter = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="user_reports_submitted",
	)
	reason = models.TextField(blank=True)
	speed = models.CharField(max_length=32, choices=SPEED_CHOICES, default="normal")
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"UserReport(reported_user={self.reported_user_id}, speed={self.speed})"
