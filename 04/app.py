"""
/front/users serves a web page to see the users
this comes with new files:
- templates/users.html.j2
- static/style.css
"""

VERSION = "04"

import json
import requests

from flask import Flask
from flask import request
from flask import render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

## usual Flask initilization
app = Flask(__name__)

## DB declaration

# filename where to store stuff (sqlite is file-based)
db_name = 'chat.db'
# how do we connect to the database ?
# here we say it's by looking in a file named chat.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)


## define a table in the database

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    nickname = db.Column(db.String)


# actually create the database (i.e. tables etc)
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    return f'hello, this is a chat app! (version {VERSION})'


# try it with
"""
http :5001/db/alive
"""
@app.route('/db/alive')
def db_alive():
    try:
        result = db.session.execute(text('SELECT 1'))
        print(result)
        return dict(status="healthy", message="Database connection is alive")
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


# try it with
"""
http :5001/api/version
"""
@app.route('/api/version')
def version():
    return dict(version=VERSION)


# try it with
"""
http :5001/api/users name="Alice Caroll" email="alice@foo.com" nickname="alice"
http :5001/api/users name="Bob Morane" email="bob@foo.com" nickname="bob"
"""
@app.route('/api/users', methods=['POST'])
def create_user():
    # we expect the user to send a JSON object
    # with the 3 fields name email and nickname
    try:
        parameters = json.loads(request.data)
        name = parameters['name']
        email = parameters['email']
        nickname = parameters['nickname']
        print("received request to create user", name, email, nickname)
        # temporary
        new_user = User(name=name, email=email, nickname=nickname)
        db.session.add(new_user)
        db.session.commit()
        return parameters
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422


# try it with
"""
http :5001/api/users
"""
@app.route('/api/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return [dict(
            id=user.id, name=user.name, email=user.email, nickname=user.nickname)
        for user in users]



## Frontend
# for clarity we define our routes in the /front namespace
# however in practice /front/users would probably be just /users

# try it by pointing your browser to
"""
http://localhost:5001/front/users
"""
@app.route('/front/users')
def front_users():
    # first option of course, is to get all users from DB
    # users = User.query.all()
    # but in a more fragmented architecture we would need to
    # get that info at another endpoint
    # here we ask ourselves on the /api/users route
    url = request.url_root + '/api/users'
    req = requests.get(url)
    if not (200 <= req.status_code < 300):
        # return render_template('errors.html', error='...')
        return dict(error=f"could not request users list", url=url,
                    status=req.status_code, text=req.text)
    users = req.json()
    return render_template('users.html.j2', users=users, version=VERSION)


if __name__ == '__main__':
    app.run()
