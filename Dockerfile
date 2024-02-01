FROM python:3.11.4-slim-bookworm
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y --no-install-recommends \
  libpq-dev \
  gcc \
  && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code/

RUN groupadd --gid 1000 spejstore && useradd --uid 1000 --gid 1000 --home /code --shell /bin/bash spejstore
USER spejstore

CMD bash -c "python manage.py collectstatic --no-input --clear && python manage.py migrate && gunicorn --workers 1 --threads 4 -b 0.0.0.0:8000 --capture-output --error-logfile - --access-logfile - spejstore.wsgi:application"
