FROM python:3.14.2-slim as base

# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /home/ilya/code/deploy/pastepy


FROM base as dep-pip
COPY requirements.txt ./
RUN python -m venv env
RUN pip install -r requirements.txt
COPY src src
COPY .env .env

