# Generated by Django 2.2.19 on 2022-11-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20221130_1438'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='ingredientsamount',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='unique_ingredients'),
        ),
    ]
