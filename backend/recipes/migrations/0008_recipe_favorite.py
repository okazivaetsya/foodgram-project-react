# Generated by Django 2.2.19 on 2022-12-01 06:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_auto_20221130_0807'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Любимые рецепты'),
        ),
    ]