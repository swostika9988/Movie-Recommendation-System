from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet,ReviewViewSet,UserDashboardChartViewsets

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register('review',ReviewViewSet,basename='review')
router.register('charts',UserDashboardChartViewsets,basename='charts')



urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('', include(router.urls)), 
    path('search/', views.search, name='search'),
    path('movie/<id>',views.movie,name='movie'),
    path('dashboard',views.dashboard,name='dashboard'),
]