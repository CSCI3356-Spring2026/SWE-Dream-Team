"""
Management command to seed fake user profiles for testing.
Half are renters, half are sublettors with listing data.

Usage:
    python manage.py seed_users          # creates 12 users
    python manage.py seed_users --count 20
    python manage.py seed_users --clear  # delete all seeded users first
"""

import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from user_profile.models import Profile

User = get_user_model()

FIRST_NAMES = ["Alex", "Jordan", "Casey", "Morgan", "Taylor", "Riley", "Drew", "Quinn",
               "Avery", "Skyler", "Jamie", "Reese", "Blake", "Sage", "Hayden", "Dakota"]
LAST_NAMES = ["Smith", "Johnson", "Lee", "Brown", "Davis", "Wilson", "Moore", "Taylor",
              "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Garcia", "Clark"]

MAJORS = [
    "Computer Science", "Economics", "Biology", "Psychology", "Finance",
    "Marketing", "Political Science", "English", "Nursing", "Data Science",
]

GRAD_YEARS = ["2026", "2027", "2028", "2029"]

LOCATIONS = [
    "123 Commonwealth Ave, Boston, MA",
    "45 Brighton Ave, Allston, MA",
    "88 Beacon St, Brookline, MA",
    "200 Chestnut Hill Ave, Brighton, MA",
    "10 Lake St, Brighton, MA",
    "77 Foster St, Brighton, MA",
    "34 Sutherland Rd, Brighton, MA",
    "5 Strathmore Rd, Brighton, MA",
    "91 Kelton St, Allston, MA",
    "300 Commonwealth Ave, Boston, MA",
    "15 Aspinwall Ave, Brookline, MA",
    "62 Dummer St, Brookline, MA",
]

BIOS = [
    "Looking for a clean and respectful roommate near campus.",
    "Early riser, keep things tidy, love cooking on weekends.",
    "Grad student, mostly quiet, happy to share common spaces.",
    "Social but respect personal space — let's make it work!",
    "Night owl, friendly, big fan of board games and good coffee.",
    "Low-key and independent. Just need a chill place to study.",
]

DEALBREAKER_OPTIONS = [
    "smoking", "excessive_noise", "messiness", "guests_frequent",
    "significant_other_guest", "strong_odors", "sleep_schedules", "pets",
    "drug_use", "alcohol_use",
]

YES_NO = ["yes", "no"]
GENDERS = ["man", "woman", "non_binary", "genderqueer", "agender", "prefer_not_to_say"]
VIBES = ["quiet_studious", "chill_low_key", "social_balanced", "very_social", "independent"]
CLEANLINESS = ["very_messy", "somewhat_messy", "neutral", "somewhat_clean", "very_clean"]
BEDTIMES = ["20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00"]
SOCIAL_LEVELS = ["very_social", "moderately_social", "balanced", "mostly_independent", "extremely_independent"]
LAUNDRY = ["in_unit", "in_building", "doesnt_matter"]
UTILITIES = ["included", "not_included"]
OUTREACH = ["phone", "instagram", "email"]
RENT_AMOUNTS = [800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000]


def _fill_common_fields(profile, username):
    rent_start = date.today() + timedelta(days=random.randint(0, 60))
    rent_end = rent_start + timedelta(days=random.randint(60, 270))

    profile.has_onboarded = True
    profile.gender = random.choice(GENDERS)
    profile.major_minor = random.choice(MAJORS)
    profile.grad_year = random.choice(GRAD_YEARS)
    profile.outreach_preference = random.choice(OUTREACH)
    profile.instagram = f"@{username}"
    profile.phone = f"617-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    profile.bio = random.choice(BIOS)
    profile.preferred_location = random.choice(LOCATIONS)
    profile.walking_time_minutes = random.choice([5, 10, 15, 20, 30])
    profile.min_monthly_rent = random.choice(RENT_AMOUNTS)
    profile.rent_start_date = rent_start
    profile.rent_end_date = rent_end
    profile.ideal_housing_vibe = random.choice(VIBES)
    profile.roommate_dealbreakers = random.sample(DEALBREAKER_OPTIONS, k=random.randint(0, 4))
    profile.cleanliness = random.choice(CLEANLINESS)
    profile.weekend_bedtime = random.choice(BEDTIMES)
    profile.weeknight_bedtime = random.choice(BEDTIMES)
    profile.social_level = random.choice(SOCIAL_LEVELS)
    profile.live_opposite_sex = random.choice(YES_NO)
    profile.share_double = random.choice(YES_NO)
    profile.okay_smoking = random.choice(YES_NO)
    profile.okay_alcohol = random.choice(YES_NO)
    profile.okay_overnight = random.choice(YES_NO)
    profile.okay_pets = random.choice(YES_NO)
    profile.dishwasher = random.choice(YES_NO)
    profile.laundry = random.choice(LAUNDRY)
    profile.utilities = random.choice(UTILITIES)
    profile.parking_needed = random.choice(YES_NO)
    profile.already_furnished = random.choice(YES_NO)
    profile.roommate_match = round(random.uniform(40, 99), 1)
    profile.housing_match = round(random.uniform(40, 99), 1)


class Command(BaseCommand):
    help = "Seed fake user profiles for testing (half renters, half sublettors)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=12,
            help="Number of fake users to create (default: 12)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all previously seeded users before creating new ones",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = User.objects.filter(username__startswith="seed_user_").delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted} seeded users/profiles."))
            return

        count = options["count"]
        renter_count = count // 2
        sublettor_count = count - renter_count
        created = 0

        for i in range(count):
            username = f"seed_user_{random.randint(100000, 999999)}"
            while User.objects.filter(username=username).exists():
                username = f"seed_user_{random.randint(100000, 999999)}"

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="testpass123",
                first_name=random.choice(FIRST_NAMES),
                last_name=random.choice(LAST_NAMES),
            )

            profile, _ = Profile.objects.get_or_create(user=user)
            _fill_common_fields(profile, username)
            profile.user_type = "renter" if i < renter_count else "sublettor"
            profile.save()

            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created} users ({renter_count} renters, {sublettor_count} sublettors)."
        ))
        self.stdout.write("Log in as any seed user with password: testpass123")
