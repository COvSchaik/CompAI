from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='signin')
def index(request):
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
