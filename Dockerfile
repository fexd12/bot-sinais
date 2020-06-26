FROM python:3.8.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN apt-get update && pip install git+https://github.com/fexd12/iqoptionapi.git --user && pip install python-dateutil

COPY . /usr/src/app

CMD ["python","./main.py"]