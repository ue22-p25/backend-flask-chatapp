"""
/front/messages/<user_id> has a dialog to send messages
see also differences in messages.html.j2
"""

import json
from datetime import datetime as DateTime
import requests

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy.sql import or_

VERSION = "13"

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

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime)

    # Define relationships (to fetch User objects directly)
    author = db.relationship('User', foreign_keys=[author_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

# actually create the database (i.e. tables etc)
with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():
    # redirect to /front/users
    # actually this is just a rsponse with a 301 HTTP code
    return redirect('/front/users')


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
http :5001/api/users name="Charlie Chaplin" email="charlie@foo.com" nickname="charlie"
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


# try it with
"""
http :5001/api/users/1
"""
@app.route('/api/users/<int:id>', methods=['GET'])
def list_user(id):
    try:
        # as id is the primary key
        user = User.query.get(id)
        return dict(
            id=user.id, name=user.name, email=user.email, nickname=user.nickname)
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422


# try it with
"""
http :5001/api/messages author_id=1 recipient_id=2 content="trois petits chats"
http :5001/api/messages author_id=2 recipient_id=1 content="chapeau de paille"
http :5001/api/messages author_id=1 recipient_id=2 content="paillasson"
http :5001/api/messages author_id=2 recipient_id=1 content="somnambule"
http :5001/api/messages author_id=1 recipient_id=2 content="bulletin"
http :5001/api/messages author_id=2 recipient_id=1 content="tintamarre"
http :5001/api/messages author_id=2 recipient_id=3 content="not visible by 1"
"""
@app.route('/api/messages', methods=['POST'])
def create_message():
    try:
        parameters = json.loads(request.data)
        content = parameters['content']
        author_id = parameters['author_id']
        recipient_id = parameters['recipient_id']
        date = DateTime.now()
        print("received request to create message", author_id, recipient_id, content)
        new_message = Message(content=content, date=date,
                              author_id=author_id, recipient_id=recipient_id)
        db.session.add(new_message)
        db.session.commit()
        return parameters
    except Exception as exc:
        return dict(error=f"{type(exc)}: {exc}"), 422


# try it with
"""
http :5001/api/messages
"""
@app.route('/api/messages', methods=['GET'])
def list_messages():
    messages = Message.query.all()
    return [dict(
            id=message.id, content=message.content, date=message.date,
            author_id=message.author_id, recipient_id=message.recipient_id)
        for message in messages]


# try it with
"""
http :5001/api/messages/with/1
"""
@app.route('/api/messages/with/<int:recipient_id>', methods=['GET'])
def list_messages_to(recipient_id):
    """
    returns only messages to and from a given person
    need to write a little more elaborate query
    we still can only return author_id and recipient_id
    """
    messages = Message.query.filter(
        or_(
            Message.author_id==recipient_id,
            Message.recipient_id==recipient_id,
        )
    ).all()
    # now we have in message.author and message.recipient
    # the actual User objects
    return [
        dict(
            id=message.id,
            author = dict(
                id=message.author.id, name=message.author.name,
                email=message.author.email, nickname=message.author.nickname),
            recipient = dict(
                id=message.recipient.id, name=message.recipient.name,
                email=message.recipient.email, nickname=message.recipient.nickname),
            content=message.content,  date=message.date)
        for message in messages
    ]


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


# try it by pointing your browser to
"""
http://localhost:5001/front/messages/1
"""
@app.route('/front/messages/<int:recipient>')
def front_messages(recipient):
    # same as for the users, let's pretend we don't have direct access to the DB
    url = request.url_root + f'/api/users/{recipient}'
    req1 = requests.get(url)
    if not (200 <= req1.status_code < 300):
        return dict(error="could not request user info", url=url,
                    status=req1.status_code, text=req1.text)
    user = req1.json()
    req2 = requests.get(request.url_root + f'/api/messages/with/{recipient}')
    if not (200 <= req2.status_code < 300):
        return dict(error="could not request messages list", url=url,
                    status=req2.status_code, text=req2.text)
    messages = req2.json()
    # not trying to optimize for now
    url = request.url_root + '/api/users'
    req3 = requests.get(url)
    users = req3.json()
    return render_template(
        'messages.html.j2',
        user=user, messages=messages,
        users=users,
    )



if __name__ == '__main__':
    app.run()
