from flask import Flask
from flask import g
import compute_friends
from flask import render_template


app = Flask(__name__)

DATABASE = '/path/to/database.db'

@app.route('/')
def login():
    return app.send_static_file('login.html')

@app.route('/calculate/<auth_code>', methods=['GET', 'POST'])
def friends(auth_code):
    friends_lists, scores, auto_name, auto_username, auto_percent = compute_friends.find_friends(auth_code)
    self_name = compute_friends.find_self(auth_code).full_name
    self_username = compute_friends.find_self(auth_code).username
    number = [1, 2, 3, 4, 5]
    friends_list = list(zip(friends_lists, number))
    return render_template('display.html', auto_percent = auto_percent, auto_name = auto_name, auto_username = auto_username, scores = scores, friends_list = friends_list, self_name = self_name, self_username = self_username)
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







