from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import yaml

from .models import ESC, EscTemplate, EscTempQuestion
from projects.models import Project
from .forms import EscTemplateForm, EscQuestionForm

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

            for i in range(1, 11):
                tempq = EscTempQuestion()
                tempq.template = temp
                tempq.number = i
                tempq.save()
        return redirect("esctemp/" + str(temp.id))
    else:
        form = EscTemplateForm()

    context = {'projects': project_list, 'templates': temp_list, 'form': form}
    return render(request,'esc_overview.html', context)

@login_required(login_url='signin')
def esctemp(request, pk):
    action = request.POST.get('action')
    template = get_object_or_404(EscTemplate, pk=pk)
    questions = template.questions.all()

    if request.method == 'POST' and action == 'save-sds':     
        for question in questions:
            form_prefix = f'question-{question.number}'
            form = EscQuestionForm(request.POST, instance=question, prefix=form_prefix)
            
            if form.is_valid():
                form.save()
        return redirect('esctemp', pk=pk)  


    with open('yaml/esc/esc.yaml', 'r') as file:
            descriptions = yaml.load(file, Loader=yaml.FullLoader)
    forms = []
    last = ""
    for question in questions:
        form_prefix = f'question-{question.number}'
        form = EscQuestionForm(instance=question, prefix=form_prefix)
        form.description = descriptions.get(question.number, {}).get('text', '')
        form.title = descriptions.get(question.number, {}).get('title', '')
        form.first = False
        form.last = False
        if form.title != last:
            form.first = True
            if forms:
                forms[-1].last = True
        last = form.title
        
        
        forms.append(form)

    context = {'template': template, 'forms': forms}
    return render(request,'esc_template.html', context)

@login_required(login_url='signin')
def delete_esc(request, pk):
    temp = EscTemplate.objects.get(pk=pk)
    temp.delete()
    return redirect('/esc')

@login_required(login_url='signin')
def create_esc(request, pk): 
    action = request.POST.get('action')
    proj = get_object_or_404(Project, pk=pk)
    sds = get_object_or_404(ESC, pk=proj.esc.id)
    questions = sds.questions.all()
    temp_list = EscTemplate.objects.all()

    if request.method == 'POST' and action == 'save-sds':     
        for question in questions:
            form_prefix = f'question-{question.number}'
            form = EscQuestionForm(request.POST, instance=question, prefix=form_prefix)
            
            if form.is_valid():
                form.save()
        return redirect('create_esc', pk=pk)
    
    if request.method == 'POST' and action == 'load-temp':
        template_id = request.POST.get('template_id')
        temp = get_object_or_404(EscTemplate, pk=template_id)       
        for question in sds.questions.all():
            temp_question = temp.questions.filter(number=question.number).first()
            if temp_question:
                question.answer = temp_question.answer
                question.save()           
        return redirect('create_esc', pk=pk)  


    with open('yaml/esc/esc.yaml', 'r') as file:
            descriptions = yaml.load(file, Loader=yaml.FullLoader)
    forms = []
    last = ""
    for question in questions:
        form_prefix = f'question-{question.number}'
        form = EscQuestionForm(instance=question, prefix=form_prefix)
        form.description = descriptions.get(question.number, {}).get('text', '')
        form.title = descriptions.get(question.number, {}).get('title', '')
        form.first = False
        form.last = False
        if form.title != last:
            form.first = True
            if forms:
                forms[-1].last = True
        last = form.title
        
        
        forms.append(form)
            

    context = {'sds': sds, 'forms': forms, 'proj': proj, 'templates': temp_list}
    return render(request,'create_esc.html', context)