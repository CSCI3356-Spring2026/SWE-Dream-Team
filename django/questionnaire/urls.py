from django.urls import path
from . import views

urlpatterns = [
    path('declaration/', views.DeclarationCardsView.as_view(), name='declaration'),
]