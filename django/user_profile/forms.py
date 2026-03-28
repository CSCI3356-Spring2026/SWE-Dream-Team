from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['gender', 'major_minor', 'grad_year', 'instagram', 'phone', 'bio', 'photo']
        widgets = {
            # This adds your specific CSS classes to the Django-generated fields
            'gender': forms.Select(attrs={'class': 'forms-card__input'}),
            'major_minor': forms.TextInput(attrs={'class': 'forms-card__input', 'placeholder': 'e.g. Computer Science'}),
            'grad_year': forms.TextInput(attrs={'class': 'forms-card__input', 'placeholder': '2027'}),
            'instagram': forms.TextInput(attrs={'class': 'forms-card__input'}),
            'phone': forms.TextInput(attrs={'class': 'forms-card__input'}),
            'bio': forms.Textarea(attrs={'class': 'forms-card__textarea', 'rows': 5}),
        }
