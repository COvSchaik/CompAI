from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, AssessmentForm
from django.contrib.auth.models import User
from .models import Project
from irp_assessment.models import Assessment
from irp_assessment.models import Item
from frameworks.models import Framework
from datetime import datetime

import yaml

# Create your views here.
@login_required(login_url='signin')
def projects(request):
    userdisplay = User.objects.all()
    project_list = Project.objects.filter(status = "active")
    archived = Project.objects.filter(status = "archived")

    if request.method == 'POST':
        form = ProjectForm(request.POST or None)        
        if form.is_valid():
            proj = form.save(commit=False)
            proj.creator = request.user
            proj.save()
            selected_users = request.POST.getlist('form-project-manager[]')
            # Add the selected users to the project's team members
            proj.members.set(selected_users) 
            proj.members.add(request.user)    
            proj.save()
        return redirect("detail/" + str(proj.id))
    

    else:
        form = ProjectForm()

    
    context = {'projects': project_list, 'form': form, 'userdisplay': userdisplay, 'archived':archived}
    return render (request, 'projects.html', context)


def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    project.delete()
    return redirect('/projects')


@login_required(login_url='signin')
def detail(request, pk):
    action = request.POST.get('action')    
    project = get_object_or_404(Project, pk=pk)  
    memberdisplay = project.members.all()
    assessmentdisplay = project.assessments.all()
    userdisplay = User.objects.exclude(projects=project.id) 

    if request.method == 'POST' and action == 'change_info':
        form = ProjectForm(request.POST or None)        
        if form.is_valid():
            edit = form.cleaned_data
            project.name = edit['name']
            project.description = edit['description']
            project.startdate = edit['startdate']   
            # project.enddate.set(request.POST.get('enddate'))
            # project.enddate = request.POST.get('enddate')

            # Add the selected users to the project's team members
            project.save()
            return redirect("/projects/detail/" + str(project.id)) 
    else:
        instance = project
        form = ProjectForm(
            initial = {
                'name': project.name,
                'startdate': project.startdate,                
                'description': project.description
            })
        
    if request.method == 'POST' and action == 'change_members':
            selected_users = request.POST.getlist('form-project-manager[]')
            project.members.clear()           
            project.members.set(selected_users) 
            # Add the selected users to the project's team members
            project.save()
            return redirect("/projects/detail/" + str(project.id)) 
    
    if request.method == 'POST' and action == 'new_assessment':
        form = AssessmentForm(request.POST or None)        
        if form.is_valid():
            asses = form.save(commit=False)
            asses.creator = request.user
            asses.project = project            
            asses.save()

            template = Framework.objects.get(name= asses.framework)          
            items = template.items.all()

            item_count = 0
            for i in items:
                item = Item()
                item.assessment = asses
                item.item_count = item_count + 1
                item.item_nr = i.item_nr
                item.stage = i.stage
                item.template = i
                # item.category = i["category"]
                # item.respondent = i["respondent"]
                # item.description =i["description"]
                # item.deliverable_description = i["deliverable"]
                item.modified_by = request.user


                item.save()
                item_count = item_count + 1


            
        return redirect("/projects/detail/" + str(project.id))
    else:
        asses_form = AssessmentForm()

    
      
    context = {'project': project, 'form': form, 'asses_form': asses_form, 'memberdisplay': memberdisplay,
                'userdisplay': userdisplay, 'assessmentdisplay': assessmentdisplay}
    return render (request, 'detail.html', context)

def delete_assessment(request, pk):
    assessment = Assessment.objects.get(pk=pk)
    assessment.delete()
    return redirect('/projects/detail/'+ str(assessment.project.id))