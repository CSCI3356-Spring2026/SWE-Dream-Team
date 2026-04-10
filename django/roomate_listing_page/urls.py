from django.urls import path

from . import views

urlpatterns = [
    path("", views.explore_roommates, name="roommates-explore"),
]
