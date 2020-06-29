FROM python:3.8.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && pip install -r requirements.txt

COPY . /usr/src/app

CMD ["python","./main.py"]