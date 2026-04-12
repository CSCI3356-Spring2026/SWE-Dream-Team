from django.urls import path

from . import views

urlpatterns = [
    path("", views.explore_housing, name="listings-explore-housing"),
    path("<int:pk>/", views.listing_detail, name="listings-detail"),
]
