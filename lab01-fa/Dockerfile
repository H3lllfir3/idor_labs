FROM python:3.8.18-alpine3.17

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

RUN python /app/init_db.py
RUN chmod 777 database.db


EXPOSE 5000


CMD ["python", "app.py"]
