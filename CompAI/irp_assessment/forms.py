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
class IRPForm(forms.ModelForm):    
    
    class Meta:
        MATURITY_LEVELS = (
            (1, 'Level 1: Initial'),
            (2, 'Level 2: Repeatable'),
            (3, 'Level 3: Defined'),
            (4, 'Level 4: Managed and Measurable'),
            (5, 'Level 5: Continuous Improvement'),
        )
        model = Item
        fields = ['maturity', 'summary', 'proof']
        widgets = {
            'maturity' : forms.Select( 
                choices=MATURITY_LEVELS, 
                attrs={'class': 'form-select',
            }),
              
            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short description here'
                
            }), 
            'proof': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a link to relevant documents'
            }),               
        }
