import requests
import json
from recommend.serializers import TrendingSerializer


url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5M2ZjYTk0N2QzZjgwM2VhZDU2Mzk1YmJiYTEyMWYyZSIsIm5iZiI6MTcxOTU4MjM5Mi43NDI0NjYsInN1YiI6IjY2N2QzY2VjYTVjNDA3ZDMxMzExZjI2MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.17br821iXdkqIYSX9r9YZwp7gcG0si8yNU_znx9or70",
    "accept": "application/json"
}

response = requests.get(url, headers=headers)


if response.status_code == 200:
   
    response_data = response.json()  
    print(response_data)
    
    for item in response_data['results']:
        data = {
                    'title': item['title'],
                    'poster_url': f"https://image.tmdb.org/t/p/w500{item['poster_path']}",
                    'trailer_url': None,
                    'actors': None,
                    'release_date': item['release_date'],
                    'ratings': item['vote_average'],
                    'poster_path': item['poster_path'],
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
        serailzer = TrendingSerializer(data=item)
    if serailzer.is_valid():
        serailzer.save()
    else:
        print(f"Error saving movie: {TrendingSerializer.errors}")

    with open('response.json', 'w') as file:
        json.dump(response_data['results'], file, indent=4)
else:
    print(f"Failed to get response: {response.status_code}, {response.text}")
