# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request, 'books/index.html')


def register(request):
    result = User.objects.register(request.POST)
    if 'err_messages' in result:
        for error in result['err_messages']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result['new_user'].id
        print(request.session['user_id'])
        messages.success(request, "You have successfully registered. Please login now")
        return redirect('/')


def login(request):
    result = User.objects.login(request.POST)
    if 'err_messages' in result:
        for error in result['err_messages']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result['logged_user'].id
        print(request.session['user_id'])
        return redirect('/books')


def logout(request):
    request.session.clear()
    return redirect('/')


def books(request):
    if request.method == 'POST':
        result = Book.objects.add_book_review(request.POST, request.session['user_id'])
        book = result['new_book']
        return redirect('/books/{}'.format(book.id))
    else:
        logged_user = User.objects.get(id=request.session['user_id'])
        recent_reviews = Review.objects.all().order_by('-created_at')[:3]
        reviewed_books = Book.objects.exclude(reviews__review="")
        context = {
            'user': logged_user,
            'reviews': recent_reviews,
            'books': reviewed_books
        }
        return render(request, 'books/books.html', context)


def add_book(request):
    context = {
        'authors': Author.objects.all()
    }
    return render(request, 'books/new.html', context)


def show(request, book_id):
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book=book)
    context = {
        'book': book,
        'all_reviews': reviews,
    }
    return render(request, 'books/show.html', context)


def review(request, book_id):
    book = Book.objects.get(id=book_id)
    user = User.objects.get(id=request.session['user_id'])
    Review.objects.create(review=request.POST['review'], rating=request.POST['rating'], user=user, book=book)
    return redirect('/books/{}'.format(book.id))


def show_user(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user
    }
    return render(request, 'books/user.html', context)






















