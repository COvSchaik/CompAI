from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from .forms import ProjectForm, AssessmentForm
from django.contrib.auth.models import User
from .models import Assessment, Item
from datetime import datetime

from django.core.paginator import Paginator

# Create your views here.




def assessment(request, pk, stage):
    assessment = get_object_or_404(Assessment, pk=pk) 
    item_list = assessment.items.filter(stage=stage)  

    p = Paginator(item_list, 1)
    page = request.GET.get('page')
    items = p.get_page(page)
    nums = "a" * items.paginator.num_pages

    context = {'assessment': assessment, 'items': items, 'nums': nums}
    return render(request,'assessment.html', context)