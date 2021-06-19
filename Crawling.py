import requests
from bs4 import BeautifulSoup
import re
import sys

movie_list = []
movie_info = []
def url_search():

    # sys.stdout = open('stdout.txt', 'w')
    number = 1
    for num in range(1, 41):
        raw = requests.get("https://movie.naver.com/movie/sdb/rank/"
                           "rmovie.nhn?sel=pnt&date=20210527&page=" + str(num),
                           headers={'User-Agent':'Mozilla/5.0'})
        html = BeautifulSoup(raw.text, 'html.parser')

        movie = html.select("td.title")
        for m in movie:
            title = m.select_one("div.tit5 a")
            # print(title.text)

            url = "https://movie.naver.com" + title.attrs["href"]
            # print(str(number) + " : " + url)
            movie_list.append(url)
            number += 1
    # sys.stdout.close()

def make_info(url):

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

    # # 감독 및 인물
    # for k in movie:
    #     kk = k.select("dd p > a")
    #     print(kk.attrs["href"])
    #     # for kkk in kk:
    #     #     if '/movie/bi/pi/' in k.attrs["href"]:
    #     #         print(kkk)

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

    # Story = Story1 + " " + Story2
    story.append(list(Story))
    story = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\$%&\\\=\(\'\"]', '', Story).split()

    info = {
        'title': Name,
        'genre': genre,
        'director & actor': d_a,
        'story': story
    }
    print(info)
    movie_info.append(info)
    # sys.stdout.close()

if __name__ == "__main__":
    url_search()
    for i in movie_list:
        print(i)
        make_info(i)
    # print(movie_info)