from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'test'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL', 'test@test.com'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD', 'test')
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))