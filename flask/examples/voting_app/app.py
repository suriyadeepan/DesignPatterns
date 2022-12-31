"""
Define routes
"""
from flask import Flask
from flask import render_template, redirect, url_for
from models import db


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///votes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "fortheloveofgoddonotusethisassecret"

db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    return redirect(url_for("login"))


@app.route("/candidate/{candidate_id}", methods=["GET", "POST"])
def candidate(candidate_id):
    return render_template("candidate.html")


@app.route("/vote/count", methods=["GET", "POST"])
def vote_count():
    return


app.run("0.0.0.0",debug=True)