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
        execute_from_command_line(["manage.py", "populate_items", "--generate_items", str(items_number), "--generate_reviews", str(reviews_number)])

    def _add_super_user(self):
        User.objects.create_superuser('admin', 'admin@admin.com', 'admin')

    def _save_data_from_xml(self):
        execute_from_command_line(["manage.py", "save_data_from_xml"])

    def add_arguments(self, parser):
        parser.add_argument('--generate_items', type=int, default=10, help='Number of dummy items generated')
        parser.add_argument('--generate_reviews', type=int, default=50, help='Number of dummy reviews generated')
        parser.add_argument('--generate_dummy_data', action='store_true', help='True if you want to generate dummy data. False (or just don\'t give this as an argument) if you want to get the data from the xml file.')

    def handle(self, *args, **kwargs):
        self._init_db()
        if 'generate_dummy_data' and kwargs['generate_dummy_data']:
            self._populate_items(kwargs['generate_items'], kwargs['generate_reviews'])
        else:
            self._save_data_from_xml()
        self._add_super_user()
