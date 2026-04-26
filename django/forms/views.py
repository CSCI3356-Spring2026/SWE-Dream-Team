from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from user_profile.forms import (
    HousingPreferencesForm,
    ProfileForm,
    RoommatePreferencesForm,
    SublettorListingDetailsForm,
    SublettorRoommateInfoForm,
)
from user_profile.models import Profile, USER_TYPE_CHOICES

RENT_YEAR_RANGE = range(2025, 2032)

SESSION_FORMS_PATH = "forms_onboarding_path"
SESSION_FORMS_STEP = "forms_onboarding_step"
SESSION_USER_TYPE_CHOSEN = "forms_user_type_chosen"
PATH_RENTER = "renter"
PATH_SUBLETTOR = "sublettor"

_ALLOWED_USER_TYPES = frozenset(dict(USER_TYPE_CHOICES).keys())

STEP_INTRO = 1
STEP_ROOMMATE = 2
STEP_HOUSING = 3


def _onboarding_path(request):
    return request.session.get(SESSION_FORMS_PATH, PATH_RENTER)


def _effective_onboarding_path(request, profile):
    if profile.has_onboarded:
        return profile.user_type
    return _onboarding_path(request)


def _set_step(request, step: int):
    request.session[SESSION_FORMS_STEP] = step


def _redirect_if_onboarding_blocked(request, profile):
    if not profile.has_onboarded and not request.session.get(SESSION_USER_TYPE_CHOSEN):
        return redirect("forms-set-card")
    return None


class SetUserTypeCardsView(TemplateView):
    template_name = "forms/set_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cards"] = [
            {
                "title": " Student Renter",
                "description": [
                    "Need to find off-campus housing",
                    "Looking to find compatible roommates",
                ],
                "icon": "fa-solid fa-user",
                "buttontxt": "I am renting",
                "value": PATH_RENTER,
            },
            {
                "title": "Sublettor",
                "description": [
                    "Looking to list a property",
                    "Looking for a roommate to lease to",
                    "Looking for someone to take on my lease",
                ],
                "icon": "fa-solid fa-bed",
                "buttontxt": "I need a renter",
                "value": PATH_SUBLETTOR,
            },
        ]
        return context


@require_POST
def set_user_type(request):
    profile, _created = Profile.objects.get_or_create(user=request.user)
    user_type = (request.POST.get("user_type") or "").strip().lower()
    if user_type not in _ALLOWED_USER_TYPES:
        return redirect("forms-set-card")

    profile.user_type = user_type
    profile.save(update_fields=["user_type"])
    request.session[SESSION_FORMS_PATH] = user_type
    request.session[SESSION_USER_TYPE_CHOSEN] = True
    return redirect("forms-get-to-know-you")


def _get_to_know_you_response(request):
    profile, _created = Profile.objects.get_or_create(user=request.user)
    blocked = _redirect_if_onboarding_blocked(request, profile)
    if blocked:
        return blocked

    _set_step(request, STEP_INTRO)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if _effective_onboarding_path(request, profile) == PATH_SUBLETTOR:
                return redirect("forms-sublettor-roommate-info")
            return redirect("forms-student-roommate-preferences")
        return render(
            request,
            "forms/get_to_know_you.html",
            {
                "form": form,
                "google_picture": request.session.get("google_picture"),
            },
        )

    form = ProfileForm(instance=profile)
    context = {
        "form": form,
        "google_picture": request.session.get("google_picture"),
    }
    return render(request, "forms/get_to_know_you.html", context)


def get_to_know_you(request):
    """First step for both workflows after user type is chosen on set-card."""
    return _get_to_know_you_response(request)


def roommate_preferences(request):
    """Renter: roommate preference questionnaire."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    blocked = _redirect_if_onboarding_blocked(request, profile)
    if blocked:
        return blocked
    if _effective_onboarding_path(request, profile) == PATH_SUBLETTOR:
        return redirect("forms-sublettor-roommate-info")
    _set_step(request, STEP_ROOMMATE)

    if request.method == "POST":
        form = RoommatePreferencesForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("forms-student-housing-preferences")
    else:
        form = RoommatePreferencesForm(instance=profile)

    return render(request, "forms/roommate_preferences.html", {"form": form})


def housing_preferences(request):
    """Renter: housing search preferences."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    blocked = _redirect_if_onboarding_blocked(request, profile)
    if blocked:
        return blocked
    if _effective_onboarding_path(request, profile) == PATH_SUBLETTOR:
        return redirect("forms-sublettor-listing-details")
    _set_step(request, STEP_HOUSING)
    rent_years = list(RENT_YEAR_RANGE)

    if request.method == "POST":
        form = HousingPreferencesForm(request.POST, instance=profile, rent_years=rent_years)
        if form.is_valid():
            form.save()
            profile.has_onboarded = True
            profile.save(update_fields=["has_onboarded"])
            return redirect("listings-explore-housing")
    else:
        form = HousingPreferencesForm(instance=profile, rent_years=rent_years)

    return render(request, "forms/housing_preferences.html", {"form": form, "rent_years": rent_years})


def sublettor_roommate_info(request):
    """Sublettor: household / roommate info."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    blocked = _redirect_if_onboarding_blocked(request, profile)
    if blocked:
        return blocked
    if _effective_onboarding_path(request, profile) != PATH_SUBLETTOR:
        return redirect("forms-student-roommate-preferences")
    _set_step(request, STEP_ROOMMATE)

    if request.method == "POST":
        form = SublettorRoommateInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("forms-sublettor-listing-details")
    else:
        form = SublettorRoommateInfoForm(instance=profile)

    return render(request, "forms/sublettor_roommate_info.html", {"form": form})


def sublettor_listing_details(request):
    """Sublettor: listing / lease details."""
    profile, _created = Profile.objects.get_or_create(user=request.user)
    blocked = _redirect_if_onboarding_blocked(request, profile)
    if blocked:
        return blocked
    if _effective_onboarding_path(request, profile) != PATH_SUBLETTOR:
        return redirect("forms-student-housing-preferences")

    _set_step(request, STEP_HOUSING)
    rent_years = list(RENT_YEAR_RANGE)

    if request.method == "POST":
        form = SublettorListingDetailsForm(
            request.POST,
            request.FILES,
            instance=profile,
            rent_years=rent_years,
        )
        if form.is_valid():
            form.save()
            profile.has_onboarded = True
            profile.save(update_fields=["has_onboarded"])
            return redirect("roommates-explore")
    else:
        form = SublettorListingDetailsForm(instance=profile, rent_years=rent_years)

    return render(request, "forms/sublettor_listing_details.html", {"form": form, "rent_years": rent_years})
