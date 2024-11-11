FROM python:3.10-alpine

WORKDIR /flask-app

COPY requirements.txt /flask-app

RUN pip install -r requirements.txt --no-cache-dir

COPY . /flask-app

CMD python3 app.py