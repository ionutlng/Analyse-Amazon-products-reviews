# Generated by Django 3.1.2 on 2021-01-22 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_auto_20210122_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
