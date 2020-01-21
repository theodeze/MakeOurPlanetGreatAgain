FROM python:alpine
LABEL maintainer="theo.deze@etud.univ-angers.fr"
LABEL version="1.0"
LABEL description="Run server."
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apk add gcc musl-dev jpeg-dev zlib-dev
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
RUN python manage.py makemigrations authentication venture && \
    python manage.py migrate

ENTRYPOINT python manage.py runserver 0.0.0.0:8000