"""
the simplest possible hello world app
"""

from flask import Flask

VERSION = "00"

## usual Flask initilization
app = Flask(__name__)

@app.route('/')
def hello_world():
    return f'hello, this is a chat app! (version {VERSION})'

if __name__ == '__main__':
    app.run()
