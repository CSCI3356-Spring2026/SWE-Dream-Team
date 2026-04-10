from django.urls import path

from . import views

urlpatterns = [
    path("", views.explore_roommates, name="roommates-explore"),
    path("<int:pk>/", views.roommate_detail, name="roommates-detail"),
]
