# Generated by Django 4.1.7 on 2023-03-29 21:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roomsession', '0002_roomsession_user_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomsession',
            name='user_bio',
        ),
    ]
