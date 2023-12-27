FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY faithful_heart/ .

RUN python manage.py collectstatic

CMD ["gunicorn", "faithful_heart.wsgi:application", "--bind", "0:8000" ]
