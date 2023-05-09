import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, TitleGenre
from users.models import User


def read_users():
    with open("static/data/users.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            User.objects.create(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=[4],
                first_name=row[5],
                last_name=row[6]
            )
        return "Файл users.csv готов!"


def read_category():
    with open("static/data/category.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            Category.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        return "Файл category.csv готов!"


def read_genre():
    with open("static/data/genre.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            Genre.objects.create(
                id=row[0],
                name=row[1],
                slug=row[2]
            )
        return "Файл genre.csv готов!"


def read_titles():
    with open("static/data/titles.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            Title.objects.create(
                id=row[0],
                name=row[1],
                year=row[2],
                category=Category.objects.get(id=row[3])
            )
        return "Файл titles.csv готов!"


def read_genre_title():
    with open("static/data/genre_title.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            TitleGenre.objects.create(
                id=row[0],
                title=Title.objects.get(id=row[1]),
                genre=Genre.objects.get(id=row[2])
            )
        return "Файл genre_title.csv готов!"


def read_reviews():
    with open("static/data/review.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            Review.objects.create(
                id=row[0],
                title_id=row[1],
                text=row[2],
                author=User.objects.get(id=row[3]),
                score=row[4],
                pub_date=row[5]
            )
        return "Файл review.csv готов!"


def read_comments():
    with open("static/data/comments.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        next(file_reader)
        for row in file_reader:
            Comment.objects.create(
                id=row[0],
                review=Review.objects.get(id=row[1]),
                text=row[2],
                author=User.objects.get(id=row[3]),
                pub_date=row[4]
            )
        return "Файл comments.csv готов!"


class Command(BaseCommand):
    help = 'Импортирует информацию из static/data'

    def handle(self, *args, **options):
        function_list = [
            read_users,
            read_category,
            read_titles,
            read_genre,
            read_genre_title,
            read_reviews,
            read_comments,
        ]
        for func in function_list:
            text = func()
            self.stdout.write(self.style.SUCCESS(text))
        self.stdout.write(self.style.SUCCESS('ура получилось!'))
