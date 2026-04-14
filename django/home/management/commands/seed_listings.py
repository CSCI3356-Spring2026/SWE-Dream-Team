"""
Management command to seed fake sublettor listings for filter testing.

Usage:
    python manage.py seed_listings          # creates 12 listings
    python manage.py seed_listings --count 20
    python manage.py seed_listings --clear  # delete all seeded listings first
"""

import random
from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from user_profile.models import Profile

User = get_user_model()

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

YES_NO = ["yes", "no"]
GENDERS = ["man", "woman", "non_binary", "prefer_not_to_say"]


class Command(BaseCommand):
    help = "Seed fake sublettor listings for filter testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=12,
            help="Number of fake listings to create (default: 12)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all previously seeded listings before creating new ones",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = User.objects.filter(username__startswith="seed_listing_").delete()
            self.stdout.write(self.style.WARNING(f"Cleared {deleted} seeded users/profiles."))

        count = options["count"]
        created = 0

        for i in range(count):
            username = f"seed_listing_{random.randint(100000, 999999)}"
            while User.objects.filter(username=username).exists():
                username = f"seed_listing_{random.randint(100000, 999999)}"

            user = User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="testpass123",
                first_name=random.choice(["Alex", "Jordan", "Casey", "Morgan", "Taylor", "Riley", "Drew", "Quinn"]),
                last_name=random.choice(["Smith", "Johnson", "Lee", "Brown", "Davis", "Wilson", "Moore", "Taylor"]),
            )

            rent_start = date.today() + timedelta(days=random.randint(0, 60))
            rent_end = rent_start + timedelta(days=random.randint(60, 270))

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.user_type = "sublettor"
            profile.gender = random.choice(GENDERS)
            profile.preferred_location = random.choice(LOCATIONS)
            profile.min_monthly_rent = random.choice([800, 900, 1000, 1100, 1200, 1400, 1600, 1800, 2000])
            profile.rent_start_date = rent_start
            profile.rent_end_date = rent_end
            profile.roommate_match = round(random.uniform(40, 99), 1)
            profile.housing_match = round(random.uniform(40, 99), 1)
            profile.okay_smoking = random.choice(YES_NO)
            profile.okay_pets = random.choice(YES_NO)
            profile.share_double = random.choice(YES_NO)
            profile.live_opposite_sex = random.choice(YES_NO)
            profile.has_onboarded = True
            profile.save()

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} fake listings."))
        self.stdout.write("Log in as any seed user with password: testpass123")