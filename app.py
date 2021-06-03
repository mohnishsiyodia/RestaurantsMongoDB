from flask import Flask, render_template, request, url_for, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb+srv://mohnish:qwerty1234@cluster0.a6g5j.mongodb.net/sample_restaurants'
#mongodb+srv://mohnish:<password>@cluster0.a6g5j.mongodb.net/sample_restaurants
#mongodb+srv://mohnish:qwerty1234@cluster0.a6g5j.mongodb.net/sample_restaurants?retryWrites=true&w=majority'
mongo = PyMongo(app)

restaurant = mongo.db.restaurants

@app.route('/')
def index():
    # saved_restaurant = restaurant.find()
    saved_restaurant = restaurant.find().limit(50)
    print(saved_restaurant)
    return render_template('index.html', restaurants=saved_restaurant)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('new-todo')
    restaurant.insert_one({'text' : new_todo, 'complete' : False})
    return redirect(url_for('index'))

@app.route('/complete/<oid>')
def complete(oid):
    todo_item = restaurant.find_one({'_id': ObjectId(oid)})
    todo_item['complete'] = True
    restaurant.save(todo_item)
    return redirect(url_for('index'))

@app.route('/delete_completed')
def delete_completed():
    restaurant.delete_many({'complete' : True})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()