FROM python:3-alpine3.15
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 5000

CMD python ./app.py
