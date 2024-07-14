from django.contrib import admin
from .models import User,Movies,Genres,Trendingmovie


# Register your models here.

admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created_at', 'modified_at', 'active')
    search_fields = ('username', 'email')
    
admin.site.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster_url', 'trailer_url', 'rating', 'release_date')
    search_fields = ('title',)


admin.site.register(Genres)
class GeneresAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Trendingmovie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'poster_url', 'trailer_url', 'rating', 'release_date')
    search_fields = ('title',)    
   