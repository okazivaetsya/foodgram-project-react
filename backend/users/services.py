def check_empty_fields(*fields):
    """Проверка на пустые поля"""
    for field in fields:
        if not field:
            raise ValueError(f'Поле {field} является обязательным')


def check_user_items_in_models(model, request, obj):
    """
    Проеверка на наличие элеемнта в связной модели.
    Возвращает TRUE если пользователь имеет в связной модели данный объект.
    """
    return (request.user.is_authenticated and model.objects.filter(
                    user=request.user,
                    recipe=obj
                ).exists())
