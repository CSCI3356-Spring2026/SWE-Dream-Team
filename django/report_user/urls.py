from django.urls import path

from . import views

app_name = "report_user"

urlpatterns = [
    path("<int:user_id>/", views.report_user_form, name="report-user-form"),
    path("thank-you/", views.report_user_thank_you, name="report-user-thank-you"),
]
