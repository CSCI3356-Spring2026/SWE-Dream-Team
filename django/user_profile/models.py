from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Shown on the profile card (if empty, you can use User first/last name in templates).",
    )
    instagram = models.CharField(
        max_length=100,
        blank=True,
        help_text="Handle (e.g. billyrulez) or full URL.",
    )
    school = models.CharField(max_length=120, blank=True)
    year = models.CharField(max_length=50, blank=True)
    major = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    outreach_preference = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    contact_email = models.EmailField(blank=True)
    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True,
        help_text="Profile picture (requires Pillow installed).",
    )

    def __str__(self):
        if self.name:
            return f"Profile: {self.name}"
        return f"Profile: {self.user.get_username()}"
