from flask import Flask, render_template
from flask_caching import Cache
import requests
import json

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 60
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


def get_meme():
    url = "https://meme-api.com/gimme"
    response = json.loads(requests.request("GET", url).text)
    meme_large = response["url"]
    subreddit = response["subreddit"]
    return meme_large, subreddit


@app.route("/")
@cache.cached(timeout=60)
def index():
    meme_pic, subreddit = get_meme()
    return render_template("meme_index.html",
                           meme_pic=meme_pic, subreddit=subreddit)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
