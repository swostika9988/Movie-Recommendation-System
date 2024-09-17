from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import User,Movies,Genres
from django.forms.models import model_to_dict
from django.db.models import Q
from .utils import get_embed_url
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


import random




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
    query = request.GET.get('query')
    genre_filter = request.GET.get('genre')  # Get genre filter if applied
    
    # Get all movie data, filter by genre if provided
    if genre_filter:
        movies = Movies.objects.filter(genres__name__icontains=genre_filter)
    else:
        movies = Movies.objects.all()
    if query:
        # Get all movie data
        movies = Movies.objects.all()
        titles = [movie.title for movie in movies]
        genres = [", ".join([genre.name for genre in movie.genres.all()]) for movie in movies]
        unique_genres = set()

        for movie in movies:
            for genre in movie.genres.all():
                unique_genres.add(genre.name)

        # Convert the set to a sorted list if needed
        unique_genres = sorted(unique_genres)

        descriptions = [movie.tagline if movie.tagline else '' for movie in movies]

        # Combine title, genres, and descriptions for the vectorizer
        documents = [f"{title} {genres} {description}" for title, genres, description in zip(titles, genres, descriptions)]

        # Vectorize the documents and the query
        vectorizer = TfidfVectorizer().fit(documents)
        doc_vectors = vectorizer.transform(documents)
        query_vector = vectorizer.transform([query])

        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, doc_vectors).flatten()
        
        
        # Get the top 5 most similar movies
        top_indices = similarities.argsort()[-16:][::-1]
        top_indices = list(top_indices)
        top_indices = [int(i) for i in top_indices]
        recommended_movies = [movies[i] for i in top_indices]

        

        return render(request, 'search.html', {'movies': recommended_movies, 'query': query, 'genres_list': unique_genres, 'genre_filter': genre_filter })
    else:
        return render(request, 'search.html', {'movies': [], 'query': query})
    
    
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
    
def movie(request,id):
    moives = Movies.objects.get(id=id)
    genres = moives.genres.all()
    related_movie = []
    for gen in genres:
        related_movie.extend(gen.movies.exclude(Q(poster_url__isnull=True) | Q(poster_url='')).filter(tag='trending').order_by('-release_date')[:10])
    related_movie =  random.sample(related_movie, 10)
    context = {
        'movie': moives,
        'related_movies': related_movie
    }
    return render(request,'movie.html',context)


