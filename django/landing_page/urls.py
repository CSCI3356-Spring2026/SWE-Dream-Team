from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name= "landing"),
    path("auth-receiver", views.auth_receiver, name="auth_receiver"),
    path("sign-out", views.sign_out, name="sign_out"),
]