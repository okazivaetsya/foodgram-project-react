# Generated by Django 3.2.15 on 2022-12-05 14:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221205_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientsinrecipes',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Минимальное значение для поля - 1')]),
        ),
    ]
