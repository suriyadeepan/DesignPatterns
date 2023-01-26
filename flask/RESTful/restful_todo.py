from flask import Flask, request
from flask_restful import Resource, Api

# request data validation
from flask_restful import reqparse


app = Flask(__name__)
api = Api(app)

todos = {}


class ToDo(Resource):
    def get(self, id):
        todo = todos.get(id, "No such resource")
        return {id: todo}

    def put(self, id):
        todos[id] = request.form["data"]
        return {id: todos[id]}


api.add_resource(ToDo, "/<string:id>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
