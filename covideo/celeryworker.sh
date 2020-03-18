#!/bin/bash

# Start queue worker processes
echo Launching Covideo queue worker...
exec celery -A covideo worker -E --loglevel=INFO --concurrency=1