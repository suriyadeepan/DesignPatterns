import random

from gdrive_service import GoogleDriveService

from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
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
    # file_meta = gdrive.files().get(fileId=id).execute()
    # image_url = f"https://drive.google.com/file/d/{id}/view"
    image_url = f"https://drive.google.com/uc?export=view&id={id}"
    return render_template("gallery.html", user_image=image_url), {"Refresh": "10; url=/next"}


@app.route("/next")
def render_next_image():
    file_id = random.choice(images)
    return redirect(url_for("get_file_by_id", id=file_id))


if __name__ == "__main__":
    images = [f["id"] for f in get_image_list_meta()]
    app.run(host="0.0.0.0", debug=True)
