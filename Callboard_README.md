# Callboard project, powered by

![N|Solid](https://www.djangoproject.com/m/img/logos/django-logo-negative.png)

## Регистрация

- После заполнения и отправки формы регистрации, создаётся аккаунт пользователя в статусе неактивного.
- При корректном вводе кода из письма, статус аккаунта меняется на активированный и пользователь может наслаждаться полным функционалом.

## Подписка

- Задание реализовано как подписка на рассылку всех объявлений, вышедших за последние сутки.

## CK editor

- Функционал реализован, видео, фото и другой контент доступны к добавлению, но из-за ограниченного времени не успел разобраться с прямым добавлением видео по ссылке в редактор...

## Technologies used

- Basic [Django] Patterns: Filters, Forms, Signals, Views...
- Implemented a system of periodic tasks using [Celery] and cloud [Redis]
- Work has been done on logging, more pleasing to the tasks of the developer


## Launch
Currently using a local server, just use the command: 
```sh
python manage.py runserver 
```
and follow the link in a browser
```sh
http://127.0.0.1:8000/posts
```

## Periodic tasks

The project is implemented on Windows, so to start the task of sending an email about a new post, use the command:
```sh
celery -A NewsPaper worker --pool=solo -l INFO
```
To run periodic tasks, open a new terminal window and use the command:
```sh
celery -A NewsPaper beat -l INFO
```



## License

HOME SWEET HOME

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [django]: <https://www.djangoproject.com/>
   [Redis]: <https://redis.io/>
   [Celery]: <https://docs.celeryq.dev/en/stable/>
   [Yandex]: <https://mail.yandex.ru/>


