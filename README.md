# Проект YaMDB
<!-- ![Github actions](https://github.com/mbragins1988/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg) -->

### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
Пользователи могут оставлять комментарии к отзывам.
Проект выполнялся командой из трех разработчиков.

### Как запустить проект

Клонировать репозиторий:

```
git clone git@github.com:mbragins1988/Fitness_tracker.git
```

Перейти в папку

```
cd yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
для Windows
```
source venv/Scripts/activate
```
для Mac
```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip3 install -r requirements.txt
```

### Заполнение базы данных из CSV:

Файлы с csv нужно добавить в папку static/data

Заполнение базы данных:

'''
python manage.py import_csv
'''

### документация:
http://127.0.0.1:8000/redoc/

### Стек технологий:
- Python 3.7
- Django
- Rest_Framework
- simple_jwt
- csv

## Разработчики:
- Илья Смирнов
- Михаил Брагин
- Антон Дубовкин