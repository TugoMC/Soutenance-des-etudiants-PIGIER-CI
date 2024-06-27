
from django import forms
from .models import Soutenance

class SoutenanceForm(forms.ModelForm):
    class Meta:
        model = Soutenance
        fields = '__all__'
