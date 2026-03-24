"""
URL routes for the onboarding questionnaire.

Suggested paths (add views as you build UI):
  - /forms/role/           — Student vs Lessor selection
  - /forms/get-to-know-you/ — shared profile form
  - /forms/student/...     — student-only preference forms
  - /forms/lessor/...      — lessor-only preference forms
"""

from django.urls import path

from . import views

urlpatterns = [
    # path("role/", views.role_select, name="forms-role-select"),
]
