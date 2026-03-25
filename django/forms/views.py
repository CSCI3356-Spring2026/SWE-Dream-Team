from django.shortcuts import render

# Views for role selection, get-to-know-you, and preference forms will go here.
# Use django.forms.ModelForm or forms.Form; POST handlers will save to models in models.py.


def get_to_know_you(request):
    """
    First onboarding screen: shared profile fields.
    GET: render empty form. POST: later validate a ModelForm and save to Profile (or related model).
    """
    if request.method == "POST":
        # TODO: bind POST/FILES to a form, save, redirect to next step (role-specific flows).
        return render(request, "forms/get_to_know_you.html")
    return render(request, "forms/get_to_know_you.html")
