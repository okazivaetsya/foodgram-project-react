# Generated by Django 2.2.19 on 2022-11-28 08:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0005_auto_20221128_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]