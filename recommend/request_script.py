import requests
import json


url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"


headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI5M2ZjYTk0N2QzZjgwM2VhZDU2Mzk1YmJiYTEyMWYyZSIsIm5iZiI6MTcxOTU4MjM5Mi43NDI0NjYsInN1YiI6IjY2N2QzY2VjYTVjNDA3ZDMxMzExZjI2MiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.17br821iXdkqIYSX9r9YZwp7gcG0si8yNU_znx9or70",
    "accept": "application/json"
}

response = requests.get(url, headers=headers)


if response.status_code == 200:
   
    response_data = response.json()  
    print(response_data)
    
    
    with open('response.json', 'w') as file:
        json.dump(response_data, file, indent=4)
else:
    print(f"Failed to get response: {response.status_code}, {response.text}")
