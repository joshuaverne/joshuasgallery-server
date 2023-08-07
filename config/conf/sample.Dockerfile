# Dockerfile

FROM python:3.9

COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apps code
COPY ./config config
WORKDIR /code

EXPOSE 8000

ENV JGENV='dev'

CMD ["gunicorn", "-b", "0.0.0.0:8000", "apps.wsgi"]