import datetime

from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from gdrive_service import GoogleDriveService
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from flask import (Flask, jsonify, redirect, render_template, request, session,
                   url_for)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///voting.db"
app.config["SECRET_KEY"] = "fortheloveofgoddonotusethisassecret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
db = SQLAlchemy(app)
Session(app)
gdrive = GoogleDriveService().build()
images = []


class Vote(db.Model):
    # primary key: vote id
    id = db.Column(db.Integer, primary_key=True)
    # foregin key: file_id
    file_id = db.Column(db.String(50), db.ForeignKey('images.file_id'))
    ip = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(70))
    timestamp = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.now
    )


class Images(db.Model):
    # primary key
    file_id = db.Column(db.String(100), nullable=False, primary_key=True)
    # number of votes received
    votes = db.Column(db.Integer, default=0)


def get_image_list_meta():
    list_file = gdrive.files().list().execute()
    # filter files based on typerender_template("gallery.html", user_image=file_id)
    return [file_ for file_ in list_file.get("files")
            if "image" in file_["mimeType"]]


@app.route("/all")
def all_files():
    return {
        "files": get_image_list_meta()
    }


@app.route("/vote/<file_id>", methods=["GET", "POST"])
def register_vote(file_id):
    vote = Vote(file_id=file_id, ip=str(request.remote_addr),
                user_agent=str(request.user_agent))
    db.session.add(vote)
    db.session.commit()
    # count the vote in Images DB
    image = Images.query.filter_by(file_id=file_id).first()
    image.votes += 1
    db.session.commit()
    return jsonify({
        "file_id": file_id,
        "ip": vote.ip,
        "timestamp": vote.timestamp,
        "user_agent": str(request.user_agent)
    }), 200


@app.route("/file-by-id/<id>")
def get_file_by_id(id):
    image_url = f"https://drive.google.com/uc?export=view&id={id}"
    return render_template("gallery.html", user_image=image_url)


@app.route("/next-meta")
def get_random_image_url():
    if not session.get("count") or session["count"] >= len(images):
        session["count"] = 0
    file_id = images[session["count"]]
    session["count"] = session["count"] + 1
    return jsonify({
        "src": file_id
    })


@app.route("/next")
def render_next_image():
    if not session.get("count"):
        session["count"] = 0
        # create vote
        # session["vote"] = {}
    if session["count"] >= len(images):
        session["count"] = 0
    file_id = images[session["count"]]
    session["count"] = session["count"] + 1
    return redirect(url_for("get_file_by_id", id=file_id))


@app.route("/")
def render_cards():
    return render_template("cards.html")


@app.route("/gallery")
def render_gallery():
    return render_template("gallery.html")


@app.route("/session")
def debug_session():
    return jsonify({
        "count": session['count'],
        "votes": session['votes']
    })


@app.route("/topk/<count>", methods=["GET"])
def fetch_topk_images(count):
    result = db.engine.execute(
        text(f"select * from images order by votes DESC LIMIT {count}"))
    data = []
    for row in result:
        data.append({
            "file_id": row[0],
            "votes": row[1]
        })
    return jsonify(data), 200


def init_db(images):
    for im in set(images):
        try:
            image = Images(file_id=im)
            db.session.add(image)
            db.session.commit()
        except IntegrityError:
            print(image, "exits in db")

# @app.route("/register-vote/<id>", methods=["POST"])
# def register_vote(id):
#     if not session.get("votes"):
#         session["votes"] = {}
#     if not session.get("votes").get(id):
#         session["votes"][id] = 0
#     session["votes"][id] += 1
#     return jsonify(session["votes"])


if __name__ == "__main__":
    images = [f["id"] for f in get_image_list_meta()]
    # with app.app_context():
    #     init_db(images)
    app.run(host="0.0.0.0", debug=True)
