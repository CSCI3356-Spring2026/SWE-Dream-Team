from django.shortcuts import render
from django.views.generic import ListView
from user_profile.models import Profile
from django.db.models import Q

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

        search = self.request.GET.get("search", "").strip()
        major = self.request.GET.get("major", "").strip()
        year = self.request.GET.get("year", "").strip()

        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(major_minor__icontains=search)
            )

        if major:
            queryset = queryset.filter(major_minor__icontains=major)

        if year:
            queryset = queryset.filter(grad_year=year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_data = self.request.session.get("user_data", {})
        context["user_type"] = user_data.get("user_type")
        return context
