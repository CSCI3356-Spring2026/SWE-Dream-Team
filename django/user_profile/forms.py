from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Profile,
    ROOMMATE_DEALBREAKER_CHOICES,
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['instagram', 'phone', 'outreach_preference', 'bio', 'photo', 'gender', 'major_minor', 'grad_year']
        widgets = {
            # This adds your specific CSS classes to the Django-generated fields
            'gender': forms.Select(attrs={'class': 'forms-card__input'}),
            'major_minor': forms.TextInput(attrs={'class': 'forms-card__input', 'placeholder': 'e.g. Computer Science'}),
            'grad_year': forms.TextInput(attrs={'class': 'forms-card__input', 'placeholder': '2027'}),
            'instagram': forms.TextInput(attrs={'class': 'forms-card__input'}),
            'phone': forms.TextInput(attrs={'class': 'forms-card__input'}),
            'bio': forms.Textarea(attrs={'class': 'forms-card__textarea', 'rows': 5}),
            'outreach_preference': forms.Select(attrs={'class': 'forms-card__input'}),

        }


_SELECT = {'class': 'forms-card__select'}
_SELECT_MULTI = {'class': 'forms-card__select forms-card__select--multi', 'size': '1'}


class RoommatePreferencesForm(forms.ModelForm):
    roommate_dealbreakers = forms.MultipleChoiceField(
        choices=ROOMMATE_DEALBREAKER_CHOICES,
        required=True,
        widget=forms.SelectMultiple(attrs=_SELECT_MULTI),
    )

    class Meta:
        model = Profile
        fields = [
            'ideal_housing_vibe',
            'roommate_dealbreakers',
            'cleanliness',
            'weekend_bedtime',
            'weeknight_bedtime',
            'social_level',
            'live_opposite_sex',
            'share_double',
            'okay_smoking',
            'okay_alcohol',
            'okay_overnight',
            'okay_pets',
        ]
        labels = {
            'ideal_housing_vibe': 'Ideal housing vibe',
            'roommate_dealbreakers': 'Roommate dealbreakers',
            'cleanliness': 'Cleanliness level of roommates',
            'weekend_bedtime': 'Weekend bedtime hours',
            'weeknight_bedtime': 'Weeknight bedtime',
            'social_level': 'Social level at home',
            'live_opposite_sex': 'Live with opposite sex',
            'share_double': 'Share a double',
            'okay_smoking': 'Okay with smoking',
            'okay_alcohol': 'Okay with alcohol in house',
            'okay_overnight': 'Okay with overnight partners',
            'okay_pets': 'Okay with pets',
        }
        help_texts = {
            'weekend_bedtime': 'Typical time you aim to sleep (8:00 PM – 2:00 AM).',
            'weeknight_bedtime': 'Typical school-night sleep time (8:00 PM – 2:00 AM).',
        }
        widgets = {
            'ideal_housing_vibe': forms.Select(attrs=_SELECT),
            'cleanliness': forms.Select(attrs=_SELECT),
            'weekend_bedtime': forms.Select(attrs=_SELECT),
            'weeknight_bedtime': forms.Select(attrs=_SELECT),
            'social_level': forms.Select(attrs=_SELECT),
            'live_opposite_sex': forms.Select(attrs=_SELECT),
            'share_double': forms.Select(attrs=_SELECT),
            'okay_smoking': forms.Select(attrs=_SELECT),
            'okay_alcohol': forms.Select(attrs=_SELECT),
            'okay_overnight': forms.Select(attrs=_SELECT),
            'okay_pets': forms.Select(attrs=_SELECT),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        empty = 'Select…'
        for name in (
            'ideal_housing_vibe',
            'cleanliness',
            'weekend_bedtime',
            'weeknight_bedtime',
            'social_level',
            'live_opposite_sex',
            'share_double',
            'okay_smoking',
            'okay_alcohol',
            'okay_overnight',
            'okay_pets',
        ):
            f = self.fields[name]
            if hasattr(f, 'empty_label'):
                f.empty_label = empty

    def clean_roommate_dealbreakers(self):
        data = self.cleaned_data.get('roommate_dealbreakers') or []
        if not data:
            raise ValidationError('Select at least one dealbreaker.')
        allowed = {c[0] for c in ROOMMATE_DEALBREAKER_CHOICES}
        for item in data:
            if item not in allowed:
                raise ValidationError('Invalid choice.')
        return list(data)
