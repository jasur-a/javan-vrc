FROM python:3.8-slim-buster

LABEL maintainer="jaspeu.a@gmail.com"

RUN apk --no-cache add python build-base python-dev \
	    jpeg-dev zlib-dev linux-headers zlib-dev
WORKDIR /srv/src/
ADD requirements.txt /srv/src/
RUN pip install -r requirements.txt
COPY . /srv/src/
EXPOSE :8080
CMD ["uwsgi", "--ini", "uwsgi.ini"]
