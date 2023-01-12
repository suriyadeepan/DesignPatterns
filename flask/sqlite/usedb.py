import datetime

from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

from flask import Flask, request, jsonify
import os

app = Flask(__name__)
dbdir = os.path.join(os.path.dirname(app.instance_path), "poll.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{dbdir}'
app.config["SECRET_KEY"] = "fortheloveofgoddonotusethisassecret"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
Session(app)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.String(50), nullable=False)
    ip = db.Column(db.String(50), nullable=False)
    user_agent = db.Column(db.String(70))
    timestamp = db.Column(
        db.DateTime(timezone=True), default=datetime.datetime.now
    )


@app.route("/")
def home():
    return "<h1>Hello!</h1>"


@app.route("/vote/<file_id>", methods=["GET", "POST"])
def register_vote(file_id):
    vote = Vote(file_id=file_id, ip=str(request.remote_addr),
                user_agent=str(request.user_agent))
    db.session.add(vote)
    db.session.commit()
    return jsonify({
        "file_id": file_id,
        "ip": vote.ip,
        "timestamp": vote.timestamp,
        "user_agent": str(request.user_agent)
    }), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
