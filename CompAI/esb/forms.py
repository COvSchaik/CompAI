from django import forms
from .models import EscTemplate

class EscTemplateForm(forms.ModelForm):
       
    class Meta:
        model = EscTemplate
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your template name',
            }),       
        }
