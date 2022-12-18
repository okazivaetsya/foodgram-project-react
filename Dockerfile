FROM python:3.7-slim
LABEL author='Denis Murashov' project_name='foodgram' version='1.0'
RUN mkdir /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY backend/ /app
RUN python3 app/manage.py makemigrations
WORKDIR /app

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
