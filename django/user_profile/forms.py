from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import (
    Profile,
    LAUNDRY_CHOICES,
    ROOMMATE_DEALBREAKER_CHOICES,
    UTILITIES_CHOICES,
    YES_NO_CHOICES,
    USER_TYPE_CHOICES,
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


class HousingPreferencesForm(forms.ModelForm):
    rent_start_month = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'forms-card__select housing-rent__month'}))
    rent_start_year = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'forms-card__select housing-rent__year'}))
    rent_end_month = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'forms-card__select housing-rent__month'}))
    rent_end_year = forms.ChoiceField(required=True, widget=forms.Select(attrs={'class': 'forms-card__select housing-rent__year'}))

    class Meta:
        model = Profile
        fields = [
            'preferred_location',
            'walking_time_minutes',
            'min_monthly_rent',
            'dishwasher',
            'laundry',
            'utilities',
            'parking_needed',
            'already_furnished',
            'listing_image',
        ]
        labels = {
            'preferred_location': 'Preferred location (street / area)',
            'walking_time_minutes': 'Walking time from Boston College (in minutes)',
            'min_monthly_rent': 'Target monthly rental price',
            'dishwasher': 'Dishwasher?',
            'laundry': 'Laundry specifications',
            'utilities': 'Utilities',
            'parking_needed': 'Parking needed',
            'already_furnished': 'Already furnished',
        }
        widgets = {
            'preferred_location': forms.TextInput(attrs={'class': 'forms-card__input', 'autocomplete': 'street-address', 'placeholder': 'Value'}),
            'walking_time_minutes': forms.NumberInput(attrs={'class': 'forms-card__input', 'min': '0', 'step': '1', 'inputmode': 'numeric', 'placeholder': 'Value'}),
            'min_monthly_rent': forms.NumberInput(attrs={'class': 'forms-card__input', 'min': '0', 'step': '1', 'inputmode': 'numeric', 'placeholder': 'Value'}),
            'dishwasher': forms.Select(attrs=_SELECT),
            'laundry': forms.Select(attrs=_SELECT),
            'utilities': forms.Select(attrs=_SELECT),
            'parking_needed': forms.Select(attrs=_SELECT),
            'already_furnished': forms.Select(attrs=_SELECT),
            'listing_image': forms.FileInput(attrs={'class': 'forms-card__input'}),
        }

    def __init__(self, *args, **kwargs):
        self.rent_years = kwargs.pop('rent_years', None)
        super().__init__(*args, **kwargs)

        months = [
            ('01', 'Jan'),
            ('02', 'Feb'),
            ('03', 'Mar'),
            ('04', 'Apr'),
            ('05', 'May'),
            ('06', 'Jun'),
            ('07', 'Jul'),
            ('08', 'Aug'),
            ('09', 'Sep'),
            ('10', 'Oct'),
            ('11', 'Nov'),
            ('12', 'Dec'),
        ]
        years = self.rent_years or []
        self.fields['rent_start_month'].choices = [('', 'Month')] + months
        self.fields['rent_end_month'].choices = [('', 'Month')] + months
        self.fields['rent_start_year'].choices = [('', 'Year')] + [(str(y), str(y)) for y in years]
        self.fields['rent_end_year'].choices = [('', 'Year')] + [(str(y), str(y)) for y in years]

        # Pre-fill month/year from instance for GET.
        if self.instance and getattr(self.instance, 'rent_start_date', None):
            self.initial.setdefault('rent_start_month', self.instance.rent_start_date.strftime('%m'))
            self.initial.setdefault('rent_start_year', str(self.instance.rent_start_date.year))
        if self.instance and getattr(self.instance, 'rent_end_date', None):
            self.initial.setdefault('rent_end_month', self.instance.rent_end_date.strftime('%m'))
            self.initial.setdefault('rent_end_year', str(self.instance.rent_end_date.year))

        empty = 'Select…'
        for name in ('dishwasher', 'laundry', 'utilities', 'parking_needed', 'already_furnished'):
            f = self.fields[name]
            if hasattr(f, 'empty_label'):
                f.empty_label = empty

        # Ensure choices align with model constants (defense-in-depth if model changes).
        self.fields['dishwasher'].choices = YES_NO_CHOICES
        self.fields['parking_needed'].choices = YES_NO_CHOICES
        self.fields['already_furnished'].choices = YES_NO_CHOICES
        self.fields['laundry'].choices = LAUNDRY_CHOICES
        self.fields['utilities'].choices = UTILITIES_CHOICES

    def clean(self):
        cleaned = super().clean()
        start_month = cleaned.get('rent_start_month')
        start_year = cleaned.get('rent_start_year')
        end_month = cleaned.get('rent_end_month')
        end_year = cleaned.get('rent_end_year')

        if start_month and start_year:
            cleaned['rent_start_date'] = date(int(start_year), int(start_month), 1)
        if end_month and end_year:
            cleaned['rent_end_date'] = date(int(end_year), int(end_month), 1)

        start_date = cleaned.get('rent_start_date')
        end_date = cleaned.get('rent_end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('Rent end date must be on or after the start date.')

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.rent_start_date = self.cleaned_data['rent_start_date']
        instance.rent_end_date = self.cleaned_data['rent_end_date']
        if commit:
            instance.save()
        return instance


class SublettorRoommateInfoForm(RoommatePreferencesForm):
    class Meta(RoommatePreferencesForm.Meta):
        labels = {
            'ideal_housing_vibe': 'What is your housing vibe?',
            'roommate_dealbreakers': 'Which of the following apply to your household?',
            'cleanliness': 'Cleanliness level in the household',
            'weekend_bedtime': 'Typical weekend bedtime in the household',
            'weeknight_bedtime': 'Typical weeknight bedtime in the household',
            'social_level': 'Social level in the home',
            'live_opposite_sex': 'Opposite-sex roommates in the unit?',
            'share_double': 'Is the arrangement a shared double?',
            'okay_smoking': 'Is smoking allowed in the home?',
            'okay_alcohol': 'Is alcohol allowed in the home?',
            'okay_overnight': 'Are overnight guests allowed?',
            'okay_pets': 'Are pets in the home?',
        }
        help_texts = {
            'weekend_bedtime': 'Roughly when the home quiets down (8:00 PM – 2:00 AM).',
            'weeknight_bedtime': 'Roughly when the home quiets down on school nights (8:00 PM – 2:00 AM).',
        }


class SublettorListingDetailsForm(HousingPreferencesForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['listing_image'].required = True


    class Meta(HousingPreferencesForm.Meta):
        labels = {
            'preferred_location': 'House location (street / area)',
            'walking_time_minutes': 'Walking time from Boston College (in minutes)',
            'min_monthly_rent': 'Asking monthly rent',
            'dishwasher': 'Does the unit have a dishwasher?',
            'laundry': 'Laundry',
            'utilities': 'Utilities',
            'parking_needed': 'Parking available?',
            'already_furnished': 'Is the unit furnished?',
            'listing_image': 'Upload a photo of your listing',
        }
