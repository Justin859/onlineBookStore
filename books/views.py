import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.forms import formset_factory
from django.contrib.postgres.search import SearchVector, TrigramDistance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from .forms import BookForm
from .models import *

# Create your views here.

def index(request):

    data = {'name':'justin', 'surname':'hammond'}

    with open('data.json', 'w') as f:
        json.dump(data, f)

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
    books = Book.objects.filter(book_category=book_category).order_by('pk')

    paginator = Paginator(books, 3)    
    
    page = request.GET.get('page')

    try:
        book_results = paginator.page(page)
        page_int = int(page)
    except PageNotAnInteger:
        book_results = paginator.page(1)
        page_int = 1
    except EmptyPage:
        book_results = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'book_results': book_results, 'books': books, 'categories': categories, 'book_category': book_category, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def authors(request):
    authors = Author.objects.all().order_by('author_name')
    categories = BOOK_CATEGORIES

    paginator = Paginator(authors, 6)    

    page = request.GET.get('page')

    try:
        author_result = paginator.page(page)
        page_int = int(page)
    except PageNotAnInteger:
        author_result = paginator.page(1)
        page_int = 1
    except EmptyPage:
        author_result = paginator.page(paginator.num_pages)

    return render(request, 'authors.html', {'authors': authors, 'author_result': author_result, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def author_detail(request, author_name):
    categories = BOOK_CATEGORIES

    author = get_object_or_404(Author, author_name=author_name)

    return render(request, 'author_detail.html', {'author': author, 'categories': categories})

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

    categories = BOOK_CATEGORIES

    query = request.GET.get('query')
    results = []

    distance_author = Book.objects.annotate(
        distance=TrigramDistance('book_author', query),
    ).filter(distance__lte=0.8).order_by('distance')

    distance_title = Book.objects.annotate(
        distance=TrigramDistance('book_title', query),
    ).filter(distance__lte=0.8).order_by('distance')

    results.append(distance_title)
    results.append(distance_author)

    result = [a for a in results if a.count() != 0]
    results = result

    try:
        paginator = Paginator(results[0], 3)
    except:
        paginator = Paginator(results, 3)    
    
    page = request.GET.get('page')

    try:
        book_results = paginator.page(page)
        page_int = int(page)
    except PageNotAnInteger:
        book_results = paginator.page(1)
        page_int = 1
    except EmptyPage:
        book_results = paginator.page(paginator.num_pages)
         
    return render(request, 'search.html', {'book_results': book_results, 'query': query, 'results': results, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def api(request):
    books_json = serializers.serialize('json', Book.objects.all(), fields=('book_title'))
    return HttpResponse(books_json, content_type='application/json')