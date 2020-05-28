import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200403&hh=23&rtm=N&pg=1',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

genie_chart = soup.select('#body-content > div.newest-list > div > table > tbody > tr')

for genie_charts in genie_chart:
    title = genie_charts.select_one('td.info > a.title.ellipsis')
    rank = genie_charts.select_one('td.number')
    singer = genie_charts.select_one('td.info > a.artist.ellipsis')
    if title is not None:
        song_title = title.text.strip()
        song_rank = rank.text[0:2].strip()
        song_singer = singer.text.strip()
        db.users.insert_one({'순위':song_rank,'제목':song_title,'가수':song_singer})
        song_db = list(db.users.find())

for test in song_db:
    print(test['순위']+'위. '+test['제목']+' ['+ test['가수']+']')


