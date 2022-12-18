FROM python:3.7-slim
LABEL author='Denis Murashov' project_name='foodgram' version='1.0'

RUN mkdir /app

COPY ["../", "/app"]

RUN python -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
RUN python3 ./app/manage.py makemigrations

WORKDIR /app

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
