FROM python:3.7-slim
LABEL author='Denis Murashov' project_name='foodgram' version='1.0'

WORKDIR /app

COPY ../ /app

RUN python -m pip install --upgrade pip
RUN pip install -r /requirements.txt --no-cache-dir
RUN python3 manage.py makemigrations

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]
