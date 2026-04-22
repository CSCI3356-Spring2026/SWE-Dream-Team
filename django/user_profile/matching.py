"""
Pairwise compatibility scores (0–10) between a seeker's Profile and a card Profile.

Used on explore_housing (renter seeker, sublettor cards) and explore_roommates
(sublettor seeker, renter cards). Weights are explicit constants for easy tuning.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from user_profile.models import (
    BEDTIME_CHOICES,
    CLEANLINESS_CHOICES,
    IDEAL_HOUSING_VIBE_CHOICES,
    Profile,
    SOCIAL_LEVEL_CHOICES,
)

# --- Roommate axis weights (sum = 10.0) ---
W_ROOMMATE_DEALBREAKERS = Decimal("4.0")
W_ROOMMATE_VIBE = Decimal("2.0")
W_ROOMMATE_CLEANLINESS = Decimal("1.5")
W_ROOMMATE_SOCIAL = Decimal("1.5")
W_ROOMMATE_BEDTIME = Decimal("1.0")

# --- Housing axis weights (sum = 10.0) ---
W_HOUSING_RENT = Decimal("3.0")
W_HOUSING_LEASE = Decimal("3.0")
W_HOUSING_AMENITIES = Decimal("2.5")
W_HOUSING_LOCATION = Decimal("1.5")

_QUANT = Decimal("0.1")

_VIBE_ORDER = [c[0] for c in IDEAL_HOUSING_VIBE_CHOICES]
_CLEAN_ORDER = [c[0] for c in CLEANLINESS_CHOICES]
_SOCIAL_ORDER = [c[0] for c in SOCIAL_LEVEL_CHOICES]
_BEDTIME_ORDER = [c[0] for c in BEDTIME_CHOICES]


def _idx(order: list[str], value: str) -> int:
    try:
        return order.index(value)
    except ValueError:
        return len(order) // 2


def _ordinal_similarity(order: list[str], a: str, b: str) -> float:
    """1.0 = identical, 0.0 = opposite ends of the scale."""
    ia, ib = _idx(order, a), _idx(order, b)
    span = max(len(order) - 1, 1)
    dist = abs(ia - ib) / span
    return max(0.0, 1.0 - dist)


def _bedtime_avg_index(profile: Profile) -> float:
    wi = _idx(_BEDTIME_ORDER, profile.weeknight_bedtime or "23:00")
    we = _idx(_BEDTIME_ORDER, profile.weekend_bedtime or "23:00")
    return (wi + we) / 2.0


def _dealbreaker_component(seeker: Profile, card: Profile) -> float:
    """
    Returns a value in [0, 1]. 1 = no conflicts; lower when card violates seeker's dealbreakers.
    """
    raw = seeker.roommate_dealbreakers
    if not raw:
        return 1.0

    dealbreakers = set(raw) if isinstance(raw, (list, tuple)) else set()
    if not dealbreakers:
        return 1.0

    penalties = 0.0
    n = len(dealbreakers)

    def penalize(weight: float = 1.0) -> None:
        nonlocal penalties
        penalties += weight / max(n, 1)

    if "smoking" in dealbreakers and card.okay_smoking == "yes":
        penalize(1.2)
    if "pets" in dealbreakers and card.okay_pets == "yes":
        penalize(1.2)
    if "alcohol_use" in dealbreakers and card.okay_alcohol == "yes":
        penalize(0.9)
    if "significant_other_guest" in dealbreakers and card.okay_overnight == "yes":
        penalize(1.0)
    if "guests_frequent" in dealbreakers and card.okay_overnight == "yes":
        penalize(0.7)

    if "messiness" in dealbreakers:
        messy = {"very_messy", "somewhat_messy"}
        if card.cleanliness in messy:
            penalize(1.0)

    if "excessive_noise" in dealbreakers:
        if card.social_level == "very_social":
            penalize(0.8)
        elif card.social_level == "moderately_social":
            penalize(0.35)

    if "sleep_schedules" in dealbreakers:
        seek_avg = _bedtime_avg_index(seeker)
        card_avg = _bedtime_avg_index(card)
        if abs(seek_avg - card_avg) >= 3:
            penalize(0.9)
        elif abs(seek_avg - card_avg) >= 2:
            penalize(0.45)

    if "strong_odors" in dealbreakers and card.okay_smoking == "yes":
        penalize(0.5)

    # drug_use: no direct field — light tie to smoking policy
    if "drug_use" in dealbreakers and card.okay_smoking == "yes":
        penalize(0.3)

    return max(0.0, 1.0 - min(penalties, 1.0))


def pairwise_roommate_score(seeker: Profile, card: Profile) -> Decimal:
    deal = _dealbreaker_component(seeker, card)
    vibe = _ordinal_similarity(
        _VIBE_ORDER,
        seeker.ideal_housing_vibe or "quiet_studious",
        card.ideal_housing_vibe or "quiet_studious",
    )
    clean = _ordinal_similarity(
        _CLEAN_ORDER,
        seeker.cleanliness or "neutral",
        card.cleanliness or "neutral",
    )
    social = _ordinal_similarity(
        _SOCIAL_ORDER,
        seeker.social_level or "balanced",
        card.social_level or "balanced",
    )
    seek_avg = _bedtime_avg_index(seeker)
    card_avg = _bedtime_avg_index(card)
    span = max(len(_BEDTIME_ORDER) - 1, 1)
    bedtime_sim = max(0.0, 1.0 - abs(seek_avg - card_avg) / span)

    total = (
        Decimal(str(deal)) * W_ROOMMATE_DEALBREAKERS
        + Decimal(str(vibe)) * W_ROOMMATE_VIBE
        + Decimal(str(clean)) * W_ROOMMATE_CLEANLINESS
        + Decimal(str(social)) * W_ROOMMATE_SOCIAL
        + Decimal(str(bedtime_sim)) * W_ROOMMATE_BEDTIME
    )
    return total.quantize(_QUANT)


def _days_in_range(start: date, end: date) -> int:
    if not start or not end or end < start:
        return 0
    return (end - start).days + 1


def _lease_overlap_ratio(seeker: Profile, card: Profile) -> float:
    s1, e1 = seeker.rent_start_date, seeker.rent_end_date
    s2, e2 = card.rent_start_date, card.rent_end_date
    if not all((s1, e1, s2, e2)):
        return 0.5  # neutral when incomplete
    start = max(s1, s2)
    end = min(e1, e2)
    overlap_days = _days_in_range(start, end)
    if overlap_days <= 0:
        return 0.0
    seeker_days = _days_in_range(s1, e1)
    if seeker_days <= 0:
        return 0.0
    return min(1.0, overlap_days / seeker_days)


def _rent_component(seeker: Profile, card: Profile) -> float:
    target = int(seeker.min_monthly_rent or 0)
    asking = int(card.min_monthly_rent or 0)
    if asking <= 0:
        return 0.7
    if target <= 0:
        return 1.0
    if asking <= target:
        return 1.0
    ratio = target / asking
    return max(0.0, min(1.0, float(ratio)))


def _yes_no_match(seeker_val: str, card_val: str, seeker_matters: bool) -> float:
    """Seeker 'yes' = wants feature; card 'yes' = has / allows."""
    if not seeker_matters:
        return 1.0
    if seeker_val == "yes":
        return 1.0 if card_val == "yes" else 0.35
    if seeker_val == "no":
        return 1.0  # indifferent to absence
    return 1.0


def _laundry_match(seeker_laundry: str, card_laundry: str) -> float:
    if seeker_laundry == "doesnt_matter":
        return 1.0
    if seeker_laundry == "in_unit":
        if card_laundry == "in_unit":
            return 1.0
        if card_laundry == "in_building":
            return 0.65
        return 0.25
    if seeker_laundry == "in_building":
        if card_laundry in ("in_unit", "in_building"):
            return 1.0
        return 0.35
    return 1.0


def _utilities_match(seeker_u: str, card_u: str) -> float:
    if seeker_u == card_u:
        return 1.0
    return 0.55


def _amenities_component(seeker: Profile, card: Profile) -> float:
    parts = [
        _yes_no_match(seeker.dishwasher, card.dishwasher, seeker.dishwasher == "yes"),
        _laundry_match(seeker.laundry or "doesnt_matter", card.laundry or "in_building"),
        _utilities_match(seeker.utilities or "included", card.utilities or "included"),
        _yes_no_match(seeker.parking_needed, card.parking_needed, seeker.parking_needed == "yes"),
        _yes_no_match(seeker.already_furnished, card.already_furnished, seeker.already_furnished == "yes"),
    ]
    return sum(parts) / len(parts)


def _normalize_location(s: str) -> str:
    return " ".join((s or "").lower().split())


def _location_component(seeker: Profile, card: Profile) -> float:
    a = _normalize_location(seeker.preferred_location or "")
    b = _normalize_location(card.preferred_location or "")
    score = 0.0
    if a and b:
        if a in b or b in a:
            score += 0.65
        else:
            # token overlap
            ta, tb = set(a.replace(",", " ").split()), set(b.replace(",", " ").split())
            common = ta & tb
            if len(common) >= 2:
                score += 0.55
            elif len(common) == 1:
                score += 0.35
            else:
                score += 0.15
    else:
        score += 0.35

    sw = int(seeker.walking_time_minutes or 0)
    cw = int(card.walking_time_minutes or 0)
    if sw <= 0:
        score += 0.35
    elif cw <= sw:
        score += 0.85
    else:
        score += max(0.15, 0.85 - (cw - sw) / 60.0)

    return max(0.0, min(1.0, score))


def pairwise_housing_score(seeker: Profile, card: Profile) -> Decimal:
    rent = _rent_component(seeker, card)
    lease = _lease_overlap_ratio(seeker, card)
    amen = _amenities_component(seeker, card)
    loc = _location_component(seeker, card)

    total = (
        Decimal(str(rent)) * W_HOUSING_RENT
        + Decimal(str(lease)) * W_HOUSING_LEASE
        + Decimal(str(amen)) * W_HOUSING_AMENITIES
        + Decimal(str(loc)) * W_HOUSING_LOCATION
    )
    return total.quantize(_QUANT)


def pairwise_average(seeker: Profile, card: Profile) -> Decimal:
    return (
        (pairwise_roommate_score(seeker, card) + pairwise_housing_score(seeker, card)) / Decimal("2")
    ).quantize(_QUANT)


def attach_pairwise_to_profiles(profiles: list[Profile], seeker: Profile | None) -> None:
    """
    Sets on each profile:
      pairwise_roommate_score, pairwise_housing_score (Decimal), or None if no seeker.
    """
    if seeker is None or not getattr(seeker, "has_onboarded", False):
        for p in profiles:
            p.pairwise_roommate_score = None
            p.pairwise_housing_score = None
        return

    for p in profiles:
        p.pairwise_roommate_score = pairwise_roommate_score(seeker, p)
        p.pairwise_housing_score = pairwise_housing_score(seeker, p)


def sort_profiles_by_pairwise(profiles: list[Profile], seeker: Profile | None) -> list[Profile]:
    """Returns a new list sorted by descending average pairwise score; tie-break pk desc."""
    attach_pairwise_to_profiles(profiles, seeker)
    if seeker is None or not seeker.has_onboarded:
        return sorted(profiles, key=lambda p: p.pk, reverse=True)

    def sort_key(p: Profile) -> tuple[Decimal, int]:
        rm = p.pairwise_roommate_score or Decimal("0")
        hm = p.pairwise_housing_score or Decimal("0")
        avg = (rm + hm) / Decimal("2")
        return (avg, p.pk)

    return sorted(profiles, key=sort_key, reverse=True)


def viewer_profile_for_pairwise(user) -> Profile | None:
    """Returns the user's Profile if they can use pairwise ranking."""
    if not user.is_authenticated:
        return None
    try:
        prof = user.profile
    except Profile.DoesNotExist:
        return None
    if not prof.has_onboarded:
        return None
    return prof
