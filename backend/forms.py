from django import forms
from backend.models import Screenshots


class ScreenshotForm(forms.ModelForm):
    class Meta:
        model = Screenshots
        fields = ['image']
