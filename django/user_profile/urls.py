from django.urls import path

from . import views

urlpatterns = [
    path("profile/preview/", views.profile_card_preview, name="profile-card-preview"),
    path("<int:pk>/", views.profile_detail, name="profile-detail"),
]
