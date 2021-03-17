import time
import telegram
import requests
from telegram import ChatAction, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from urllib.request import urlopen
from bs4 import BeautifulSoup
import geocoder
from selenium import webdriver

BOT_TOKEN='1429113658:AAEi5BmzzzV4jGKXWE3z8GabcA5MGSiVOgg'
 
updater = Updater( token=BOT_TOKEN, use_context=True )
dispatcher = updater.dispatcher
g=geocoder.ipinfo('me')
ftitle=[]
fno=[]
movie_photo_list=[]
age_list=[]
reserv_list=[]
genre_list=[]
score_list=[]
near_theater_list=[]
latitude = g.lat
longitude = g.lng

bot = telegram.Bot(token=BOT_TOKEN)
bot.send_message(
    chat_id=1412750462
    , text='환영합니다. 아래의 서비스 사용 명령어를 확인하세요'
    +'\n'+'실시간 영화 순위 확인 : /chart'
    +'\n'+'현재위치 확인 : /location'
    +'\n'+'상영중인 영화 포스터 및 정보(상위 10개) : /info'
    +'\n'+'가장 가까운 영화관 확인 : /near'
    )


#실시간 영화 순위
def cmd_task_buttons_1(update, context):
    context.bot.send_message(
            chat_id=update.message.chat_id
            , text="실시간 영화 순위입니다."
        )
    ftitle=real_time_movie_chart()
    context.bot.send_message(
            text="\n".join(ftitle)
            , chat_id=update.message.chat_id
        )

#현재 위치 반환
def cmd_task_buttons_3(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id
        , text="사용자님의 현재 위치입니다."
        )
    context.bot.send_location(
        chat_id=update.message.chat_id
        , latitude=latitude
        , longitude=longitude)


#가장 가까운 영화관
def cmd_task_buttons_2(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id
        , text="가장 가까운 영화관 목록을 불러오는 중입니다. 조금만 기다려주세요."
    )
    near_theater_list=near_theater();
    task_buttons = [
        [
            InlineKeyboardButton( near_theater_list[0], callback_data=1 )
        ],
        [
            InlineKeyboardButton( near_theater_list[1], callback_data=2 )
        ],
        [
            InlineKeyboardButton( near_theater_list[2], callback_data=3 )
        ]
    ]
    reply_markup = InlineKeyboardMarkup( task_buttons )
    
    context.bot.send_message(
        chat_id=update.message.chat_id
        , text="가장 가까운 영화관 목록입니다."
        , reply_markup=reply_markup
    )


# def cb_button_2(update, context):
#     query = update.callback_query
#     data = query.data

    
#     context.bot.send_chat_action(
#         chat_id=update.effective_user.id
#         , action=ChatAction.TYPING
#     )
    
#     if data == '1':
#         location=theater_location(data)
#         context.bot.send_message(
#             url=location
#             , chat_id=query.message.chat_id
#         )
    
#     else:
#         context.bot.edit_message_text(
#             text='잘못된 입력입니다.'
#             , chat_id=query.message.chat_id
#             , message_id=query.message.message_id
#         )
    


#영화 상영정보
def cmd_task_buttons_4(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id
        , text="상위 10개 영화 포스터 및 정보입니다."
        )
    movie_photo_list=movie_img()
    ftitle=real_time_movie_chart()
    age_list=movie_age()
    reserv_list=movie_reserv_rate()
    genre_list=movie_genre()
    score_list=movie_score()
    for i in range(0,10):
        context.bot.send_photo(
            chat_id=1412750462
            , photo=movie_photo_list[i]
        )
        context.bot.send_message(
            chat_id=1412750462
            ,  text=ftitle[i]+"\n"
            +"영화 관람 등급 : "+age_list[i]+"\n"
            +"영화 예매율 : "+reserv_list[i]+"%"+"\n"
            +"영화 장르 : "+genre_list[i]+"\n"
            +"영화 평점 : "+score_list[i]+"\n"
        )





#함수
#영화 순위
def real_time_movie_chart():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    ftitle=[]
    no=0;
    #파싱해오는 for문
    for n in range(0, 10) :
        # 영화 순위
        no+=1;
        # 영화 제목
        title = list[n].find(class_="tit").find("a").text
        title = str(no)+". "+title
        
        ftitle.append(title)

    return ftitle

#영화 포스터 
def movie_img():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    fimg_list=[]
    no=0;
    #파싱해오는 for문
    for n in range(0, 10) :
        img=list[n].find(class_="thumb").find("a").find("img")
        imgList=img.get('src')
        fimg_list.append(imgList)

    return fimg_list

#영화 n세 관람가
def movie_age():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    fage_list=[]
    no=0;
    #파싱해오는 for문
    for n in range(0, 10) :
        age=list[n].find(class_="lst_dsc").find(class_="tit").find("span").text
        fage_list.append(age)

    return fage_list

#영화 예매율
def movie_reserv_rate():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    freserv_rate_list=[]
    no=0;
    #파싱해오는 for문
    for n in range(0, 10) :
        reserv_rate=list[n].find(class_="lst_dsc").find(class_="star").find(class_="info_exp").find(class_="star_t1 b_star").find("span").text
        freserv_rate_list.append(reserv_rate)

    return freserv_rate_list

#영화 장르
def movie_genre():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    fgenre_list=[]
    no=0;
    #파싱해오는 for문
    for n in range(0, 10) :
        genre=list[n].find(class_="info_txt1").find_all("dd")[0].find("span").find_all("a")
        genre_list=[genre.text.strip() for genre in genre]
        #리스트의 값을 문자열로 합하여 저장해서 다시 리스트로 넣어주는 작업
        genre_list=" ".join(genre_list)
        fgenre_list.append(genre_list)

    return fgenre_list

#영화 평점
def movie_score():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    fscore_list=[]
    no=0;
    #파싱해오는 for문
    for n in range(0, 10) :
        score_list=list[n].find(class_="star_t1").find("a").find("span",class_="num").text
        fscore_list.append(score_list)

    return fscore_list
    
#가장 가까운 영화관
def near_theater():
    #driver = webdriver.Chrome("./chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

    # 구버전 네이버지도 접속
    driver.get("https://v4.map.naver.com")

    driver.find_elements_by_css_selector("button.btn_close")[1].click()

    # 검색창에 검색어 입력하기 // 검색창: input#search-input
    search_box = driver.find_element_by_css_selector("input#search-input")
    search_box.send_keys("영화관")
    # 검색버튼 누르기 // 검색버튼: button.spm
    search_button = driver.find_element_by_css_selector("button.spm")
    search_button.click()

    time.sleep(5)

    #select=배열, select_one=하나의 값만가져올때

    html=driver.page_source
    bs=BeautifulSoup(html,'html.parser')
    cs=bs.select('ul.lst_site > li')
    ftitle=[]


    for i in range(0,3):
        title=cs[i].select_one('div.lsnx > dl.lsnx_det > dt > a').text
        ftitle.append(title)


    return ftitle

# def theater_location(int data):
#     near_theater_list


#     #driver = webdriver.Chrome("./chromedriver.exe")
#     options = webdriver.ChromeOptions()
#     options.add_argument('headless')
#     options.add_argument('window-size=1920x1080')
#     options.add_argument("disable-gpu")
#     driver = webdriver.Chrome('./chromedriver.exe', chrome_options=options)

#     # 구버전 네이버지도 접속
#     driver.get("https://naver.com")

#     driver.find_elements_by_css_selector("button.btn_close")[1].click()

#     # 검색창에 검색어 입력하기 // 검색창: input#search-input
#     search_box = driver.find_element_by_css_selector("input#search-input")
#     search_box.send_keys("영화관")
#     # 검색버튼 누르기 // 검색버튼: button.spm
#     search_button = driver.find_element_by_css_selector("button.spm")
#     search_button.click()

#     time.sleep(5)



#핸들러
task_buttons_handler_1 = CommandHandler('chart', cmd_task_buttons_1 )

task_buttons_handler_3 = CommandHandler('location', cmd_task_buttons_3)

task_buttons_handler_4 = CommandHandler('info', cmd_task_buttons_4 )
 
task_buttons_handler_2 = CommandHandler('near', cmd_task_buttons_2 )
# button_callback_handler_2 = CallbackQueryHandler( cb_button_2 )   


dispatcher.add_handler( task_buttons_handler_1 )
dispatcher.add_handler( task_buttons_handler_3)
dispatcher.add_handler( task_buttons_handler_4 )
dispatcher.add_handler( task_buttons_handler_2 )
# dispatcher.add_handler( button_callback_handler_2 )

 
updater.start_polling()
updater.idle()
