# Generated by Django 4.1.7 on 2023-04-01 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomsession', '0009_message_delete_subscription'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
