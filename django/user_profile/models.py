from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

GENDER_CHOICES = [
        ('man', 'Man'),
        ('woman', 'Woman'),
        ('non_binary', 'Non-binary'),
        ('genderqueer', 'Genderqueer / Gender-fluid'),
        ('agender', 'Agender'),
        ('self_describe', 'A gender not listed (Self-describe)'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]      

OUTREACH_OPTIONS = [
        ('phone', 'Phone'),
        ('instagram', 'Instagram'),
        ('email', 'Email'),
    ]

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    
    has_onboarded = models.BooleanField(default=False)

    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default='prefer_not_to_say',
    )
    
    gender_self_described = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="If you selected 'A gender not listed', please specify here."
    )


    major_minor = models.CharField(max_length=120, blank=True)

    grad_year = models.CharField(max_length=50, blank=True)

    # insta, phone, or email
    outreach_preference = models.CharField(
        max_length=20,
        choices=OUTREACH_OPTIONS,
        blank=True,
        default='email' 
    )

    instagram = models.CharField(
        max_length=100,
        blank=True,
        help_text="Handle (e.g. billyrulez) or full URL.",
    )

    phone = models.CharField(max_length=30, blank=True)

    bio = models.TextField(blank=True)
    
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
