from django.shortcuts import render
from django.views.generic import ListView
from .models import HomeCards

def home(request):
    return render(request, 'home/home.html')

class HomeCardsView(ListView):
    model = HomeCards
    template_name = 'home/home.html'
    context_object_name = 'cards'
