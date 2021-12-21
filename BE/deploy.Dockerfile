FROM python:3.8-slim-buster

WORKDIR /BE

RUN pip install --no-cache-dir torch==1.6.0

COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip3 install -e .

EXPOSE 22

ENTRYPOINT ["./gunicorn_starter.sh"]

