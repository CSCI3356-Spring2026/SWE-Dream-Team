from django.shortcuts import render
from django.views.generic import ListView
from user_profile.models import Profile

def home(request):
    user_data = request.session.get("user_data", {})
    return render(request, "home/home.html", {
        "user_type": user_data.get("user_type")
    })

class HomeCardsView(ListView):
    template_name = 'home/home.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return Profile.objects.all()
