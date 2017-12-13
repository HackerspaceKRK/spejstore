FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get -y update
RUN apt-get -y install libsasl2-dev libldap2-dev libssl-dev
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN wget https://github.com/vishnubob/wait-for-it/raw/8ed92e8cab83cfed76ff012ed4a36cef74b28096/wait-for-it.sh -O /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it
ADD . /code/
