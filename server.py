from flask import Flask
import compute_friends
from flask import render_template
app = Flask(__name__)

@app.route('/')
def login():
    return app.send_static_file('login.html')

@app.route('/calculate/<auth_code>', methods=['GET', 'POST'])
def friends(auth_code):
    friends_lists = compute_friends.find_friends(auth_code)
    self_name = compute_friends.find_self(auth_code).full_name
    self_username = compute_friends.find_self(auth_code).username
    number = [1, 2, 3, 4, 5]
    friends_list = list(zip(friends_lists, number))
    return render_template('display.html', friends_list = friends_list, self_name = self_name, self_username = self_username)
@app.route('/cover.css')
def css():
    return app.send_static_file('cover.css')


@app.route('/extra.css')
def css1():
    return app.send_static_file('extra.css')

if __name__ == '__main__':
    app.run(threaded=True)







