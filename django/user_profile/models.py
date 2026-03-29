from datetime import date

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

IDEAL_HOUSING_VIBE_CHOICES = [
    ('quiet_studious', 'Quiet & Studious'),
    ('chill_low_key', 'Chill & Low-Key'),
    ('social_balanced', 'Social but Balanced'),
    ('very_social', 'Very Social / Going Out Often'),
    ('independent', 'Independent / Keep to Myself'),
]

ROOMMATE_DEALBREAKER_CHOICES = [
    ('smoking', 'Smoking'),
    ('excessive_noise', 'Excessive noise / loud late at night'),
    ('messiness', 'Messiness / unclean common areas'),
    ('guests_frequent', 'Having guests over frequently'),
    ('significant_other_guest', 'Significant other as guest'),
    ('strong_odors', 'Strong odors (weed, food, etc.)'),
    ('sleep_schedules', 'Different sleep schedules'),
    ('pets', 'Pets in the house'),
    ('drug_use', 'Drug use'),
    ('alcohol_use', 'Alcohol use'),
]

CLEANLINESS_CHOICES = [
    ('very_messy', 'Very messy'),
    ('somewhat_messy', 'Somewhat messy'),
    ('neutral', 'Neutral'),
    ('somewhat_clean', 'Somewhat clean'),
    ('very_clean', 'Very clean'),
]

BEDTIME_CHOICES = [
    ('20:00', '8:00 PM'),
    ('21:00', '9:00 PM'),
    ('22:00', '10:00 PM'),
    ('23:00', '11:00 PM'),
    ('00:00', '12:00 AM (midnight)'),
    ('01:00', '1:00 AM'),
    ('02:00', '2:00 AM'),
]

SOCIAL_LEVEL_CHOICES = [
    ('very_social', 'Very social'),
    ('moderately_social', 'Moderately social'),
    ('balanced', 'Balanced'),
    ('mostly_independent', 'Mostly independent'),
    ('extremely_independent', 'Extremely independent'),
]

YES_NO_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
]

LAUNDRY_CHOICES = [
    ('in_unit', 'In unit'),
    ('in_building', 'In building'),
    ('doesnt_matter', "Doesn't matter"),
]

UTILITIES_CHOICES = [
    ('included', 'Included'),
    ('not_included', 'Not included'),
]

USER_TYPE_CHOICES = [
    ('renter', 'Renter'),
    ('sublettor', 'Sublettor'),
]


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='renter',
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

    ideal_housing_vibe = models.CharField(
        max_length=32,
        choices=IDEAL_HOUSING_VIBE_CHOICES,
        default='quiet_studious',
    )
    roommate_dealbreakers = models.JSONField(default=list, blank=True)
    cleanliness = models.CharField(
        max_length=32,
        choices=CLEANLINESS_CHOICES,
        default='neutral',
    )
    weekend_bedtime = models.CharField(
        max_length=5,
        choices=BEDTIME_CHOICES,
        default='23:00',
    )
    weeknight_bedtime = models.CharField(
        max_length=5,
        choices=BEDTIME_CHOICES,
        default='23:00',
    )
    social_level = models.CharField(
        max_length=32,
        choices=SOCIAL_LEVEL_CHOICES,
        default='balanced',
    )
    live_opposite_sex = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    share_double = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    okay_smoking = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    okay_alcohol = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    okay_overnight = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    okay_pets = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )

    preferred_location = models.CharField(max_length=255, default='')
    walking_time_minutes = models.PositiveIntegerField(default=0)
    rent_start_date = models.DateField(default=date(2025, 9, 1))
    rent_end_date = models.DateField(default=date(2026, 5, 1))
    min_monthly_rent = models.PositiveIntegerField(default=0)
    dishwasher = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    laundry = models.CharField(
        max_length=20,
        choices=LAUNDRY_CHOICES,
        default='doesnt_matter',
    )
    utilities = models.CharField(
        max_length=20,
        choices=UTILITIES_CHOICES,
        default='included',
    )
    parking_needed = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )
    already_furnished = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        default='no',
    )

    def __str__(self):
        return f"Profile: {self.user.get_username()}"
