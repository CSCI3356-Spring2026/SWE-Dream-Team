from django.shortcuts import redirect, render

# import profile dependencies: 
from user_profile.forms import ProfileForm, RoommatePreferencesForm
from user_profile.models import Profile


# Use django.forms.ModelForm or forms.Form; POST handlers will save to models in models.py.

RENT_YEAR_RANGE = range(2025, 2032)

SESSION_FORMS_PATH = "forms_onboarding_path"
SESSION_FORMS_STEP = "forms_onboarding_step"
PATH_RENTER = "renter"
PATH_SUBLETTOR = "sublettor"

STEP_INTRO = 1
STEP_ROOMMATE = 2
STEP_HOUSING = 3


def _onboarding_path(request):
    return request.session.get(SESSION_FORMS_PATH, PATH_RENTER)


def _set_step(request, step: int):
    request.session[SESSION_FORMS_STEP] = step


def _redirect_for_workflow_step(step: int, path_kind: str):
    """HTTP redirect to the URL for this step in the given workflow."""
    if step <= STEP_INTRO:
        return redirect("forms-get-to-know-you")
    if path_kind == PATH_RENTER:
        if step == STEP_ROOMMATE:
            return redirect("forms-student-roommate-preferences")
        return redirect("forms-student-housing-preferences")
    if step == STEP_ROOMMATE:
        return redirect("forms-sublettor-roommate-info")
    return redirect("forms-sublettor-listing-details")


def set_workflow_mode(request, mode: str):
    """
    Toggle renter vs sublettor; keeps the same step (intro / roommate / housing).
    Linked from the workflow bar on every forms page.
    """
    m = (mode or "").strip().lower()
    if m in ("renter", "student", "tenant"):
        request.session[SESSION_FORMS_PATH] = PATH_RENTER
        path_kind = PATH_RENTER
    elif m in ("sublettor", "subletor", "lessor", "landlord"):
        request.session[SESSION_FORMS_PATH] = PATH_SUBLETTOR
        path_kind = PATH_SUBLETTOR
    else:
        return redirect("forms-get-to-know-you")

    step = request.session.get(SESSION_FORMS_STEP, STEP_INTRO)
    try:
        step = int(step)
    except (TypeError, ValueError):
        step = STEP_INTRO
    step = max(STEP_INTRO, min(STEP_HOUSING, step))
    return _redirect_for_workflow_step(step, path_kind)


def _get_to_know_you_response(request):
    _set_step(request, STEP_INTRO)
    # Get the profile for the logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Bind POST data AND Files (for the photo) to the form
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            print("DEBUG: Form is valid! Saving now...")
            form.save()
            
            # Logic for redirection based on path
            if _onboarding_path(request) == PATH_SUBLETTOR:
                return redirect("forms-sublettor-roommate-info")
        else:
            print("Detailed Errors:", form.errors.as_text())
            return redirect("forms-student-roommate-preferences")
    else:
        # Pre-fill the form with existing data
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "google_picture": request.session.get("google_picture")
    }
    return render(request, "forms/get_to_know_you.html", context)


def get_to_know_you(request):
    """First step for both workflows; use the top toggle to switch renter / sublettor."""
    return _get_to_know_you_response(request)


def get_to_know_you_renter(request):
    request.session[SESSION_FORMS_PATH] = PATH_RENTER
    return _get_to_know_you_response(request)


def get_to_know_you_sublettor(request):
    request.session[SESSION_FORMS_PATH] = PATH_SUBLETTOR
    return _get_to_know_you_response(request)


def roommate_preferences(request):
    """Renter: roommate preference questionnaire."""
    if _onboarding_path(request) == PATH_SUBLETTOR:
        return redirect("forms-sublettor-roommate-info")
    _set_step(request, STEP_ROOMMATE)
    profile, _created = Profile.objects.get_or_create(user=request.user)

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
    if _onboarding_path(request) == PATH_SUBLETTOR:
        return redirect("forms-sublettor-listing-details")
    _set_step(request, STEP_HOUSING)
    context = {"rent_years": list(RENT_YEAR_RANGE)}
    if request.method == "POST":
        # TODO: validate and save housing preference answers to a model.
        return redirect("landing")
    return render(request, "forms/housing_preferences.html", context)


def sublettor_roommate_info(request):
    """Sublettor: household / roommate info."""
    if _onboarding_path(request) != PATH_SUBLETTOR:
        return redirect("forms-student-roommate-preferences")
    _set_step(request, STEP_ROOMMATE)
    if request.method == "POST":
        # TODO: validate and save to a model.
        return redirect("forms-sublettor-listing-details")
    return render(request, "forms/sublettor_roommate_info.html")


def sublettor_listing_details(request):
    """Sublettor: listing / lease details."""
    if _onboarding_path(request) != PATH_SUBLETTOR:
        return redirect("forms-student-housing-preferences")
    _set_step(request, STEP_HOUSING)
    context = {"rent_years": list(RENT_YEAR_RANGE)}
    if request.method == "POST":
        # TODO: validate and save to a model.
        return redirect("landing")
    return render(request, "forms/sublettor_listing_details.html", context)
