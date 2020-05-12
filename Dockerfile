FROM python:3.5.9@sha256:3a71fd2dac2343263993f4ab898c9398dfbfd0235dafe41e784876b69bdfa899
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
RUN wget https://github.com/vishnubob/wait-for-it/raw/8ed92e8cab83cfed76ff012ed4a36cef74b28096/wait-for-it.sh -O /usr/local/bin/wait-for-it && chmod +x /usr/local/bin/wait-for-it
ADD . /code/
RUN python manage.py collectstatic

CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
