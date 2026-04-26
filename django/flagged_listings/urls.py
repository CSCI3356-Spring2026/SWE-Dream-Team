from django.urls import path

from . import views

app_name = "flagged_listings"

urlpatterns = [
    path("", views.explore_flagged_listings, name="flagged_listings-explore"),
    path("<int:pk>/", views.flagged_listings_detail, name="flagged_listings-detail"),
]
