from flask import Flask
import redis


app = Flask(__name__)
redis_client = redis.Redis(host="redis", port=6379)


@app.route("/")
def home():
    secure_key = redis_client.get("secure-key")
    secure_key = secure_key.decode("utf-8")
    print(type(secure_key))
    return f"<h1>!Docker Secrets Exercise</h1><br><p>{secure_key}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
