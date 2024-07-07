from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import User,Movies,Genres
from django.forms.models import model_to_dict

# Create your views here.


def index(request):
    template_name = 'index.html'
    
    
    return render(request,template_name)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    return render(request, 'base.html')

def signup(request):
    if request.method == "POST":
        print(request.POST)
        signupform = signupform(request.POST)
        signup = signupform.save()
        return JsonResponse(model_to_dict(signup))
       
         