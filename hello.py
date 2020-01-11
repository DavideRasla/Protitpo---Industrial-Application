from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world!'

@app.route('/login')
def test_template(name=None):
    return render_template('login.html', name=name)