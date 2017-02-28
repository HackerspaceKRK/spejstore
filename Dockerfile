FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get -y update
RUN apt-get -y install libsasl2-dev libldap2-dev libssl-dev
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
