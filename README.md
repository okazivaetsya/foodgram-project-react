# Дипломная работа на Яндекс.Практикуме
![workflow status badge](https://github.com/okazivaetsya/foodgram-project-react/actions/workflows/foodgram workflow.yml/badge.svg?event=push)

Проект лежит тут: http://158.160.11.184/
### Данные для входа:
**login:** admin@mail.ru
**password:** admin


# FOODGRAM

### Описание
Foodgram - проект для создания, хранения и просмотра рецептов с возможностью подписки на любимых авторов, сохранения рецептов в "Избранное" а также создавать списки для покупок необходимых ингредиентов.

### Программные требования
1) Сервер должен работать на ОС Linux
2) На сервере должен быть установлен [Docker](https://www.docker.com/)


### Установка
##### Установка приложения из контейнеров
1) Склонируйте foodgram из [репозитория](https://github.com/okazivaetsya/foodgram-project-react)
2) Скопируйте на сервер два файла:
```bash 
scp docker-compose.yml <user_name>@<ip>:
scp nginx.conf <user_name>@<ip>:/nginx/default.conf
```
3) Запустите docer-compose:
```bash 
sudo docker-compose up -d --build
```

##### Настройка базы данных
1) Сделайте миграции:
```bash 
sudo docker-compose exec web python3 manage.py migrate
```
2) Подгрузите статику:
```bash 
sudo docker-compose exec web python3 manage.py collectstatic
```
3) Загрузите необходимые данные в базу:
```bash 
docker-compose exec web python manage.py loaddata dump.json```

