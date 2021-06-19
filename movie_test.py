import requests
import json

client_id = "sNhNY29KQ_9fggJH6kb4"
client_key = "gN1zdMPlO2"
movie = "장고"

url = f"https://openapi.naver.com/v1/search/movie.json?query={movie}"

header = {
    "X-Naver-Client-Id" : client_id,
    "X-Naver-Client-Secret": client_key
}

r = requests.get(url, headers=header)
data = r.json()


print(data)