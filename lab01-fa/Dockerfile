FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

RUN python init_db.py


EXPOSE 8000


CMD ["python", "app.py"]
