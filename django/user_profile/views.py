from django.shortcuts import render


def profile_card_preview(request):
    """Serves the profile card template (placeholder content) for local preview."""
    return render(request, "user_profile/profile_card.html")
