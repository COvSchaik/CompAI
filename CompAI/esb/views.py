from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import yaml

from .models import EscTemplate, EscTempQuestion
from projects.models import Project
from .forms import EscTemplateForm

# Create your views here.
@login_required(login_url='signin')
def esc(request):
    project_list = Project.objects.filter(status = "active")
    temp_list = EscTemplate.objects.all()
    
    if request.method == 'POST':
        form = EscTemplateForm(request.POST or None)        
        if form.is_valid():
            temp = form.save(commit=False)
            temp.creator = request.user
            temp.save()

            for i in range(1, 13):
                tempq = EscTempQuestion()
                tempq.template = temp
                tempq.number = i
                tempq.save()
        return redirect("temp/" + str(temp.id))
    else:
        form = EscTemplateForm()

    context = {'projects': project_list, 'templates': temp_list, 'form': form}
    return render(request,'esc_overview.html', context)

