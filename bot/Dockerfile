FROM python:3.11

WORKDIR /bot

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY ./ .

CMD ["python", "main.py"]
