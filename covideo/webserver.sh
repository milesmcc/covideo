#!/bin/bash

# Start Gunicorn processes
echo Launching Covideo web server...
exec gunicorn covideo.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 1 \
    --timeout 100
