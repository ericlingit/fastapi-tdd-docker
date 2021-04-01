FROM python:3.7-slim-buster

# set working directorys
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc \
  && apt-get clean

# install python dependencies
RUN pip install -U pip wheel
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

# add entry point to check for postgre
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
