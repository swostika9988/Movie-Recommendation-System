from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import User,Movies,Genres,Reviews
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .utils import get_embed_url
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import datetime
from django.db.models import Sum,Count
from django.contrib import messages
from .models import (
    WatchHistory,
    Reviews,
    MOVIE_TAG
)
from django.db.models import Avg
import random
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from .serializers import MovieSerializer

# Create your views here.

# ************************* Content base filter - genres and actor ****************

def content_based_recommendation(movie_id):
    # Get the movie the user is currently viewing
    movie = Movies.objects.get(id=movie_id)

    # Combine relevant features (genres, actors) to form the "content" of the movie
    def get_content(movie):
        genres = [item.name for item in movie.genres.all()]
        genres = ','.join(genres)
        return f"{genres} {movie.actors}"

    # Get all movies to compare with
    all_movies = Movies.objects.exclude(poster_url__isnull=True).exclude(trailer_url__isnull=True)

    # Prepare data for similarity calculation
    movies_content = [get_content(m) for m in all_movies]
    
    # Convert text to matrix of token counts
    vectorizer = CountVectorizer().fit_transform(movies_content)
    
    # Calculate cosine similarity between movies
    cosine_sim = cosine_similarity(vectorizer)
    
    # Find the index of the current movie
    movie_idx = list(all_movies).index(movie)
    
    # Get similarity scores for this movie
    sim_scores = list(enumerate(cosine_sim[movie_idx]))
    
    # Sort by similarity score and get top 10 movies
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    
    # Get the movie objects for the recommendations
    recommended_movies = [all_movies[i[0]] for i in sim_scores]
    return recommended_movies

# ************************** Collabrative Filter ***********************

def collaborative_filtering(user):
    # Get the current user's reviews
    current_user_reviews = Reviews.objects.filter(user=user)

    # Get all other users' reviews
    all_reviews = Reviews.objects.exclude(user=user)
    
    # Create a dictionary to store user similarities
    user_similarity = {}

    # Compare current user's reviews with other users
    for review in current_user_reviews:
        movie_reviews = all_reviews.filter(movie_id=review.movie.id)
        for other_review in movie_reviews:
            if other_review.user_id not in user_similarity:
                user_similarity[other_review.user_id] = []
            # Calculate similarity based on rating difference
            user_similarity[other_review.user_id].append(
                abs(review.rating - other_review.rating)
            )
    
    # Calculate average similarity score for each user
    user_similarity = {k: np.mean(v) for k, v in user_similarity.items()}

    # Get the top N most similar users (lowest difference in ratings)
    similar_users = sorted(user_similarity, key=user_similarity.get)[:5]
    
    # Recommend movies based on these similar users' reviews
    similar_user_reviews = Reviews.objects.filter(user_id__in=similar_users).exclude(movie_id__in=current_user_reviews.values('movie_id'))
    # Get movies that have high ratings from similar users
    similar_reviews = similar_user_reviews.values('movie_id').annotate(average_rating=Avg('rating')).order_by('-average_rating')[:10]
    # Get all movie ids 
    movie_ids = [item['movie_id'] for item in similar_reviews]
    recommended_movies = Movies.objects.filter(id__in=movie_ids)
    return recommended_movies



def index(request):
    template_name = 'index.html'
    # template_name = 'demo.html'
    movies_obj = Movies.objects.exclude(poster_url__isnull=True).exclude(trailer_url__isnull=True).order_by('-release_date')
    movie_list = movies_obj[:10]
    popular_movies = movies_obj.filter(tag='popular').order_by('-popularity')[:10]
    coming_soon_movies = movies_obj.filter(tag='coming_soon').order_by('release_date')[:10]
    top_rated_movies = movies_obj.filter(tag='top_rated').order_by('-rating')[:10]
    most_reviewed_movies = movies_obj.filter(tag='most_reviewed')[:10]
    if request.session.has_key('user'):
        username = request.session['user']
        user = User.objects.get(username=username)
        collaborative_content = collaborative_filtering(user=user)
    else:
        collaborative_content = []
    # get all record of movies having movie_urls
    # find the section of trailer in index.html
    # use foor loop to list all the trailers in traier section of index.html
    trailer_urls = Movies.objects.exclude(Q(trailer_url__isnull=True) | Q(trailer_url='')).order_by('-release_date')[:10]
    for movie in trailer_urls:
        movie.trailer_url = get_embed_url(movie.trailer_url)
    context = {
        'movie_lists': movie_list,
        'popular_movies': popular_movies,
        'coming_soon_movies': coming_soon_movies,
        'top_rated_movies': top_rated_movies,
        'most_reviewed_movies': most_reviewed_movies, # 15
        'movie_urls': trailer_urls,
        'collaborative_content': collaborative_content
        
    }
    return render(request,template_name,context)



def search(request):
    query = request.GET.get('query')
    genre_filter = request.GET.get('genre')  # Get genre filter if applied
    genres_list = request.GET.getlist('movie_list',None)
    movies_obj = Movies.objects.exclude(poster_url__isnull=True).exclude(trailer_url__isnull=True)
    # Get all movie data, filter by genre if provided
    if genre_filter:
        movies = movies_obj.filter(genres__name__icontains=genre_filter)[:24]
    elif genres_list:
        print(f'genres lsit : {genres_list}')
        q = Q()
        for genre in genres_list:
            if isinstance(genre, str) and genre.strip():
                q |= Q(genres__name__contains=genre)
        movies = movies_obj.filter(q).distinct()[:24]
    else:
        movies = movies_obj
        # Get all movie data
    titles = [movie.title for movie in movies]
    genres = [", ".join([genre.name for genre in movie.genres.all()]) for movie in movies]
    unique_genres = set()
    for movie in movies:
        for genre in movie.genres.all():
            unique_genres.add(genre.name)

    # Convert the set to a sorted list if needed
    unique_genres = sorted(unique_genres)

    # using vector and similiartie for query
    if query:
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
    else:
        recommended_movies = movies

    return render(request, 'search.html', {'movies': recommended_movies,'total_movie': len(recommended_movies), 'query': query, 'genres_list': unique_genres, 'genre_filter': genre_filter })
    
    
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
    
def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return redirect('index')
    
def movie(request,id):
    moives = Movies.objects.get(id=id)
    genres = moives.genres.all()
    reviews = moives.reviews_set.all().order_by('-id')
    username = request.session['user']
    user = User.objects.get(username=username)
    related_movie = content_based_recommendation(id)
    # related_movie = []
    # for gen in genres:
    #     related_movie.extend(gen.movies.exclude(Q(poster_url__isnull=True) | Q(poster_url='')).filter(tag='trending').order_by('-release_date')[:10])
    # related_movie =  random.sample(related_movie, 10)
    context = {
        'movie': moives,
        'related_movies': related_movie,
        'reviews': reviews,
        'user': user,
        'total_review': len(reviews)
    }
    return render(request,'movie.html',context)







# ************************** User Dashboard ******************************


def dashboard(request):
    template_name = 'dashboard/dashboard.html'
    return render(request,template_name)

def watch_history(request):
    username = request.session['user']
    user = User.objects.get(username=username)
    history = WatchHistory.objects.filter(user=user)
    template_name = 'dashboard/watch_history.html'
    context = {
        'history': history
    }
    return render(request,template_name,context)

def time_spent(request):
    username = request.session['user']
    user = User.objects.get(username=username)
    history = WatchHistory.objects.filter(user=user)
    template_name = 'dashboard/time_spent.html'
    context = {
        'history': history
    }
    return render(request,template_name,context)

def rating_movie(request):
    username = request.session['user']
    user = User.objects.get(username=username)
    reviews = Reviews.objects.filter(user=user)
    template_name = 'dashboard/rating.html'
    context = {
        'history': reviews
    }
    return render(request,template_name,context)

def watch_genres(request):
    username = request.session['user']
    user = User.objects.get(username=username)
    today = datetime.date.today()
    last_30_days = today - datetime.timedelta(days=30)
    # Get all watched movies by the user in the last 30 days
    watched_movies = WatchHistory.objects.filter(
        user=user,
        created_at__date__gte=last_30_days
    ).values('movie_id').distinct()

    # Get genres for those movies and count how many times each genre was watched
    genre_counts = Genres.objects.filter(
        movies__id__in=watched_movies
    ).annotate(
        num_movies_watched=Count('movies')
    ).order_by('-num_movies_watched')
    template_name = 'dashboard/watch_genres.html'
    context = {
        'history': genre_counts
    }
    return render(request,template_name,context)


def add_edit_movie(request,id=None):
    template_name = 'dashboard/movie.html'
    method = request.method
    movie = None
    serializer = None
    if id and method in ['post','POST']:
        movie_instance = get_object_or_404(Movies, id=id)
        serializer = MovieSerializer(movie_instance, data=request.POST)
    elif method in ['post','POST']:
        serializer = MovieSerializer(data=request.POST)

    if serializer:
        if serializer.is_valid():
            movie = serializer.save()
            messages.success(request, 'Movie saved successfully!')
        else:
            # Display an error message with the validation errors
            messages.error(request, f'Failed to save movie. Errors: {serializer.errors}')
    if id:
        movie = Movies.objects.get(id=id)
    genres = Genres.objects.all()
    context = {
        'genres': genres,
        'MOVIE_TAG': MOVIE_TAG,
        'movie': movie

    }
    return render(request,template_name,context)


def movie_listing(request,id=None):
    template_name = 'dashboard/movie_list.html'
    # delete movie and return the rest of movie
    if request.method in ['post','POST'] and id:
        res = Movies.objects.get(ikd=id)
        res.delete()
    
    movies =  Movies.objects.exclude(poster_url__isnull=True).exclude(trailer_url__isnull=True).exclude(rating=0).order_by('-release_date')[:1000]
    context = {
        'movies': movies
    }
    return render(request,template_name,context)