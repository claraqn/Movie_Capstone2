#!C:\\Users\\clara\\AppData\\Local\\Programs\\Python\\Python39\\python.exe
print("content-type: text/html;")
#flask, render_template, url_for
from flask import Flask, render_template, url_for
app = Flask(__name__)
#값을 주고받기 위한 requests와 크롤링을 위한 BeautifulSoup
import requests
from bs4 import BeautifulSoup
#urlopen, dataframe 사용을 위한 모듈
from urllib.request import urlopen
import pandas as pd
#html에서 jinja2 사용하기 위함
#jinja2에서 zip을 사용하기 위한 코드
import jinja2
env=jinja2.Environment()
env.globals.update(zip=zip)
#google map을 사용하기 위한 flask_googlemaps import
from flask_googlemaps import GoogleMaps, Map
GoogleMaps(app)
from telegram_bot import hello


@app.route('/')
def main():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/map')
def map():
    return render_template('map.html')
    


@app.route('/moviechart')
def movie_chart():
    #영화순위사이트 가져오기
    url=urlopen('https://movie.naver.com/movie/running/current.nhn')
    #html 코드 가져오기
    bs = BeautifulSoup(url, 'html.parser')
    #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
    body = bs.body
    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    #값을 담아 movie_chart.html로 넘겨주기 위해 필요한 리스트 생성
    #no=순위
    ftitle=[]
    fdirectorList=[]
    fcastList=[]
    fnoList=[]
    fimgList=[]
    fscoreList=[]
    fgenreList=[]
    fvideoList=[]
    video_target_List=[]
    no=0
    movie_url='https://movie.naver.com/movie/running/current.nhn'

    #파싱해오는 for문
    for n in range(0, len(list)) :
        # 영화 순위
        no+=1
        fnoList.append(no)
        # 영화 제목
        title = list[n].find(class_="tit").find("a").text
        ftitle.append(title)
        # 감독
        try:
            director = list[n].find(class_="info_txt1").find_all("dd")[1].find("span").find_all("a")
            #text.strip()=공백 없게 문자열 정리해주는 함수
            directorList = [director.text.strip() for director in director]
            fdirectorList.append(directorList)
        except IndexError:
            print("제작 감독 :\t 정보 없음")
        # 출연 배우
        try:
            cast = list[n].find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(class_="link_txt").find_all("a")
            castList = [cast.text.strip() for cast in cast]
            fcastList.append(castList)
        except IndexError:
            print("출연 배우 :\t 정보 없음")
        # 영화 이미지
        try:
            img=list[n].find(class_="thumb").find("a").find("img")
            imgList=img.get('src')
            fimgList.append(imgList)
        except IndexError:
            print("이미지 : 없음")
        # 영화 평점
        try:
            score=list[n].find(class_="star_t1").find("a").find("span",class_="num")
            scoreList=[score.strip() for score in score]
            fscoreList.append(scoreList)
        except IndexError:
            print("평점 : 없음")
        # 영화 장르
        try:
            genre=list[n].find(class_="info_txt1").find_all("dd")[0].find("span").find_all("a")
            genreList = [genre.text.strip() for genre in genre]
            fgenreList.append(genreList)
        except IndexError:
            print("장르 : 없음")
        # 영화 예고편
        try:
            video=list[n].find(class_="btn_area").find("span",class_="btn_t1").find_all("a")[1]
            videoList=video.get('href')
            #동영상 에고편 사이트 가져오기
            fvideoList.append(videoList)
            #html 코드 가져오기
            # video_bs = BeautifulSoup(video_url, 'html.parser')
            # #bs.body => 파싱해온 html 중 body를 쉽게 가져올 수 있음
            # video_body = video_bs.body
            # video_target = video_body.find(class_="_videoPlayer")
            # video_target_List=video_target.get('src')
            # fvideoList.append(movie_url+videoList+video_target_List)
        except IndexError:
            print("예고편 : 없음")
    
    #movie_chart.html로 값을 넘겨줌
    return render_template('movie_chart.html',
        list=list,ftitle=ftitle,fdirectorList=fdirectorList,
        fcastList=fcastList,fnoList=fnoList,fimgList=fimgList,
        fscoreList=fscoreList,fgenreList=fgenreList,
        fvideoList=fvideoList,movie_url=movie_url,zip=zip)


#실행
if __name__ == '__main__':

	app.run(port="5501", debug=True)