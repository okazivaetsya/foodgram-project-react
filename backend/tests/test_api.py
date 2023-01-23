from recipes.models import (Ingredients, IngredientsInRecipes, Recipes, Tags,
                            TagsInRecipes)
from users.models import CustomUser
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class TestRecipes(APITestCase):
    url = '/api/recipes/'

    def setUp(self):

        CustomUser.objects.create_user(
            email='testuser@mail.ru',
            username='TestUser',
            password='qwerty',
            first_name='Test',
            last_name='Testov'
        )

        Ingredients.objects.create(
            name='Carrot',
            measurement_unit='kg'
        )

        Tags.objects.create(
            name='Breackfast',
            color='green',
            slug='breakfast'
        )

        Recipes.objects.create(
            name='Salat',
            image='image.jpg',
            cooking_time='100',
            text='Test description for recipe',
            author=CustomUser.objects.get(id=1)
        )

        TagsInRecipes.objects.create(
            tag=Tags.objects.get(id=1),
            recipe=Recipes.objects.get(id=1)
        )

        IngredientsInRecipes.objects.create(
            ingredient=Ingredients.objects.get(id=1),
            recipe=Recipes.objects.get(id=1),
            amount='5'
        )

    def test_get_recipes_list(self):
        """Проверка get-запроса /api/recipes/"""
        response = self.client.get(self.url)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(result['results'], list)
        self.assertEqual(len(result['results']), 1)
        self.assertEqual(result['results'][0]['name'], 'Salat')
        self.assertEqual(
            result['results'][0]['image'],
            'http://testserver/media/image.jpg'
        )
        self.assertEqual(
            result['results'][0]['text'],
            'Test description for recipe'
        )
        self.assertEqual(
            result['results'][0]['author']['username'],
            'TestUser'
        )

        self.assertEqual(result['results'][0]['cooking_time'], 100)

    def test_get_recipe(self):
        """Проверка get-запроса /api/recipes/{id}"""
        response = self.client.get(f'{self.url}'+'1/')
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['name'], 'Salat')
        self.assertIsInstance(result['tags'], list)
