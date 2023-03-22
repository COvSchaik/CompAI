from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from .forms import ProjectForm, AssessmentForm
from django.contrib.auth.models import User
from .models import Assessment, Item
from datetime import datetime

# Create your views here.

def assessment(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk) 
    items = Item.objects.filter(assessment=assessment)

    first = Item.objects.filter(assessment = assessment, item_count = 1)
    context = {'assessment': assessment, 'items': items, 'first': first}
    return render(request,'assessment.html', context)