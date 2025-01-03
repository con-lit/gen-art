#!/bin/sh

# Apply database migrations
python manage.py migrate

# Create superuser if it does not exist
python manage.py create_superuser

# Check if the environment is production
if [ "$DJANGO_ENV" = "production" ]; then
    # Start Hypercorn in production
    hypercorn --bind 0.0.0.0:8000 consta.asgi:application
else
    # Start the Django development server on local machine
    python manage.py runserver 0.0.0.0:8000
fi