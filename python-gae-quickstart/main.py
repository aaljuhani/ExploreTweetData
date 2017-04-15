from flask import Flask
from flask import send_file
from flask import render_template
import csv
import json


data_path = './data/'

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def index():
    """
    :return: main page
    """
    return render_template("index.html")

@app.route('/data')
def get_data():
    """Return Data"""
    #count_tweets = pd.read_csv(data_path+'tweetcounts.csv')
   # misra = pd.read_csv(data_path+'misra.csv')
    return 'Hello World!'


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
