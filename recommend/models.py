from django.db import models

# Create your models here.

class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

# create table for user

class User(DateTimeModel):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,null=True)
    
    def __str__(self) -> str:
        return f'{self.username}'
   

MOVIE_TAG = (
    ('normal','normal'),
    ('popular','popular'),
    ('upcomming','upcomming'),
    ('top_rated','top_rated'),
    ('most_reviewd','most_reviewd'),
)


class Genres(DateTimeModel):
    name = models.CharField(max_length=30)
    
    def __str__(self) -> str:
        return f'{self.name}'
    

class Movies(DateTimeModel):
    title = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=300,null=True,blank=True)
    trailer_url = models.CharField(max_length=300,null=True,blank=True)
    actors = models.CharField(max_length=300,null=True,blank=True)
    release_date = models.DateField(null=True,blank=True)
    rating = models.FloatField(default=0)
    poster_path = models.CharField(max_length=300,null=True,blank=True)
    adult = models.BooleanField(default=False)
    budget = models.FloatField(default=0)
    homepage = models.CharField(max_length=300,null=True,blank=True)
    imdb_id = models.CharField(max_length=50, null=True,blank=True)
    popularity = models.FloatField(default=0)
    revenue = models.FloatField(default=0)
    runtime = models.IntegerField(default=0)
    status = models.CharField(max_length=20,null=True,blank=True)
    tagline = models.CharField(max_length=200,null=True,blank=True)
    vote_count = models.FloatField(default=0)
    vote_average = models.FloatField(default=0)
    genres = models.ManyToManyField(Genres,related_name='movies')
    tag = models.CharField(choices=MOVIE_TAG,default='normal',max_length=30)
    
    def __str__(self) -> str:
        return f'{self.title}'
    
    
    
    
    
    
    
    

    


