import json
import os
path = '/Users/daud.ibrahim/Documents/Learning/movie_recom/Movie-Recommendation-System/movies_dataset_2014_2024.jsonl'

generes_list = []

def read_json_file(file):
    with open(file, "r") as r:
        response = r.read()
        response = response.replace('\n', '')
        response = response.replace('}{', '},{')
        response = "[" + response + "]"
        return json.loads(response)

data = read_json_file(path)

print('processing ...')
            
from recommend.models import Genres
from recommend.serializers import MovieSerializer

all_gen = Genres.objects.all()
gen_map = {}
for item in all_gen:
    gen_map[item.name] = item.id


for idx,item in enumerate(data):
    item['genres'] = [gen_map[k] for k in item['genres'].split(',')]
    item['release_date'] = item['release_date'] if len(item['release_date']) > 2 else None
    serailzer = MovieSerializer(data=item)
    if serailzer.is_valid():
        serailzer.save()
    else:
        print(idx)

print('Generes table is populated successfully')
    