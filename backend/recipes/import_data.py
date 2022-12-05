import csv
import os

path = "/Users/murashovdenis/Dev/mydiplom/foodgram-project-react/data/"
os.chdir(path)

from .models import Ingredients

with open('ingredients.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        p = Ingredients(
            name=row['name'],
            measurement_unit=row['measurement_unit']
        )
        p.save()
