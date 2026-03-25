"""
URL routes for the onboarding questionnaire (profile + roommate prefs).
Role / user-type selection lives in another app.
"""

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", views.get_to_know_you, name="forms-get-to-know-you"),
    path(
        "get-to-know-you/",
        RedirectView.as_view(
            pattern_name="forms-get-to-know-you",
            permanent=False,
        ),
        name="forms-get-to-know-you-legacy",
    ),
    path(
        "student/roommate-preferences/",
        views.roommate_preferences,
        name="forms-student-roommate-preferences",
    ),
]
