# Generated by Django 4.1.7 on 2023-04-09 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomsession', '0016_alter_sessiondate_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessiondate',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
