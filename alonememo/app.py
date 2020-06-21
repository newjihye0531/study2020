from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

## API 역할을 하는 부분
# POST
@app.route('/memo', methods=['POST'])
def saving():
        # ★★★가장 먼저 코드 작성하는 곳!!!
		# 1. 클라이언트로부터 데이터를 받기
        # 그리고 index.html의 POST로 간다
    url = request.form['url']
    comment = request.form['comment']
    print(url, comment)

		# 2. meta tag를 스크래핑하기
        # url은 지운다!
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠습니다.
    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    og_image['content']
    og_title['content']
    og_description['content'] 

    memo_dict = {
        'url': url,
        'comment': comment,
        'og_image': og_image['content'],
        'og_title': og_title['content'],
        'og_description': og_description['content']
    }

		# 3. mongoDB에 데이터 넣기
    db.memo.insert_one(memo_dict)

    return jsonify({'result': 'success', 'msg':'포스팅되었습니다!'})


#GET (post부분 성공하고 나면 get코드 작성)
@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 작성 후 index.html로 넘어가기
    articles = list(db.memo.find(projection={'_id':False}))
    print(articles)

    # 2. articles라는 키 값으로 영화정보 내려주기
    # 
    return jsonify({'result':'success', 'articles': articles})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)