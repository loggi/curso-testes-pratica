FROM python:3.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install env dependencies
RUN apt-get update \
    && apt-get install -y \
    && apt-get install -y --no-install-recommends \
    gdal-bin libgdal-dev libproj-dev
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

RUN pip install --upgrade pip
RUN pip install pipenv

# Install app dependencies
COPY ./requirements/Pipfile /app/Pipfile
RUN pipenv install --deploy --system --skip-lock --dev

# Set django app env vars
ENV DJANGO_ENV=dev
ENV DOCKER_CONTAINER=1
ENV SECRET_KEY="=97qk!l@&ueeb*la!wya#7c@o#1kfu&*s#ptv42mn59ym!=(1="

ENV POSTGRES_HOST=db
ENV POSTGRES_NAME=postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_PORT=5432

EXPOSE 8000

# Copy project
COPY . /app/