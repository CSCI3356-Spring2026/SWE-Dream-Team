from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from user_profile.matching import (
    attach_pairwise_to_profiles,
    pairwise_housing_score,
    pairwise_roommate_score,
    sort_profiles_by_pairwise,
    viewer_profile_for_pairwise,
)
from user_profile.models import Profile

User = get_user_model()


def _user(name: str) -> User:
    return User.objects.create_user(username=name, email=f"{name}@test.edu", password="x")


def _base_profile(user: User, **kwargs) -> Profile:
    defaults = {
        "user_type": "renter",
        "has_onboarded": True,
        "gender": "prefer_not_to_say",
        "major_minor": "CS",
        "grad_year": "2027",
        "outreach_preference": "email",
        "instagram": "x",
        "phone": "555",
        "bio": "hi",
        "ideal_housing_vibe": "quiet_studious",
        "roommate_dealbreakers": ["messiness"],
        "cleanliness": "neutral",
        "weekend_bedtime": "23:00",
        "weeknight_bedtime": "23:00",
        "social_level": "balanced",
        "live_opposite_sex": "no",
        "share_double": "no",
        "okay_smoking": "no",
        "okay_alcohol": "no",
        "okay_overnight": "no",
        "okay_pets": "no",
        "preferred_location": "Brighton MA",
        "walking_time_minutes": 15,
        "min_monthly_rent": 1200,
        "rent_start_date": date(2025, 9, 1),
        "rent_end_date": date(2026, 5, 1),
        "dishwasher": "no",
        "laundry": "doesnt_matter",
        "utilities": "included",
        "parking_needed": "no",
        "already_furnished": "no",
    }
    defaults.update(kwargs)
    p, _ = Profile.objects.update_or_create(user=user, defaults=defaults)
    return p


class PairwiseMatchingTests(TestCase):
    def test_similar_profiles_high_roommate_score(self):
        u1, u2 = _user("a1"), _user("a2")
        s = _base_profile(u1, roommate_dealbreakers=["messiness"])
        c = _base_profile(u2, roommate_dealbreakers=["messiness"])
        score = pairwise_roommate_score(s, c)
        self.assertGreaterEqual(score, Decimal("8.0"))

    def test_smoking_dealbreaker_vs_smoking_allowed_lowers_roommate(self):
        u1, u2 = _user("b1"), _user("b2")
        s = _base_profile(u1, roommate_dealbreakers=["smoking"], okay_smoking="no")
        c = _base_profile(u2, okay_smoking="yes")
        low = pairwise_roommate_score(s, c)
        c2 = _base_profile(_user("b3"), okay_smoking="no")
        high = pairwise_roommate_score(s, c2)
        self.assertGreater(high, low)

    def test_non_overlapping_lease_lowers_housing(self):
        u1, u2 = _user("c1"), _user("c2")
        s = _base_profile(
            u1,
            rent_start_date=date(2026, 1, 1),
            rent_end_date=date(2026, 5, 1),
            min_monthly_rent=2000,
        )
        c_overlap = _base_profile(
            u2,
            rent_start_date=date(2026, 2, 1),
            rent_end_date=date(2026, 4, 1),
            min_monthly_rent=1500,
        )
        c_gap = _base_profile(
            _user("c3"),
            rent_start_date=date(2027, 1, 1),
            rent_end_date=date(2027, 5, 1),
            min_monthly_rent=1500,
        )
        self.assertGreater(
            pairwise_housing_score(s, c_overlap),
            pairwise_housing_score(s, c_gap),
        )

    def test_asking_rent_above_target_lowers_housing(self):
        u1, u2 = _user("d1"), _user("d2")
        s = _base_profile(u1, min_monthly_rent=1000)
        cheap = _base_profile(u2, min_monthly_rent=900)
        pricey = _base_profile(_user("d3"), min_monthly_rent=2500)
        self.assertGreater(pairwise_housing_score(s, cheap), pairwise_housing_score(s, pricey))

    def test_attach_pairwise_none_seeker_sets_nulls(self):
        u = _user("e1")
        p = _base_profile(u)
        lst = [p]
        attach_pairwise_to_profiles(lst, None)
        self.assertIsNone(p.pairwise_roommate_score)
        self.assertIsNone(p.pairwise_housing_score)

    def test_sort_by_average_descending(self):
        seeker_user = _user("f_seek")
        seeker = _base_profile(seeker_user, min_monthly_rent=2000)

        good_user = _user("f_good")
        good = _base_profile(
            good_user,
            min_monthly_rent=1000,
            okay_smoking="no",
            preferred_location="Brighton MA",
            rent_start_date=seeker.rent_start_date,
            rent_end_date=seeker.rent_end_date,
        )

        bad_user = _user("f_bad")
        bad = _base_profile(
            bad_user,
            min_monthly_rent=5000,
            okay_smoking="yes",
            preferred_location="Elsewhere",
            rent_start_date=date(2028, 1, 1),
            rent_end_date=date(2028, 5, 1),
        )

        seeker.roommate_dealbreakers = ["smoking"]
        seeker.save(update_fields=["roommate_dealbreakers"])

        ordered = sort_profiles_by_pairwise([bad, good], seeker)
        self.assertEqual(ordered[0].pk, good.pk)
        self.assertEqual(ordered[1].pk, bad.pk)


class ViewerProfileForPairwiseTests(TestCase):
    def test_anonymous_user_returns_none(self):
        from django.contrib.auth.models import AnonymousUser

        req_user = AnonymousUser()
        self.assertIsNone(viewer_profile_for_pairwise(req_user))

    def test_authenticated_without_profile_returns_none(self):
        u = _user("g1")
        self.assertIsNone(viewer_profile_for_pairwise(u))

    def test_onboarded_user_returns_profile(self):
        u = _user("g2")
        p = _base_profile(u, has_onboarded=True)
        self.assertEqual(viewer_profile_for_pairwise(u), p)

    def test_not_onboarded_returns_none(self):
        u = _user("g3")
        _base_profile(u, has_onboarded=False)
        self.assertIsNone(viewer_profile_for_pairwise(u))
