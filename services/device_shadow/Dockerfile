FROM ubuntu:latest

WORKDIR /app

RUN apt-get update \
&& apt-get install -y python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/app"

COPY . /app
