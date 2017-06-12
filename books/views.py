from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore

from .models import *

shopping_cart = SessionStore()
shopping_cart.create()
shopping_cart['cart_total'] = 0
shopping_cart['books'] = {}
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    books = Book.objects.order_by('book_title')
    recomended_books = []
    categories = BOOK_CATEGORIES

    for book in books:
        if book.book_recomended:
            recomended_books.append(book)
    
    return render(request, 'index.html', {'recomended_books': recomended_books, 'books': book, 'categories': categories, 'cart_total': shopping_cart['cart_total']})

def book_detail(request, book_title):
    categories = BOOK_CATEGORIES
    book = get_object_or_404(Book, book_title=book_title)
    if request.method == 'POST':
        shopping_cart['cart_total'] += 1
        shopping_cart['books'][book.pk] = {}
        shopping_cart['books'][book.pk]['book_title'] = book.book_title
        shopping_cart['books'][book.pk]['book_price'] = book.book_price
        shopping_cart['books'][book.pk]['book_quantity'] = 1

        messages.success(request, "The book '" + book.book_title + "', Has been added to your cart")
        return HttpResponseRedirect('/book/' + book.book_title)
    return render(request, 'detail.html', {'book': book, 'categories': categories, 'cart_total': shopping_cart['cart_total']})

def cart(request):
    categories = BOOK_CATEGORIES
    books = []
    for book in shopping_cart['books']:
        books.append(book)
    return render(request, 'cart.html', {'books': books, 'categories': categories, 'cart_total': shopping_cart['cart_total'], 'cart_books': shopping_cart['books']})
