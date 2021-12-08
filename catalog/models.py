from datetime import date

from django.contrib.auth.models import User
from django.db import models


# class LibraryUser(User):
#     avatar = models.ImageField()


class AuthorManager(models.Manager):
    def young_authors(self):
        return self.filter(birth_date__gt=date(2000, 1, 1))


class Author(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)

    objects = AuthorManager()

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])


class Book(models.Model):
    name = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField(blank=True, null=True)
    genres = models.ManyToManyField('Genre', related_name='books')


class Genre(models.Model):
    name = models.CharField(max_length=256)


class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    STATUS_CHOICES = [
        ('t', 'Taken'),
        ('a', 'Available'),
        ('m', 'Maintenance')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a')
