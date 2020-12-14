import os
import random
from faker import Faker

import django
from django.core.management.base import BaseCommand

from interface.models import Review, Item

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorship.settings')

django.setup()

fake = Faker()


class Command(BaseCommand):
    def _populate_items(self, number_of_items):
        for _ in range(0, number_of_items):
            Item.objects.create(name=fake.text(max_nb_chars=15))

    def _populate_reviews(self, number_of_reviews):
        for _ in range(0, number_of_reviews):
            Review.objects.create(description=fake.text(max_nb_chars=30))

    def _add_reviews_to_items(self):
        items = Item.objects.all()
        reviews = Review.objects.all()
        for item in items:
            for _ in range(0,random.randrange(2,10)):
                item.reviews.add(random.choice(reviews))

    def add_arguments(self, parser):
        parser.add_argument('--items_number', type=int, default=10, help='later')
        parser.add_argument('--reviews_number', type=int, default=50, help='later')

    def handle(self, *args, **options):
        self._populate_items(options['items_number'])
        self._populate_reviews(options['reviews_number'])
        self._add_reviews_to_items()
