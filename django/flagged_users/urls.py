from django.urls import path

from . import views

app_name = "flagged_users"

urlpatterns = [
    path("", views.explore_flagged_users, name="flagged_users-explore"),
    path("<int:pk>/", views.flagged_users_detail, name="flagged_users-detail"),
]
