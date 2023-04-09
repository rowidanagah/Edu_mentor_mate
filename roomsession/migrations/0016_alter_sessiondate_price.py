# Generated by Django 4.1.7 on 2023-04-09 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomsession', '0015_sessiondate_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessiondate',
            name='price',
            field=models.DecimalField(decimal_places=2, default=9.99, max_digits=10),
        ),
    ]
