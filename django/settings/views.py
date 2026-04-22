from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def settings_home(request):
    return render(request, "settings/settings_home.html")

from django.shortcuts import render

# Create your views here.
