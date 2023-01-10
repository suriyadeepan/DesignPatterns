# For more information, please refer to https://aka.ms/vscode-docker-python
FROM ubuntu

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# You need to run `apt update` before installing packages
RUN apt update
# Install nginx
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update
RUN apt install python3.10 -y
RUN apt install python3-pip -y
RUN apt install nginx -y

# nginx config setup
COPY nginx.conf /etc/nginx/nginx.conf

# If the image you're using is Alpine based, so you can't use apt-get
# because it's Ubuntu's package manager. 
# RUN apk add --no-cache nginx

# Install pip requirements
COPY gdrive.requirements.txt .
RUN python3.10 -m pip install -r gdrive.requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser
EXPOSE 80

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD service nginx start; gunicorn --bind 0.0.0.0:5000 render_from_google_drive:app