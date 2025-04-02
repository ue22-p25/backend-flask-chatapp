"""
the simplest possible hello world app
"""
VERSION = "00"

from flask import Flask

## usual Flask initilization
app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'hello, this is a chat app! (version {VERSION})'

if __name__ == '__main__':
    app.run()
