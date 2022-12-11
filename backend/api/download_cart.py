import io

from django.http import FileResponse
from recipes.models import IngredientsInRecipes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework.views import APIView


class DownloadCartView(APIView):
    def get(self, request):
        user = request.user
        shopping_cart = user.shopping_cart.all()
        products_list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = IngredientsInRecipes.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in products_list:
                    products_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    products_list[name]['amount'] += amount
        shoping_list = []
        shoping_list.append('СПИСОК ПОКУПОК:')
        shoping_list.append('---------')
        for item in products_list:
            shoping_list.append(
                f'{item} – {products_list[item]["amount"]}'
                f'{products_list[item]["measurement_unit"]}'
            )
        shoping_list.append(' ')
        shoping_list.append('FoodGram by Murashov Denis, 2022')
        pdfmetrics.registerFont(TTFont('Ubuntu', './api/fonts/Ubuntu-C.ttf'))
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Ubuntu", 15)
        start = 800
        for string_line in shoping_list:
            p.drawString(50, start, string_line)
            start -= 15
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True,
            filename='shopping_list.pdf'
        )
