"""
Onboarding: renter vs sublettor. Use the toggle on any /forms/ page, or:
  /forms/renter/      — start as renter (step 1)
  /forms/sublettor/   — start as sublettor (step 1)
  /forms/workflow/renter/ or .../sublettor/ — switch workflow, same step
"""

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("renter/", views.get_to_know_you_renter, name="forms-renter-start"),
    path("sublettor/", views.get_to_know_you_sublettor, name="forms-sublettor-start"),
    path(
        "workflow/<slug:mode>/",
        views.set_workflow_mode,
        name="forms-set-workflow-mode",
    ),
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
    path(
        "student/housing-preferences/",
        views.housing_preferences,
        name="forms-student-housing-preferences",
    ),
    path(
        "sublettor/roommate-info/",
        views.sublettor_roommate_info,
        name="forms-sublettor-roommate-info",
    ),
    path(
        "sublettor/listing-details/",
        views.sublettor_listing_details,
        name="forms-sublettor-listing-details",
    ),
]
