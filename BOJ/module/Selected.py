import requests
from bs4 import BeautifulSoup
import re

def make_info(url):

    Name = list()
    genre = list()
    d_a = list()
    story = list()

    # sys.stdout = open('stdout.txt', 'w')

    raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = BeautifulSoup(raw.text, 'html.parser')
    movie = html.select("dl.info_spec")

    # 영화 제목
    name = html.select_one("h3.h_movie a").text
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
        Story2 = html.select_one("div p.con_tx").get_text()
        Story = Story2
    else:
        Story2 = html.select_one("div p.con_tx").get_text()
        Story = Story1 + " " + Story2

    story.append(list(Story))
    story = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', '', Story).split()

    info = {
        'title': Name,
        'genre': genre,
        'director & actor': d_a,
        'story': story
    }
    return info
