from django import forms
from .models import Project
from irp_assessment.models import Assessment
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    users = User.objects.all()
    
    class Meta:
        model = Project
        fields = ['name','startdate', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your project name',
            }),
            'startdate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date', 
                'id': 'startdate',               
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Project description',
                'rows': 3,
            })            
        }

class AssessmentForm(forms.ModelForm):    
    
    class Meta:
        model = Assessment
        fields = ['name', 'framework']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Assessment name',
            }),
            'framework': forms.Select(                 
                attrs={'class': 'form-select',
            }),
        }
