from django.urls import path

from . import views

urlpatterns = [
    path("profile/preview/", views.profile_card_preview, name="profile-card-preview"),
<<<<<<< HEAD
    path("<int:pk>/", views.profile_detail, name="profile-detail"),
=======
    path(
        "profile/user/<int:user_id>/",
        views.public_profile_by_user,
        name="profile-public-by-user",
    ),
>>>>>>> listing_individual_card
]
