from django.contrib import admin
from .models import User,Movies,Genres,Trendingmovie


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'modified_at', 'active')
    search_fields = ('username', 'email')
admin.site.register(User, UserAdmin)


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title','tag' ,'poster_url', 'trailer_url', 'rating', 'release_date')
    search_fields = ('title','genres','tag')

admin.site.register(Movies, MovieAdmin)


class GeneresAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Genres, GeneresAdmin)


class TrendingMovieAdmin(admin.ModelAdmin):
    list_display = ('title','tag', 'poster_url', 'trailer_url', 'rating', 'release_date')
    search_fields = ('title','genres','tag')
admin.site.register(Trendingmovie, TrendingMovieAdmin)   
   