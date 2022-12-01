# Generated by Django 2.2.19 on 2022-11-30 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20221130_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Любимые рецепты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recipe', to='recipes.Tag', verbose_name='Тэги'),
        ),
    ]
