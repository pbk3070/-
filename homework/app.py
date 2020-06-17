from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient  

client = MongoClient('localhost', 27017)  
db = client.dbsparta  



@app.route('/')
def home():
    return render_template('index.html')



@app.route('/reviews', methods=['POST'])
def write_review():
    name_box_receive = request.form['name_box_give']
    age_box_receive = request.form['age_box_give']
    where_box_receive = request.form['where_box_give']
    day_box_receive = request.form['day_box_give']

    review = {
       'name_box':name_box_receive,
       'age_box': age_box_receive,
       'where_box': where_box_receive,
       'day_box': day_box_receive
    }

    db.reviews.insert_one(review)

    return jsonify({'result': 'success', 'msg': '성공적으로 신청이 완료되었습니다!.'})

@app.route('/reviews', methods=['GET'])
def read_reviews():
    
    reviews = list(db.reviews.find({},{'_id':0}))

    return jsonify({'result':'success', 'all_review':reviews})
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)