from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User,Movies,Genres,Trendingmovie


'''
seralizer method:
1. serializer
2. methodseralizer

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.filter(username=validated_data['username'])
        if user:
            raise serializers.ValidationError(f'Username already exists .. ')
        return super(UserSerializer, self).create(validated_data)



class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(queryset=Genres.objects.all(), many=True, allow_empty=True, required=False)

    class Meta:
        model = Movies
        fields = '__all__'

    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        movie = Movies.objects.create(**validated_data)
        movie.genres.set(genres_data)
        return movie

class TrendingSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(queryset=Genres.objects.all(), many=True, allow_empty=True, required=False)

    class Meta:
        model = Trendingmovie
        fields = '__all__'
    
    def create(self, validated_data):
        genres_data = validated_data.pop('genres', [])
        movie = Trendingmovie.objects.create(**validated_data)
        movie.genres.set(genres_data)
        return Trendingmovie
    
    
    
    
    
    
    
    
    
