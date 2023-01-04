from flask_session import Session
from gdrive_service import GoogleDriveService

from flask import Flask, jsonify, redirect, render_template, session, url_for

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
gdrive = GoogleDriveService().build()
images = []


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


@app.route("/cards")
def render_cards():
    return render_template("card-slide.html")


@app.route("/session")
def debug_session():
    return jsonify({
        "count": session['count'],
        "votes": session['votes']
    })


@app.route("/register-vote/<id>", methods=["POST"])
def register_vote(id):
    if not session.get("votes"):
        session["votes"] = {}
    if not session.get("votes").get(id):
        session["votes"][id] = 0
    session["votes"][id] += 1
    return jsonify(session["votes"])


if __name__ == "__main__":
    images = [f["id"] for f in get_image_list_meta()]
    app.run(host="0.0.0.0", debug=True)
