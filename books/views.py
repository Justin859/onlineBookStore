from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.forms import formset_factory
from django.contrib.postgres.search import SearchVector, TrigramDistance

from .forms import BookForm, SearchForm
from .models import *

# Create your views here.

def index(request):

    if request.method == 'GET':
        form = SearchForm(request.GET)

    books = Book.objects.order_by('book_title')
    recomended_books = []
    categories = BOOK_CATEGORIES
    for book in books:
        if book.book_recomended:
            recomended_books.append(book)
    
    return render(request, 'index.html', {'recomended_books': recomended_books, 'books': book, 'categories': categories})

def book_detail(request, book_title):

    categories = BOOK_CATEGORIES
    book = get_object_or_404(Book, book_title=book_title)

    if request.method == 'POST':
        new_item = BookCartItems.objects.create(
            cart_pk = request.user.pk,
            cart_item_id = book.pk,
            item_title = book.book_title,
            item_price = book.book_price,
            item_quantity = 1,
        )
        messages.success(request, "The book '" + book.book_title + "', Has been added to your cart")
    return render(request, 'detail.html', {'book': book, 'categories': categories})

def book_category(request, book_category):
    categories = BOOK_CATEGORIES
    books = Book.objects.filter(book_category=book_category)

    return render(request, 'category.html', {'books': books, 'categories': categories, 'book_category': book_category})
def cart(request):
    cart_items = []
    cart = BookCartItems.objects.filter(cart_pk=request.user.pk)
    BookFormSet = formset_factory(BookForm, extra=0)
    formset = BookFormSet(initial=cart_items)
    categories = BOOK_CATEGORIES

    for item in cart:
        cart_items.append({'book_id': item.cart_item_id, 'title': item.item_title, 'price': item.item_price, 'quantity': item.item_quantity, 'delete': False})

    if request.method == 'POST':
        formset = BookFormSet(request.POST)
        for form in formset:
            if formset.is_valid():
                book_id = form.cleaned_data['book_id']
                title = form.cleaned_data['title']
                price = form.cleaned_data['price']
                quantity = form.cleaned_data['quantity']
                delete = form.cleaned_data['delete']

                if delete == 'True':
                    BookCartItems.objects.filter(item_title=title, cart_pk=request.user.pk).delete()
                else:
                    BookCartItems.objects.filter(item_title=title, cart_pk=request.user.pk).update(item_quantity=quantity)
        return HttpResponseRedirect('/cart/')    
    else:
        formset = BookFormSet(initial=cart_items)

    return render(request, 'cart.html', {'categories': categories, 'formset': formset, 'cart_items': cart_items, 'cart': cart})

def search(request):
    query = request.GET.get('query')
    results = []

    distance_author = Book.objects.annotate(
        distance=TrigramDistance('book_author', query),
    ).filter(distance__lte=0.7).order_by('distance')

    distance_title = Book.objects.annotate(
        distance=TrigramDistance('book_title', query),
    ).filter(distance__lte=0.7).order_by('distance')

    results.append([distance_author, distance_title])

    return render(request, 'search.html', {'results': results, 'query': query})