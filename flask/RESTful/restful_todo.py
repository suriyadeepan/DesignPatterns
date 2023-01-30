from flask_restful import Api, Resource, abort, reqparse

from flask import Flask, request

app = Flask(__name__)
api = Api(app)

todos = {"test": "test"}
# parser = reqparse.RequestParser()
# parser.add_argument("task")


def abort_if_no_id(id):
    if id not in todos:
        # The HTTP 404 Not Found response status code indicates
        #  that the server cannot find the requested resource.
        abort(404, message=f"{id} does not exist!")


class ToDo(Resource):
    def get(self, id):
        abort_if_no_id(id)
        return {id: todos[id]}

    def delete(self, id):
        abort_if_no_id(id)
        del todos[id]
        # The HTTP 204 No Content success status response code
        # indicates that a request has succeeded, but that
        # the client doesn't need to navigate away from its
        # current page
        return "", 204

    def put(self, id):
        # args = parser.parse_args()
        # print(args)
        # task = args["task"]
        # #
        # print("TASK", id, task)
        task = request.form["task"]
        todos[id] = task
        # The HTTP 201 Created success status response code
        # indicates that the request has succeeded and has
        # led to the creation of a resource.
        return {"data": todos[id]}, 201


api.add_resource(ToDo, "/<string:id>")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
