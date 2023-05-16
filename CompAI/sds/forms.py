from django import forms
from .models import Template, TempQuestion, SDSQuestion

class TemplateForm(forms.ModelForm):
       
    class Meta:
        model = Template
        fields = ['name',]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your template name',
            }),       
        }

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = TempQuestion
        fields = ['answer',]
        widgets = {
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your answer here',
            }),       
        }

class SDSQuestionForm(forms.ModelForm):
    
    class Meta:
        model = SDSQuestion
        fields = ['answer',]
        widgets = {
            'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your answer here',
            }),       
        }
