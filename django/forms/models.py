"""
Database models for the onboarding flow will live here.

Planned flow (for when you wire the DB):
  1. Role choice: Student vs Lessor (store on User, Profile, or a small RoleSession model).
  2. "Let's get to know you" — shared fields (name, email, major, grad year, bio, photo, etc.).
     Map to user_profile.Profile or extend it; avoid duplicating User.email if you use auth User.
  3. Student: roommate-preferences form + housing-preferences form.
  4. Lessor: counterpart forms (roommates they seek / housing they offer).

For now this app is UI-only; add Model classes and migrations when you persist submissions.
"""

from django.db import models

# Create your models here.
