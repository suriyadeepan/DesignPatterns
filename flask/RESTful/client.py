from requests import put, get


def tests():
    print(
        "PUT",
        put("http://localhost:5001/todo_01", data={"data": "Do your chores!"}).json(),
    )
    print("GET", get("http://localhost:5001/todo_01").json())
    print("GET", get("http://localhost:5001/todo_unk").json())


if __name__ == "__main__":
    tests()
