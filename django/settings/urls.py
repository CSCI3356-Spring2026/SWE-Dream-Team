from django.urls import path

from . import views


urlpatterns = [
    path("", views.settings_home, name="app-settings"),
]

