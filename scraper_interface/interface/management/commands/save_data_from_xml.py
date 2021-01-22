import os
import xml.etree.ElementTree as ET

import django
from django.conf import settings
from django.core.management.base import BaseCommand

from interface.models import Review, Item

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mentorship.settings')

django.setup()


class Command(BaseCommand):
    def _save_review(self, reviews, is_positive):
        saved_reviews = []
        if reviews != '':
            review_list = [review.strip() for raw_reviews in reviews for review in raw_reviews.split(',') if review]
            reviews_with_occurrences = [(review, review_list.count(review)) for review in set(review_list)]
            for review in reviews_with_occurrences:
                saved_review = Review.objects.create(description=review[0].strip(), is_positive=is_positive, occurrences=review[1])
                saved_reviews.append(saved_review)
        return saved_reviews

    def _save_data_from_xml(self):
        file_path = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(settings.BASE_DIR, '..'), 'scraper'), 'Output'), 'all'), 'final_reviews.xml')
        xml_file = ET.parse(file_path)
        root = xml_file.getroot()
        for item in root:
            xml_positive_reviews = []
            xml_negative_reviews = []
            saved_item = None
            created = None
            for properties in item:
                if properties.tag == 'name':
                    print(f'--- ---Saving data for: {properties.text}')
                    saved_item, created = Item.objects.get_or_create(name=properties.text)
                    if not created:
                        print(f'--- --- ---Item already exists. Skipped')

                if properties.tag == 'review' and saved_item and created:
                    xml_negative_reviews.append(properties.get('negative'))
                    xml_positive_reviews.append(properties.get('positive'))

            if saved_item:
                for review in self._save_review(xml_negative_reviews, False):
                    saved_item.reviews.add(review)

                for review in self._save_review(xml_positive_reviews, True):
                    saved_item.reviews.add(review)

    def handle(self, *args, **options):
        print('--- Saving data from xml')
        self._save_data_from_xml()
        print('--- Done ---')
