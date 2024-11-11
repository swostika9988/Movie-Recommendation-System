from django.contrib import admin
from django.urls import path,include, re_path
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet,ReviewViewSet,UserDashboardChartViewsets,MovieViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register('review',ReviewViewSet,basename='review')
router.register('charts',UserDashboardChartViewsets,basename='charts')
router.register(r'movies', MovieViewSet, basename='movies')



urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('', include(router.urls)), 
    path('search/', views.search, name='search'),
    path('movie/<id>',views.movie,name='movie'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('dashboard/watch_history',views.watch_history,name='watch_history'),
    path('dashboard/rating_review',views.rating_movie,name='rating_movie'),
    path('dashboard/time_spend',views.time_spent,name='time_spent'),
    path('dasbhoard/watched_genres',views.watch_genres,name='watch_genres'),
    re_path(r'^dashboard/add-edit-movie/(?P<id>\d+)?$',views.add_edit_movie,name='add_edit_movie'),
    re_path(r'^dashboard/movie-listing/(?P<id>\d+)?$', views.movie_listing, name='movie_listing'),
    path('logout',views.logout,name='logout'),
]