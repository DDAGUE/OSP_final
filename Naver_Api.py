import requests
import json

def call_API(words):

    api_movie = []
    
    client_id = "sNhNY29KQ_9fggJH6kb4"
    client_key = "gN1zdMPlO2"
    movie = words

    url = f"https://openapi.naver.com/v1/search/movie.json?query={movie}"

    header = {
        "X-Naver-Client-Id" : client_id,
        "X-Naver-Client-Secret": client_key
    }

    r = requests.get(url, headers=header)
    data = r.json()
    for info in data['items']:
        api_info = {
            'title': info['title'],
            'director': info['director'],
            'actor': info['actor'],
	    'image': info['image'],
        }
        api_movie.append(api_info)

    print(api_movie)
