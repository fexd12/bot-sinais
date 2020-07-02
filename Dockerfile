FROM python:3.8.1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apt-get update && pip install -r requirements.txt && chmod +x shell.sh

CMD ["./shell.sh"]