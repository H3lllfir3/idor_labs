FROM python:3.11.6-alpine3.18

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

RUN python /app/init_db.py
RUN chmod 777 database.db


EXPOSE 5000


CMD ["python", "app.py"]
