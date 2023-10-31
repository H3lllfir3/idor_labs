FROM python:3.8

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app


EXPOSE 5000


CMD ["flask", "run"]
