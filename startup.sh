#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y libcairo2-dev

# Start the Gunicorn server
gunicorn -w 4 -b 0.0.0.0:8000 app:app