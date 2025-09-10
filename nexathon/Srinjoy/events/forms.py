from django import forms
from .models import UniversityEvent

class UniversityEventForm(forms.ModelForm):
    class Meta:
        model = UniversityEvent
        fields = ['name', 'date', 'location', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
