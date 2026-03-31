from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import redirect

class DeclarationCardsView(TemplateView):
    template_name = 'declaration/declaration.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cards'] = [
            {'title': 'Student',
            'description': ['Need to find off-campus housing',
            'Looking to find compatible roommates'],
            'icon': 'fa-solid fa-user',
            'link': '/forms/renter/',
            'buttontxt': 'I am renting',
            'value': 'renter',
            },
            {'title': 'Lessor',
            'description': ['Looking to list a property',
            'Looking for a roommate to lease to',
            'Looking for someone to take on my lease'],
            'icon': 'fa-solid fa-bed',
            'link': '/forms/sublettor/',
            'buttontxt': 'I need a renter',
            'value': 'sublettor',
            },
        ]
        return context

def set_user_type(request):
    if request.method == "POST":
        profile = request.user.profile
        user_type = request.POST.get("user_type")

        allowed = {"renter", "sublettor"}
        if user_type in allowed:
            profile.user_type = user_type
            profile.save(update_fields=["user_type"])
            print("saved")
    
    return redirect("/forms/")