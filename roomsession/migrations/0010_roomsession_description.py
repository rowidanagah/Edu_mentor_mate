# Generated by Django 4.1.7 on 2023-04-05 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomsession', '0009_alter_sessiondate_deruration'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomsession',
            name='description',
            field=models.TextField(default='no  val'),
            preserve_default=False,
        ),
    ]
