# Generated by Django 4.1.7 on 2023-04-04 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_profile',
            field=models.ImageField(blank=True, upload_to='images/accounts'),
        ),
    ]
