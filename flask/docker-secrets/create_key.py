import redis


if __name__ == "__main__":
    redis_client = redis.Redis(host="127.0.0.1", port=6379)
    secure_key = "Oh no! You have seen the key. I'm gonna have to kill you now."
    redis_client.set("secure-key", secure_key)
