FROM python:3.9

LABEL maintainer="jaspeur.a@gmail.com / vane123_@hotmail.com"

# RUN apk --no-cache add python build-base python-dev \
#	    jpeg-dev zlib-dev linux-headers zlib-dev
WORKDIR /srv/src/
ADD requirements.txt /srv/src/
RUN pip install -r requirements.txt
RUN python -m spacy download es_core_news_lg
RUN python -m spacy download es_dep_news_trf
COPY . /srv/src/
EXPOSE :8080
CMD ["uwsgi", "--ini", "uwsgi.ini"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0 --port=500:5000"]
