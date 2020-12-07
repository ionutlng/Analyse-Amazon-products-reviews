from django.db import models


class Reviews(models.Model):
    description = models.CharField(max_length=300)

    def __str__(self):
        return f'{self.description[:50]}'


class Items(models.Model):
    name = models.CharField(max_length=300)
    reviews = models.ManyToManyField(Reviews)

    def __str__(self):
        return f'{self.name}'
