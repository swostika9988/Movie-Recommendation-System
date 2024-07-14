from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import User,Movies,Genres
from django.forms.models import model_to_dict
from django.db.models import Q

# Create your views here.


def index(request):
    template_name = 'index.html'
    movie_list = Movies.objects.exclude(Q(poster_url__isnull=True) | Q(poster_url='')).filter(tag='trending').order_by('-release_date')
    # get all record of movies having trailer_url
    # find the section of trailer in index.html
    # use foor loop to list all the trailers in traier section of index.html
    
    context = {
        'movie_lists': movie_list[:15], # 15
    }
    return render(request,template_name,context)

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
       
         