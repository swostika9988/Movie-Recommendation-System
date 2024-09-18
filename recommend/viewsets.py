from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
from .models import User,Reviews,Movies,WatchHistory
from .serializers import UserSerializer,ReviewsSerializer
from django.template.loader import render_to_string

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


