from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

GENDER_CHOICES = [
        ('man', 'Man'),
        ('woman', 'Woman'),
        ('non_binary', 'Non-binary'),
        ('genderqueer', 'Genderqueer / Gender-fluid'),
        ('agender', 'Agender'),
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
    
    major_minor = models.CharField(max_length=120)

    grad_year = models.CharField(max_length=50)

    # insta, phone, or email
    outreach_preference = models.CharField(
        max_length=20,
        choices=OUTREACH_OPTIONS,
        default='email' 
    )

    instagram = models.CharField(
        max_length=100,
        help_text="Handle (e.g. billyrulez) or full URL.",
    )

    phone = models.CharField(max_length=30)

    bio = models.TextField()
    
    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=False,
        null=True,
        help_text="Profile picture (requires Pillow installed).",
    )

    roommate_match = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    housing_match = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
  

    def __str__(self):
        if self.name:
            return f"Profile: {self.name}"
        return f"Profile: {self.user.get_username()}"
