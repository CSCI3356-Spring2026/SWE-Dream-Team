from django.urls import path

from . import views

app_name = "report_listing"

urlpatterns = [
    path("<int:listing_id>/", views.report_listing_form, name="report-listing-form"),
    path("thank-you/", views.report_listing_thank_you, name="report-listing-thank-you"),
]
