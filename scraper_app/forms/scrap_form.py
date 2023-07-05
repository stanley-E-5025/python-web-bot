from django import forms
from django import forms
from scraper_app.models import Scraper

class ScraperForm(forms.ModelForm):
    class Meta:
        model = Scraper
        fields = ['url', 'steps', 'case', 'data']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'steps': forms.FileInput(attrs={'class': 'form-control'}),
            'case': forms.Select(attrs={'class': 'form-control'}, choices=[('blob', 'Blob')]),
            'data': forms.TextInput(attrs={'class': 'form-control'}),
        }
