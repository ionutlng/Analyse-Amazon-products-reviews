from django.db import models


class Reviews(models.Model):
    description = models.CharField(max_length=300)


class Items(models.Model):
    name = models.CharField(max_length=300)
    reviews = models.ManyToManyField(Reviews)
