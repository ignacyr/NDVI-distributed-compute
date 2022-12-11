# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /ndvi-script

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY executor.py .

CMD [ "python3", "executor.py"]