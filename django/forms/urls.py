"""
Onboarding: choose renter vs sublettor at /forms/set-card/, then /forms/ (Let's Get to Know You).
Legacy /forms/renter/ and /forms/sublettor/ redirect to set-card.
"""

from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        "renter/",
        RedirectView.as_view(pattern_name="forms-set-card", permanent=False),
        name="forms-renter-start",
    ),
    path(
        "sublettor/",
        RedirectView.as_view(pattern_name="forms-set-card", permanent=False),
        name="forms-sublettor-start",
    ),
    path("set-card/", views.SetUserTypeCardsView.as_view(), name="forms-set-card"),
    path("set-user-type/", views.set_user_type, name="forms-set-user-type"),
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
