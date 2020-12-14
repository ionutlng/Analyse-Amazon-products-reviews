import os

import django
from django.core.management import execute_from_command_line
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorship.settings')

django.setup()


class Command(BaseCommand):
    def _init_db(self):
        try:
            os.remove("db.sqlite3")
        except FileNotFoundError:
            print("db.sqllite3 not found")
        execute_from_command_line(["manage.py", "migrate"])

    def _populate_items(self, items_number, reviews_number):
        execute_from_command_line(["manage.py", "populate_items", "--items_number", str(items_number), "--reviews_number", str(reviews_number)])

    def _add_super_user(self):
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

    def add_arguments(self, parser):
        parser.add_argument('--items_number', type=int, default=10, help='later')
        parser.add_argument('--reviews_number', type=int, default=50, help='later')

    def handle(self, *args, **kwargs):
        self._init_db()
        self._populate_items(kwargs['items_number'], kwargs['reviews_number'])
        self._add_super_user()
