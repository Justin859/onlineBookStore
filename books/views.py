from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.forms import formset_factory

from .forms import BookForm
from .models import *

# Create your views here.

def index(request):
    # return HttpResponse('Hello from Python!')
    try:
        request.session['cart_total']
        request.session['cart_items']
    except KeyError:
        request.session['cart_total'] = 0
        request.session['cart_items'] = {}

    books = Book.objects.order_by('book_title')
    recomended_books = []
    categories = BOOK_CATEGORIES
    for book in books:
        if book.book_recomended:
            recomended_books.append(book)
    
    return render(request, 'index.html', {'recomended_books': recomended_books, 'books': book, 'categories': categories, 'cart_total': request.session['cart_total'], 'cart_items': request.session['cart_items']})

def book_detail(request, book_title):

    categories = BOOK_CATEGORIES
    book = get_object_or_404(Book, book_title=book_title)
    try:
        request.session['cart_total']
        request.session['cart_items']
    except KeyError:
        request.session['cart_total'] = 0
        request.session['cart_items'] = {}
   
    if request.method == 'POST':
        request.session['cart_total'] += 1
        request.session['cart_items'][book.id] = {}
        request.session['cart_items'][book.id]['book_title'] = book.book_title
        request.session['cart_items'][book.id]['book_price'] = float(book.book_price)
        request.session['cart_items'][book.id]['book_quantity'] = 1
        messages.success(request, "The book '" + book.book_title + "', Has been added to your cart")
        return HttpResponseRedirect('/book/' + book.book_title)
    return render(request, 'detail.html', {'book': book, 'categories': categories, 'cart_total': request.session['cart_total'], 'cart_items': request.session['cart_items']})

def cart(request):

    try:
        request.session['cart_total']
        request.session['cart_items']
    except KeyError:
        request.session['cart_total'] = 0
        request.session['cart_items'] = {}

    cartItems = []
    for key, value in request.session['cart_items'].items():
        cartItems.append({'book_id': key, 'title': value['book_title'], 'price': value['book_price'], 'quantity': value['book_quantity']})

    BookFormSet = formset_factory(BookForm, extra=0)
    formset = BookFormSet(initial=cartItems)

    if request.method == 'POST':
        formset = BookFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                book_id = form.cleaned_data['book_id']
                title = form.cleaned_data['title']
                price = form.cleaned_data['price']
                quantity = form.cleaned_data['quantity']

                request.session['cart_total'] += 0
                request.session['cart_items'][book_id]['book_quantity'] = quantity
    else:
        formset = BookFormSet(initial=cartItems)

    categories = BOOK_CATEGORIES
    return render(request, 'cart.html', {'categories': categories, 'cart_total': request.session['cart_total'], 'cart_items': request.session['cart_items'], 'formset': formset})
