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
    
    stage_dict = {'design': 1, 'development':2, 'evaluation':3, 'operation':4, 'retirement':5}
   
    # Get the item on the requested page
    item = items.object_list[0]
    # Create a form for the item
    form = IRPForm(instance=item)
    if request.method == 'POST' and action == 'save-item':
        form = IRPForm(request.POST, instance=item)
        if form.is_valid():
            commit = form.save(commit=False)
            commit.saved = True
            if stage_dict[assessment.stage] < stage_dict[item.stage]:            
                assessment.stage = item.stage
                assessment.save()
            commit = form.save()
        return redirect("/irp/"+ str(pk) +"/"+ str(stage) +"/?page=" + str(page))

    else:
        form = IRPForm(instance=item)

    #graphs:
    #radar
    stages = ['Design', 'Development', 'Evaluation', 'Operation', 'Retirement']
    data_values = [0, 0, 0, 0, 0, ] 
    for i in [0,1,2,3,4]:
        for item in assessment.items.filter(stage__iexact=stages[i]).all():
            if item.saved:
                data_values[i] += item.maturity
        count = assessment.items.filter(stage__iexact=stages[i], saved = True).count()
        if count > 0:
            data_values[i]=data_values[i]/count
        else: data_values[i] = 0

    #bars
    progress = assessment.items.filter(saved=True).count()
    total = assessment.items.count()
    perc = (progress/total)*100
    avg = sum(data_values)/len(data_values)
    avgperc = (avg/5)*100
   

        
    

    context = {'assessment': assessment, 'items': items, 'nums': nums, 'form': form, 'stages': stages, 'data_values': data_values,
               'progress': progress, 'total': total, 'perc': perc, 'avg': avg, 'avgperc': avgperc,}
    return render(request,'assessment.html', context)