from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
import yaml
import random
from django.db.models import Avg

from frameworks.models import Framework, FrameItem, FrameLevel
from irp_assessment.models import Item, Assessment
from projects.models import Project

@login_required(login_url='signin')
def index(request):
    # Project.objects.all().delete()


    frame = Framework.objects.all()
    if(len(frame) == 0):
        frame = Framework.objects.create(name = "CapAI")
        with open('yaml/assessment/items.yaml', 'r') as file:
            questions = yaml.load(file, Loader=yaml.FullLoader)
            item_count = 0
            for i in questions:
                item = FrameItem()
                item.framework = frame
                item.item_count = item_count + 1
                item.item_nr = i["item_nr"]
                item.stage = i["stage"]
                item.category = i["category"]
                item.respondent = i["respondent"]
                item.description =i["description"]
                item.deliverable_description = i["deliverable"]
                item.save()
                item_count = item_count + 1

        with open('yaml/assessment/capai.yaml', 'r') as file:
            questions = yaml.load(file, Loader=yaml.FullLoader)

           
            for i in questions:
                item = FrameLevel()
                item.item = FrameItem.objects.get(item_nr = i["item_nr"])
                item.name = i["name"]
                item.value = i["value"]
                item.description =i["description"]
                item.save()  
                
    projects = Project.objects.all() 
    assessments = Assessment.objects.all()
    stages = ['Design', 'Development', 'Evaluation', 'Operation', 'Retirement']
    stage_avg = [0, 0, 0, 0, 0]
    project_list = []
    low = 0
    high = 0
    counter = 0
    avg = 0
    for proj in projects:
        proj.color = f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})"
        print (proj.color)
        proj.data_values = [0, 0, 0, 0, 0]
        if proj.assessments.first() is None:
            break
        assessment = proj.assessments.latest('last_updated')  
        proj.avg = Item.objects.filter(assessment=assessment).aggregate(Avg('maturity'))['maturity__avg']
        progress = assessment.items.filter(saved=True).count()
        total = assessment.items.count()
        proj.perc = (progress/total)*100
      
        for i in [0,1,2,3,4]:
            for item in assessment.items.filter(stage__iexact=stages[i]).all():
                if item.saved:
                    proj.data_values[i] += item.maturity
            
            count = assessment.items.filter(stage__iexact=stages[i], saved = True).count()
            if count > 0:
                proj.data_values[i]=proj.data_values[i]/count
            else: proj.data_values[i] = 0
            stage_avg[i] += proj.data_values[i]
        project_list.append(proj)
        
        latest_instance = proj.assessments.latest('last_updated')
        average_maturity = Item.objects.filter(assessment=latest_instance).aggregate(Avg('maturity'))['maturity__avg']
        proj.avg = average_maturity
        if average_maturity != None:
            avg += average_maturity
            counter += 1
            if  average_maturity < 3:
                low += 1  
            if  average_maturity == 5:
                high += 1          
    if counter!= 0:
        avg = avg/counter 
        high = (high/counter)*100 
        low = (low/counter)*100 

    

    if projects.count() != 0:
        for i in range(len(stage_avg)):
            stage_avg[i] = round(stage_avg[i]/projects.count(), 2)
    

    stats ={
        'member': 0,
        'created': 0,  
        'other': 0,
        'assessments': assessments.count(),
        'complete': 0,
        'half': 0,
        'never': 0,
        'avg': avg,
        'high': high,
        'low': low
 
    }
    if projects.count() != 0:
        stats['member'] = (request.user.projects.all().count() / projects.count()) * 100
        stats['other'] = ((projects.count() - request.user.projects.all().count()) / projects.count()) * 100
        stats['created'] = (request.user.created_projects.all().count() / projects.count()) * 100
        if stats['assessments'] != 0:
            comp = 0
            halfcomp = 0
            never = 0
            for assess in assessments:    
                completed = assess.items.all().filter(saved=False).count()
                if  completed == 0:
                    comp+=1
                if completed <= assess.items.all().count()/2 and completed!=0:
                    halfcomp+=1
                elif completed == assess.items.all().count():
                    never += 1

            stats['complete'] = (comp / assessments.count()) * 100
            stats['half'] = (halfcomp / assessments.count()) * 100
            stats['never'] = (never / assessments.count()) * 100
        
        

    
    


 
            
    context = {'projects': project_list, 'stages': stages, 'stage_avg': stage_avg, 'stats': stats}
    return render (request, 'index.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
        
           
    return render(request, 'sign-in-illustration.html')
    
def signout(request):
    logout(request)
    return redirect('signin')
