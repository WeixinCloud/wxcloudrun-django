FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 80

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
