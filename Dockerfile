FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get -y update
RUN apt-get -y install libsasl2-dev libldap2-dev libssl-dev
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN wget https://github.com/vishnubob/wait-for-it/raw/55c54a5abdfb32637b563b28cc088314b162195e/wait-for-it.sh -O /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it
ADD . /code/
