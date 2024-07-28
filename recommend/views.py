from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import User,Movies,Genres
from django.forms.models import model_to_dict
from django.db.models import Q
from .utils import get_embed_url




# Create your views here.


def index(request):
    template_name = 'index.html'
    movie_list = Movies.objects.exclude(Q(poster_url__isnull=True) | Q(poster_url='')).filter(tag='trending').order_by('-release_date')
    popular_movies = Movies.objects.filter(tag='popular').order_by('-popularity')[:10]
    coming_soon_movies = Movies.objects.filter(tag='coming_soon').order_by('release_date')[:10]
    top_rated_movies = Movies.objects.filter(tag='top_rated').order_by('-rating')[:10]
    most_reviewed_movies = Movies.objects.filter(tag='most_reviewed')[:15]

    # get all record of movies having trailer_url
    # find the section of trailer in index.html
    # use foor loop to list all the trailers in traier section of index.html
    trailer_urls = Movies.objects.exclude(Q(trailer_url__isnull=True) | Q(trailer_url='')).order_by('-release_date')
    for movie in trailer_urls:
        movie.trailer_url = get_embed_url(movie.trailer_url)
        
 
    context = {
        'movie_lists': movie_list[:15],
        'popular_movies': popular_movies,
        'coming_soon_movies': coming_soon_movies,
        'top_rated_movies': top_rated_movies,
        'most_reviewed_movies': most_reviewed_movies, # 15
        'movie_urls': trailer_urls[:30]
        
    }
    return render(request,template_name,context)


def search(request):
    query = request.GET.get('q')
    if query:
        search = Movies.objects.filter(
            Q(title__icontains=query) |
            Q(tag__icontains=query) |
            Q(genres__name__icontains=query)  # Ensure this line is correct
        ).distinct()
    else:
        search = Movies.objects.none()

    for movie in search:
        movie.trailer_url = get_embed_url(movie.trailer_url)


    context = {
        'search': search,
        'query': query
    }
    return render(request, 'search.html', context)
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
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        print(request.POST)
        signupform = signupform(request.POST)
        signup = signupform.save()
        return JsonResponse(model_to_dict(signup))

