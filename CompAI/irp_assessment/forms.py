from django import forms
from .models import Project
from .models import Assessment, Item
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
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Assessment name',
            }),                
        }
