import trafilatura
import re

def getData(url):
    downloaded = trafilatura.fetch_url(url)
    result = trafilatura.extract(downloaded)
    return result

def keyword_function(keyword): #키워드 검사 및 데이터 저장
    url = input("URL을 입력하세요.")
    web_doclist = getData(url) # web_doclist 안에 받아올 데이터 문자열 넣기
    sentences = re.sub('[-=.#/?:$}|]', '', str(web_doclist))

    sentences = sentences.split()  # 문자열을 리스트로 변환
    for idx in range(0, len(sentences)):
        if len(sentences[idx]) <= 10:
            sentences[idx - 1] += (' ' + sentences[idx])
    sentences[idx] = ''
    return sentences

def main():
    keyword = input("사용할 keyword를 입력하세요.")
    print(keyword_function(keyword))

if __name__ == '__main__':
  print("program start")
