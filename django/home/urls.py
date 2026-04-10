from django.urls import path
from .views import HomeCardsView

urlpatterns = [
    path('home/', HomeCardsView.as_view(), name='home'),
]
