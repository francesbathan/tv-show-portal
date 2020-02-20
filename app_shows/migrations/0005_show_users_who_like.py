# Generated by Django 2.2 on 2020-02-20 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shows', '0004_review_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='users_who_like',
            field=models.ManyToManyField(related_name='liked_shows', to='app_shows.User'),
        ),
    ]