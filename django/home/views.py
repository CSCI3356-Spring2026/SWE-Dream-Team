from django.shortcuts import render
from django.views.generic import ListView
from user_profile.models import Profile

class HomeCardsView(ListView):
    model = Profile
    template_name = 'home/home.html'
    context_object_name = 'cards'

    def get_queryset(self):
        queryset = super().get_queryset()

        user_data = self.request.session.get("user_data", {})
        user_type = user_data.get("user_type")

        if user_type:
            queryset = queryset.filter(user_type=user_type)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = self.request.session.get("user_data", {})
        context["user_type"] = user_data.get("user_type")
        return context
