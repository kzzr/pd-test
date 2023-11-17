FROM python:3.6-slim-stretch

RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y make
RUN apt clean && apt update && apt upgrade && apt install -f
RUN apt install -y build-essential wget unzip cmake

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5014
RUN echo $(ls -1 /app )
RUN echo "Contenido del directorio:" && ls -la
CMD python3 /app/backend/manage.py runserver
