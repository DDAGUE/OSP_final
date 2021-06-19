import requests
import json
from bs4 import BeautifulSoup
import re
import sys

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
        temp_t = re.sub('<b>', '', info['title'])
        temp_t = re.sub('</b>', '', temp_t)
        temp_d = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', ', ', info['director'])
        temp_a = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', ', ', info['actor'])
        api_info = {
            'title': temp_t,
            'director': temp_d,
            'actor': temp_a,
	    'image': info['image'],
        }
        api_movie.append(api_info)
        #print(info['link'])
        #crawling_choice(info['link'])
    print(api_movie)

def crawling_choice(url):
    Name = list()
    genre = list()
    d_a = list()
    story = list()

    # sys.stdout = open('stdout.txt', 'w')

    # url = 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=10016'
    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, 'html.parser')
    temp = []
    movie = html.select("dl.info_spec")

    # 영화 제목
    try:
        name = html.select_one("h3.h_movie a").text
    except:
        name = "None"
        Name.append(name)
    else:
        Name.append(name)

    # 장르 및 감독과 배우
    for m in movie:
        info = m.select("dd a")
        for k in info:
            # print(k)
            if 'genre' in k.attrs["href"]:
                genre.append(k.text)
            elif '/movie/bi/pi/basic.nhn?code=' in k.attrs["href"]:
                d_a.append(k.text)

    # 스토리
    try:
        # title 태그에 정보가 없고 story 에만 정보 있는 경우.
        Story1 = html.select_one("div h5.h_tx_story").get_text()
    except:
        try:
            Story2 = html.select_one("div p.con_tx").get_text()
            Story = Story2
        except:
            Story = "None"
    else:
        Story2 = html.select_one("div p.con_tx").get_text()
        Story = Story1 + " " + Story2

    # Story = Story1 + " " + Story2
    story.append(list(Story))
    story = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', '', Story).split()
    info = {
        'title': Name,
        'genre': genre,
        'director & actor': d_a,
        'story': story
    }
    if info['title'] == "None" or info['story'] == "None":
        error_info.append(url)

