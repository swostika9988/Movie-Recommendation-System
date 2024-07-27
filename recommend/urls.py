from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('',views.index,name='index'),
    path('login/', views.login, name='login'),
    path('signup/',views.signup, name='signup'),
    path('', include(router.urls)), 
    path('search/', views.search, name='search'),  
]