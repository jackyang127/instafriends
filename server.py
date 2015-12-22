from flask import Flask
from flask import g
import compute_friends
import json
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/best_friend_app/database/friends.db'
db = SQLAlchemy(app)


#DATABASE = '/path/to/database.db'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)
    full_name = db.Column(db.String(80), unique=True)
    first = db.Column(db.String(120))
    second = db.Column(db.String(120))
    third = db.Column(db.String(120))
    fourth = db.Column(db.String(120))
    fifth = db.Column(db.String(120))

    def __init__(self, user_name, full_name, first, second, third, fourth, fifth):
        self.user_name = user_name
        self.full_name = full_name
        self.first = first
        self.second = second
        self.third = third
        self.fourth = fourth
        self.fifth = fifth

    def clever_json_dump(self):
        mock = {
          'id': self.id,
          'user_name': self.user_name,
          'full_name': self.full_name,
          'first': self.first,
          'second': self.second,
          'third': self.third,
          'fourth': self.fourth,
          'fifth': self.fifth,
        }
        return json.dumps(mock)


    def __repr__(self):
        return '<User %r>' % self.user_name



@app.route('/')
def login():
    return app.send_static_file('login.html')

@app.route('/calculate/<auth_code>', methods=['GET', 'POST'])
def friends(auth_code):
    friends_lists, json_percent, auto_name, auto_username, name_object = compute_friends.find_friends(auth_code)
    user_self = compute_friends.find_self(auth_code)
    self_name = user_self.full_name
    self_username = user_self.username
    number = [1, 2, 3, 4, 5]
    if User.query.filter_by(user_name=user_self.username).first() is None: 
        friend = User(user_self.username, user_self.full_name, friends_lists[0].full_name, friends_lists[1].full_name, friends_lists[2].full_name, friends_lists[3].full_name, friends_lists[4].full_name)
        db.session.add(friend)
        db.session.commit()
    list1 = dict((row.user_name, json.loads(row.clever_json_dump())) for row in User.query.all())
    list2 = dict((row.full_name, json.loads(row.clever_json_dump())) for row in User.query.all())
    friends_list = list(zip(friends_lists, number))
    
    return render_template('display.html', name_object = name_object, json_percent = json_percent, auto_name = auto_name, auto_username = auto_username, friends_list = friends_list, self_name = self_name, self_username = self_username, user_name_friends = json.dumps(list1), full_name_friends = json.dumps(list2))


@app.route('/cover.css')
def css():
    return app.send_static_file('cover.css')
@app.route('/background.jpg')
def background():
    return app.send_static_file('background.jpg')

@app.route('/extra.css')
def css1():
    return app.send_static_file('extra.css')

@app.route('/search.css') 
def search():
    return app.send_static_file('search.css')

@app.route('/typeahead.bundle.js')
def js():
    return app.send_static_file('typeahead.bundle.js')

if __name__ == '__main__':
    app.run(threaded=True)







