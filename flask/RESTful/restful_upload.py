import os

import werkzeug
from flask_restful import Api, Resource, abort, reqparse

from flask import Flask, send_from_directory, jsonify, make_response

UPLOAD_FOLDER = "uploads"
app = Flask(__name__)
# set upload folder in config
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# set maximum file size: 30MB
app.config["MAX_CONTENT_LENGTH"] = 30 * 1000 * 1000
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument(
    "file",
    type=werkzeug.datastructures.FileStorage,
    location="files",
    required=True,
    help="Provide an audio file",
)

audios = {
    "u23-f-001": "Gillian.wav",
}


def abort_if_no_id(id):
    if id not in audios:
        # The HTTP 404 Not Found response status code indicates
        #  that the server cannot find the requested resource.
        abort(404, message=f"{id} does not exist!")


class Audio(Resource):
    def get(self, id):
        print("id", id)
        abort_if_no_id(id)
        return send_from_directory(app.config["UPLOAD_FOLDER"], audios[id])

    def post(self, id):
        args = parser.parse_args()
        print("file", args.file)
        args.file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{id}.wav"))
        audios[id] = f"{id}.wav"
        return make_response(jsonify({"status": "success", "id": id}), 200)


api.add_resource(Audio, "/audio/<string:id>")


if __name__ == "__main__":
    app.run(port=5001)
