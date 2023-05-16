from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import yaml


from .models import Template, TempQuestion, SDS
from projects.models import Project
from .forms import TemplateForm, QuestionForm, SDSQuestionForm

# Create your views here.
@login_required(login_url='signin')
def sds(request):
    project_list = Project.objects.filter(status = "active")
    temp_list = Template.objects.all()
    
    if request.method == 'POST':
        form = TemplateForm(request.POST or None)        
        if form.is_valid():
            temp = form.save(commit=False)
            temp.creator = request.user
            temp.save()

            for i in range(1, 13):
                tempq = TempQuestion()
                tempq.template = temp
                tempq.number = i
                tempq.save()
        return redirect("temp/" + str(temp.id))
    else:
        form = TemplateForm()

    context = {'projects': project_list, 'templates': temp_list, 'form': form}
    return render(request,'sds_overview.html', context)

@login_required(login_url='signin')
def create_sds(request, pk): 
    action = request.POST.get('action')
    proj = get_object_or_404(Project, pk=pk)
    sds = get_object_or_404(SDS, pk=proj.sds.id)
    questions = sds.questions.all()
    temp_list = Template.objects.all()

    if request.method == 'POST' and action == 'save-sds':     
        for question in questions:
            form_prefix = f'question-{question.number}'
            form = SDSQuestionForm(request.POST, instance=question, prefix=form_prefix)
            
            if form.is_valid():
                form.save()
        return redirect('create_sds', pk=pk)
    
    if request.method == 'POST' and action == 'load-temp':
        template_id = request.POST.get('template_id')
        temp = get_object_or_404(Template, pk=template_id)       
        for question in sds.questions.all():
            temp_question = temp.questions.filter(number=question.number).first()
            if temp_question:
                question.answer = temp_question.answer
                question.save()           
        return redirect('create_sds', pk=pk)  


    with open('yaml/sds/sds.yaml', 'r') as file:
        descriptions = yaml.load(file, Loader=yaml.FullLoader)
    forms = []
    for question in questions:
        form_prefix = f'question-{question.number}'
        form = SDSQuestionForm(instance=question, prefix=form_prefix)
        form.description = descriptions.get(question.number, {}).get('text', '')
        form.title = descriptions.get(question.number, {}).get('title', '')
        forms.append(form)
            

    context = {'sds': sds, 'forms': forms, 'proj': proj, 'templates': temp_list}
    return render(request,'create_sds.html', context)

@login_required(login_url='signin')
def delete_temp(request, pk):
    temp = Template.objects.get(pk=pk)
    temp.delete()
    return redirect('/sds')


@login_required(login_url='signin')
def temp(request, pk):
    action = request.POST.get('action')
    template = get_object_or_404(Template, pk=pk)
    questions = template.questions.all()

    if request.method == 'POST' and action == 'save-sds':     
        for question in questions:
            form_prefix = f'question-{question.number}'
            form = QuestionForm(request.POST, instance=question, prefix=form_prefix)
            
            if form.is_valid():
                form.save()
        return redirect('temp', pk=pk)  


    with open('yaml/sds/sds.yaml', 'r') as file:
            descriptions = yaml.load(file, Loader=yaml.FullLoader)
    forms = []
    for question in questions:
        form_prefix = f'question-{question.number}'
        form = QuestionForm(instance=question, prefix=form_prefix)
        form.description = descriptions.get(question.number, {}).get('text', '')
        form.title = descriptions.get(question.number, {}).get('title', '')
        forms.append(form)
            

    context = {'template': template, 'forms': forms}
    return render(request,'sds_template.html', context)



