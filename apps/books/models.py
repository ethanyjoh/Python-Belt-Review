from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import bcrypt


class UserManager(models.Manager):
    def register(self, datafromhtml):
        errors = []

        if(len(datafromhtml['name']) < 2):
            errors.append("Your name should be at least 2 characters")
        if(len(datafromhtml['password']) < 8):
            errors.append("Your password should be at least 8 characters")
        if(datafromhtml['password'] != datafromhtml['password_confirm']):
            errors.append("Your password and you password confirmation must match")
        try:
            validate_email(datafromhtml['email'])
        except ValidationError as e:
            errors.append("your email must be in a valid format")

        if errors:
            return {'err_messages': errors}
        else:
            hash_password = bcrypt.hashpw(datafromhtml['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(name=datafromhtml['name'], email=datafromhtml['email'], password=hash_password)
            return {'new_user': user}

    def login(self, datafromhtml):
        try:
            user = User.objects.get(email=datafromhtml['email'])
            if bcrypt.checkpw(datafromhtml['password'].encode(), user.password.encode()):
                return {'logged_user': user}
            else:
                return {'err_messages': ['Email/Password invalid. Please try again']}
        except:
            return {'err_messages': ['Email you have entered does not exists. Please register your email']}


class BookManager(models.Manager):
    def add_book_review(self, datafromhtml, user_id):
        if len(datafromhtml['new_author']) > 1:
            author = Author.objects.create(name=datafromhtml['new_author'])
        else:
            author = Author.objects.get(id=datafromhtml['author_id'])

        new_book = self.create(title=datafromhtml['title'], author=author)
        user = User.objects.get(id=user_id)
        new_review = Review.objects.create(review=datafromhtml['review'], rating=datafromhtml['rating'], user=user, book=new_book)
        return {'new_book': new_book}


class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()


class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name='reviews')
    book = models.ForeignKey(Book, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
