#!/bin/sh
cd ..
gunicorn "BE.app:create_app()" -w 2 --threads 2 -b 0.0.0.0:22 --certfile=certs/selfsigned.crt --keyfile=certs/selfsigned.key
