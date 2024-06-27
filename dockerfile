# pull official base image
FROM python:3.11.4-slim-buster


# create the appropriate directories
ENV HOME=/django-on-docker/django_learning
ENV APP_HOME=/django-on-docker/django_learning/web
RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles
RUN mkdir -p $APP_HOME/mediafiles
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .