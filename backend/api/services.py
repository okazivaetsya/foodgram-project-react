def get_ingredients_list(data):
    my_list = []
    my_list.append('СПИСОК ПОКУПОК:')
    my_list.append('---------')
    for item in data:
        my_list.append(
            f"{item['ingredient__name']} – "
            f"{item['sum_amount']}"
            f"({item['ingredient__measurement_unit']})"
        )
    return my_list
