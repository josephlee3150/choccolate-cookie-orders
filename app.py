from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')


## API 역할을 하는 부분
@app.route('/clientOrder', methods=['POST'])
def saving():
		# 1. 클라이언트로부터 데이터를 받기
        received_name = request.form['name_give']
        received_amount = request.form['amount_give']
        received_address = request.form['address_give']
        received_phone = request.form['phone_give']
		
		# 3. mongoDB에 데이터 넣기
        order = {
            'name': received_name,
            'amount': received_amount,
            'address': received_address,
            'phone': received_phone,
        }

        db.cookie_orders.insert_one(order)
        return jsonify({'result': 'success', 'msg':'POST 연결되었습니다!'})


@app.route('/orders', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    orders = list(db.cookie_orders.find({}, {'_id': 0}))
    # 2. articles라는 키 값으로 영화정보 내려주기
    return jsonify({'result':'success', 'orders': orders})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)
