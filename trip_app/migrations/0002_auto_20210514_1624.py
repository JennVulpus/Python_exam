# Generated by Django 2.2 on 2021-05-14 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='members',
            new_name='member',
        ),
    ]
