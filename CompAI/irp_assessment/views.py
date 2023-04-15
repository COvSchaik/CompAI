from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
# from .forms import ProjectForm, AssessmentForm
from django.contrib.auth.models import User
from .models import Assessment, Item
from .forms import IRPForm
from datetime import datetime


from django.core.paginator import Paginator

# Create your views here.



@login_required(login_url='signin')
def assessment(request, pk, stage):
    action = request.POST.get('action') 
    # Paginate the questions
    assessment = get_object_or_404(Assessment, pk=pk)     
    item_list = assessment.items.filter(stage=stage) 
    p = Paginator(item_list, 1)
    page = request.GET.get('page')
    items = p.get_page(page)
    # Count amount of pages
    nums = "a" * items.paginator.num_pages
    

   
    # Get the item on the requested page
    item = items.object_list[0]
    # Create a form for the item
    form = IRPForm(instance=item)
    if request.method == 'POST' and action == 'save-item':
        form = IRPForm(request.POST, instance=item)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.saved = True
            commit = form.save()
        return redirect("/irp/"+ str(pk) +"/"+ str(stage) +"/?page=" + str(page))

    else:
        form = IRPForm(instance=item)

    
    
    

    context = {'assessment': assessment, 'items': items, 'nums': nums, 'form': form,}
    return render(request,'assessment.html', context)