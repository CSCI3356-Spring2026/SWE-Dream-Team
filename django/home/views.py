from django.shortcuts import render
from django.views.generic import ListView
from .models import HomeCards

def home(request):
    user_data = request.session.get("user_data", {})
    return render(request, "home/home.html", {
        "user_type": user_data.get("user_type")
    })

class HomeCardsView(ListView):
    model = HomeCards
    template_name = 'home/home.html'
    context_object_name = 'cards'
