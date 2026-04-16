from django.shortcuts import render

def settings_view(request):
    return render(request, "settings_app/settings_page.html")