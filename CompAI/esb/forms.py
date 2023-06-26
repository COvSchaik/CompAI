from django import forms
from .models import EscTemplate, EscTempQuestion

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

class EscQuestionForm(forms.ModelForm):
    
    class Meta:
        model = EscTempQuestion
        fields = ['answer',]
        widgets = {
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your answer here',
            }),       
        }