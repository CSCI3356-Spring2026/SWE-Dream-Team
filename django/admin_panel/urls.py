from django.urls import path

from . import views

app_name = "admin_panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("images/", views.image_library, name="images"),
    path("reported-accounts/", views.reported_accounts, name="reported-accounts"),
]
