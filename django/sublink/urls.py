"""
URL configuration for sublink project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin-center/", include("admin_panel.urls")),
    path("", include("landing_page.urls")),
    path("", TemplateView.as_view(template_name="base.html"), name="home"), # Temp for now until we get landing page up
    path("", include("user_profile.urls")),
    path("forms/", include("forms.urls")),
    path("listings/", include("listings.urls")),
    path("listings/flagged/", include("flagged_listings.urls")),
    path("roommates/", include("roomate_listing_page.urls")),
    path("roommates/flagged/", include("flagged_users.urls")),
    path("report/", include("report_user.urls")),
    path("settings/", include("settings.urls")),
]

handler404 = 'django.views.defaults.page_not_found'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
