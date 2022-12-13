from rest_framework.pagination import PageNumberPagination


class FoodgramPagination(PageNumberPagination):
    """Кастомная пагинация Fodgramm. """
    page_size_query_param = 'limit'
