from django.urls import path
from . import views

urlpatterns = [
    path('declaration/', views.DeclarationCardsView.as_view(), name='declaration'),
    path('set-user-type/', views.set_user_type, name='set_user_type'),
]