This exercise containerizes a flask application.

## Create a Dockerfile

```bash
FROM python:3-alpine3.15  # stripped down version of python base image
# copy requirements file from current folder
COPY requirements.txt .
# install pip requirements
RUN python -m pip install -r requirements.txt

# set working directory
WORKDIR /app
# copy contents of current directory to working directory
COPY . /app

# expose PORT 5000
EXPOSE 5000

# run application
CMD python ./caching_meme_site.py
```


## Build Docker Image

```bash
docker build -t suriyadeepan/meme-flask:latest .
```

## Run container

```bash
docker container run -p 5000:5000 suriyadeepan/meme-flask:latest
```