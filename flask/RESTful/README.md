# RESTful APIs with Flask


## Install

```bash
pip install Flask, flask-restful
```

## Usage

```python
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
```

## Interact with ToDo API

```bash
curl http://localhost:5001/todo1 -d "data=Buy milk x4" -X PUT
# {"todo1": "Buy milk x4"}
curl http://localhost:5001/todo1
# {"todo1": "Buy milk x4"}
curl http://localhost:5001/todo2 -d "data=Change clock battery" -X PUT
# {"todo2": "Change clock battery"}
curl http://localhost:5001/todo2
# {"todo2": "Change clock battery"}
```