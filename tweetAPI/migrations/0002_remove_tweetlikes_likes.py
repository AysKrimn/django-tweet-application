# Generated by Django 4.2 on 2024-04-25 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweetAPI', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweetlikes',
            name='likes',
        ),
    ]