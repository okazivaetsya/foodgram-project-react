def check_empty_fields(*fields):
    """Проверка на пустые поля"""
    for field in fields:
        if not field:
            raise ValueError(f'Поле {field} является обязательным')
