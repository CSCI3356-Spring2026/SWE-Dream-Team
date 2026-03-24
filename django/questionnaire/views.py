from django.shortcuts import render
from django.views.generic import TemplateView

class DeclarationCardsView(TemplateView):
    template_name = 'items/static_cards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = [
            {'title': 'Student', 'description': ['Need to find off-campus housing', 'Looking to find compatible roommates'], 'icon': 'fa-solid fa-user'},
            {'title': 'Lessor', 'description': ['Looking to list a property', 'Looking for a roommate to lease to', 'Looking for someone to take on my lease'], 'icon': 'fa-solid fa-bed'},
        ]
        return context
