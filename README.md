# Проект YaMDB
![Github actions](https://github.com/mbragins1988/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.
Пользователи могут оставлять комментарии к отзывам.
Проект выполнялся командой из трех разработчиков.

### Как запустить проект на локальном компьютере

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

```
python manage.py import_csv
```

### Как автоматически запустить проект на удаленном сервере после изменений

Запустить и подготовить удаленный сервер.
Войти на свой удаленный сервер в терминале (ssh your_login@pu.bl.ic.ip)

Остановить службу nginx

```
sudo systemctl stop nginx
```

Установить docker

```
sudo apt install docker.io
```

Установить docker-compose

```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```
```
sudo chmod +x /usr/local/bin/docker-compose
```

Скопировать файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно

Произвести необходимые изменения в проекте, сохранить файлы

Добавить изменения

```
git add --all
```

Сделать коммит

```
git commit -m "Commit"
```

Отправить изменения в удалённый репозиторий

```
git push
```

В Git Actions workflow выполнит:
- проверку кода на соответствие стандарту PEP8 с помощью пакета flake8
- запустит pytest
- соберет и доставит докер-образ для контейнера web на Docker Hub
- деплой проекта на боевой сервер
- отправит уведомление в Telegram о том, что процесс деплоя успешно завершился

В директории /home/mbragin/.local/bin выполнить миграции

```
docker-compose exec web python manage.py migrate
```

### документация на локальном компьютере:
http://127.0.0.1:8000/redoc/

### документация на удаленном сервере:
http://158.160.46.62/redoc/

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
