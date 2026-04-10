from django.urls import path

from . import views

urlpatterns = [
    path("", views.explore_housing, name="listings-explore-housing"),
]
