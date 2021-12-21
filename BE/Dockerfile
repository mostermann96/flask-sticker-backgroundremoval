FROM python:3.8-slim-buster

WORKDIR /BE



COPY . .

RUN pip3 install -e .

ENV FLASK_APP=app

# remove for production
ENV FLASK_ENV=development

ENV FLASK_RUN_HOST=backend
ENV FLASK_RUN_PORT=5050

EXPOSE 5050

CMD [ "flask",  "run"]

