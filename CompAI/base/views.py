from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
import yaml

from frameworks.models import Framework, FrameItem, FrameLevel

@login_required(login_url='signin')
def index(request):
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

    return render (request, 'index.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password= password)
        if user is not None:
            login(request, user)
            print(password, username)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
        
           
    return render(request, 'sign-in-illustration.html')
    
def signout(request):
    logout(request)
    return redirect('signin')
