from django.urls import path

from . import views

app_name = "report_user"

urlpatterns = [
    path("<str:report_type>/<int:profile_id>/", views.report_form, name="report-form"),
    path("thank-you/", views.report_thank_you, name="report-thank-you"),
]