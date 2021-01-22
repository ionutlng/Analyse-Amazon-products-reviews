from django.db import models


class Review(models.Model):
    description = models.CharField(max_length=300)
    is_positive = models.BooleanField()
    occurrences = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.description[:50]}'


class Item(models.Model):
    name = models.CharField(max_length=300, unique=True)
    reviews = models.ManyToManyField(Review)

    def __str__(self):
        return f'{self.name}'
