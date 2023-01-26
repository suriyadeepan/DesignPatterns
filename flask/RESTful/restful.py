from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class MyResource(Resource):
    def get(self):
        return {"hello": "world"}


api.add_resource(MyResource, "/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
