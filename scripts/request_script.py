import requests
import json
from recommend.serializers import MovieSerializer
from recommend.models import Genres

api_key = '93fca947d3f803ead56395bbba121f2e'
import time

def get_genres():
    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'
    response = requests.get(url)
    data = response.json()
    genres = {genre['id']: genre['name'] for genre in data['genres']}
    return genres

def run():

    generes = get_genres()

    url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"


    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5M2ZjYTk0N2QzZjgwM2VhZDU2Mzk1YmJiYTEyMWYyZSIsIm5iZiI6MTcxOTU4MjM5Mi43NDI0NjYsInN1YiI6IjY2N2QzY2VjYTVjNDA3ZDMxMzExZjI2MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.17br821iXdkqIYSX9r9YZwp7gcG0si8yNU_znx9or70",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
    
        response_data = response.json()  
        
        for item in response_data['results']:
            geners = [generes.get(gen,'') for gen in item.get('genre_ids',[])]
            geners_ids = []
            for gen in geners:
                pk = Genres.objects.get(name=gen)
                geners_ids.append(pk.id)
            data = {
                "movie_id": item['id'],
                'title': item['title'],
                'poster_url': f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
                'trailer_url': None,
                'actors': None,
                'release_date': item['release_date'],
                'ratings': item['vote_average'],
                'poster_path': item['poster_path'],
                'genres': geners_ids,
                'adult': item['adult'],
                'tag': 'trending',
                'budget': None,
                'homepage': None,
                'imdb_id': item.get('imdb_id', ''),
                'popularity': item['popularity'],
                'revenue':None,
                'runtime': None,
                'status': None,
                'tagline':None,   
                'vote_count' : item['vote_count'],
            }
            serailzer = MovieSerializer(data=data)
            if serailzer.is_valid():
                print(data["title"])
                serailzer.save()
            else:
                print(f"Error saving movie: {serailzer.errors}")

        with open('response.json', 'w') as file:
            json.dump(response_data['results'], file, indent=4)
    else:
        print(f"Failed to get response: {response.status_code}, {response.text}")
