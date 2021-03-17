import telegram
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

# json = requests.get('https://www.naver.com/srchrank?frm=main').json()

# # json 데이터에서 "data" 항목의 값을 추출
# ranks = json.get("data")
# keywordList=[]
# helloList=['안녕','hello']

# # 해당 값은 리스트 형태로 제공되기에 리스트만큼 반복
# for r in ranks:
#     # 각 데이터는 rank, keyword, keyword_synomyms
#     rank = r.get("rank")
#     keyword = r.get("keyword")
#     keywordList.append(keyword+"")
 

# print(keywordList)

def hello():
    bot = telegram.Bot(token='1429113658:AAEi5BmzzzV4jGKXWE3z8GabcA5MGSiVOgg')

    bot.send_message(chat_id=1412750462, text="hello")