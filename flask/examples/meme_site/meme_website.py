from flask import Flask, render_template
import requests
import json

app = Flask(__name__)


# @app.route("/")
# def index():
#     return "<h1>Hello</h1>"


def get_meme():
    url = "https://meme-api.com/gimme"
    response = json.loads(requests.request("GET", url).text)
    meme_large = response["url"]
    subreddit = response["subreddit"]
    return meme_large, subreddit


@app.route("/")
def index():
    meme_pic, subreddit = get_meme()
    return render_template("meme_index.html",
                           meme_pic=meme_pic, subreddit=subreddit)
