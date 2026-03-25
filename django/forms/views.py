from django.shortcuts import redirect, render

# Use django.forms.ModelForm or forms.Form; POST handlers will save to models in models.py.

RENT_YEAR_RANGE = range(2025, 2032)


def get_to_know_you(request):
    """
    Shared profile onboarding (linked from the separate role / landing flow).
    POST: later validate a ModelForm and save; then continue to roommate preferences.
    """
    if request.method == "POST":
        # TODO: bind POST/FILES to a form, save to Profile (or related model).
        return redirect("forms-student-roommate-preferences")
    return render(request, "forms/get_to_know_you.html")


def roommate_preferences(request):
    """Roommate preference questionnaire after get-to-know-you submit."""
    if request.method == "POST":
        # TODO: validate and save preference answers to a model.
        return redirect("forms-student-housing-preferences")
    return render(request, "forms/roommate_preferences.html")


def housing_preferences(request):
    """Housing search preferences after roommate preferences submit."""
    context = {"rent_years": list(RENT_YEAR_RANGE)}
    if request.method == "POST":
        # TODO: validate and save housing preference answers to a model.
        return redirect("landing")
    return render(request, "forms/housing_preferences.html", context)
