# Multi-container Orchestration


Docker container uses the container name as hostname. 

```python
redis_client = redis.Redis(host="redis", port=6379)
```

Using `depends_on` tag in docker-compose connects the flask app container to redis container.


```yml
  flask: # flask image
    image: suriyadeepan/docker-secrets:latest
    ports:
      - 5000:5000
    restart: "no"
    depends_on:
      - redis
```