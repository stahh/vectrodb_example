FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /opt
COPY . /opt
RUN pip install -r /opt/requirements.txt