from django.urls import path

from . import views

urlpatterns = [
    path("profile/preview/", views.profile_card_preview, name="profile-card-preview"),
    path("profile/<int:pk>/", views.profile_detail, name="profile-detail"),
    path(
        "profile/user/<int:user_id>/",
        views.public_profile_by_user,
        name="profile-public-by-user",
    ),
    path("profile/<int:pk>/ban/", views.toggle_ban, name="profile-toggle-ban"),
    path("profile/<int:pk>/hide/", views.toggle_hidden, name="profile-toggle-hidden"),
    path("report/<int:report_pk>/dismiss/", views.dismiss_report, name="report-dismiss"),
]
