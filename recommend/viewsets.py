from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from .models import User,Reviews,Movies,WatchHistory,Genres
from .serializers import UserSerializer,ReviewsSerializer,MovieSerializer
from django.template.loader import render_to_string
from django.db.models import Count
import datetime
from django.db.models import Sum

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()  # select * from user table where username=username
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username) # select * from user table where username=username
            if check_password(password, user.password): # user.password
                serializer = self.get_serializer(user)
                # create user session after login 
                request.session['user'] = user.username
                request.session['password'] = password
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        # delete session 
        del request.session['user']
        return Response({'message':'logout successfully'})
    
    @action(detail=False, methods=['post'], url_path='check_user_session')
    def check_user_session(self,request):
        if request.session.has_key('user'):
            return Response({'status': True})
        else:
            return Response({'status': False})
        
class ReviewViewSet(viewsets.GenericViewSet):
    queryset = Reviews.objects.all()  # select * from user table where username=username
    serializer_class = ReviewsSerializer

    def get_all_review(self,movie_id,user):
        movie = Movies.objects.get(id=movie_id)
        queryset = self.queryset.filter(movie=movie).order_by('-id')
        html_string = render_to_string('ajax_review.html', {'reviews': queryset,'total': len(queryset),'user': user})
        return html_string
        
    @action(detail=False, methods=['post'], url_path='write_review')
    def write_review(self,request):
        if request.session.has_key('user'):
            username = request.session['user']
            user = User.objects.get(username=username)
            data = request.data
            data.update({'user': user.id})
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # Get all reviews
                html = self.get_all_review(movie_id=data['movie'],user=user)
                return Response({'html': html}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='watch_movie')
    def watch_movie(self,request):
        data = request.data
        movie_id = data['movie']
        movie = Movies.objects.get(id=movie_id)
        username = request.session['user']
        user = User.objects.get(username=username)
        watch = WatchHistory.objects.filter(user=user,movie=movie)
        if watch.exists():
            watch = watch.last()
            watch.count = watch.count + 1
        else:
            watch = WatchHistory(user=user,movie=movie)
        watch.save()
        return Response({'message':'user watch added'},status=status.HTTP_201_CREATED)


class UserDashboardChartViewsets(viewsets.GenericViewSet):

    def get_watch_history(self,user):
        today = datetime.date.today()
        last_30_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

        # Fetch the movie count for each day in the last 30 days
        watch_history = WatchHistory.objects.filter(
            user=user, 
            created_at__date__gte=today - datetime.timedelta(days=30)
        ).values('created_at__date').annotate(
            total_movies_watched=Sum('count')
        ).order_by('created_at__date')

        # Prepare the default movie data (set count to 0 for days with no movies)
        movie_data = {day: 0 for day in last_30_days}

        # Update movie_data with the actual counts from the query
        for entry in watch_history:
            day = entry['created_at__date'].strftime('%Y-%m-%d')
            movie_data[day] = entry['total_movies_watched']

        # Prepare the data for the chart
        x = list(movie_data.keys())  # x-axis: list of dates (last 30 days)
        y = list(movie_data.values())  # y-axis: list of movie counts
        return x,y

    def get_genres_data(self,user):
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

        # Prepare the data for the chart
        x = [genre.name for genre in genre_counts]  # Genre names for the x-axis
        y = [genre.num_movies_watched for genre in genre_counts]  # Count of movies per genre for the y-axis

        return x,y
    
    def get_time_spent(self,user):
        today = datetime.date.today()
        last_30_days = [(today - datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]

        # Set an average movie duration (in minutes)
        average_movie_duration = 120  # 120 minutes

        # Get total count of movies watched per day for the last 30 days
        watch_data = WatchHistory.objects.filter(
            user=user,
            created_at__date__gte=today - datetime.timedelta(days=30)
        ).values('created_at__date').annotate(
            total_movies_watched=Sum('count')
        ).order_by('created_at__date')

        # Initialize a dictionary to store time spent (default 0 for days with no data)
        time_spent_data = {day: 0 for day in last_30_days}

        # Update time_spent_data with actual values
        for entry in watch_data:
            day = entry['created_at__date'].strftime('%Y-%m-%d')
            total_time_spent = entry['total_movies_watched'] * average_movie_duration
            time_spent_data[day] = total_time_spent

        # Prepare data for the chart
        x = list(time_spent_data.keys())  # x-axis: last 30 days
        y = list(time_spent_data.values())  # y-axis: time spent (in minutes)

        return x,y
    
    def get_ratings(self,user):
        # Get the count of each rating (1 to 5) for the logged-in user
        rating_counts = Reviews.objects.filter(user=user).values('rating').annotate(
            count=Count('rating')
        ).order_by('rating')

        # Prepare the data for the chart
        x = [entry['rating'] for entry in rating_counts]  # Ratings (e.g., 1, 2, 3, 4, 5)
        y = [entry['count'] for entry in rating_counts]  # Count of ra
        return x,y

    @action(detail=False, methods=['get'], url_path='user_data')
    def charts_data(self,request):
        # Get watch hsitroy data
        username = request.session['user']
        user = User.objects.get(username=username)
        watch_x,watch_y = self.get_watch_history(user=user)
        genres_x,genres_y = self.get_genres_data(user=user)
        time_x,time_y = self.get_time_spent(user=user)
        rating_x,rating_y = self.get_ratings(user=user)
        context = {
            'watch_histroy': {'x':watch_x,'y': watch_y},
            'genres_data': {'x': genres_x,'y': genres_y},
            'time_spent': {'x': time_x,'y': time_y},
            'rating': {'x': rating_x,'y': rating_y}
        }
        return Response(context,status=200)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer

