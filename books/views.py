import json
import decimal

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.forms import formset_factory
from django.contrib.postgres.search import SearchVector, TrigramDistance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers

from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from .forms import BookForm
from .models import *

# methods

def show_me_the_money(sender, **kwargs):

    total_bill = 0
    for item in cart:
        total_bill += item.item_price

    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        if ipn_obj.reciever_email != "justinhammond859@gmail.com":

            return False
        if ipn_obj.amount != total_bill:

            return False
    else:
        return False
valid_ipn_received.connect(show_me_the_money)                  

def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

# Create your views here.

def index(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.order_by('book_title')
    categories = BOOK_CATEGORIES
    
    return render(request, 'index.html', {'number_of_items': number_of_items, 'categories': categories})

def book_detail(request, book_title):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    categories = BOOK_CATEGORIES
    book_cart = BookCartItems.objects.all()
    book_in_cart = False

    book = get_object_or_404(Book, book_title=book_title)

    for book_item in book_cart:
        if book.book_title == book_item.item_title:
            book_in_cart = True

    if request.method == 'POST':
        new_item = BookCartItems.objects.create(
            cart_pk = request.user.pk,
            cart_item_id = book.pk,
            item_title = book.book_title,
            item_price = book.book_price,
            item_quantity = 1,
        )
        messages.success(request, "The book '" + book.book_title + "', Has been added to your cart")
        return HttpResponseRedirect('/book/' + book.book_title)
    return render(request, 'book_detail.html', {'number_of_items': number_of_items, 'book': book, 'categories': categories, 'book_in_cart': book_in_cart})

def book_category(request, book_category):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
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

    return render(request, 'category.html', {'number_of_items': number_of_items, 'book_results': book_results, 'books': books, 'categories': categories, 'book_category': book_category, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def authors(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
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

    return render(request, 'authors.html', {'number_of_items': number_of_items, 'authors': authors, 'author_result': author_result, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def author_detail(request, author_name):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    categories = BOOK_CATEGORIES
    books_by_author = Book.objects.filter(book_author=author_name).order_by('id')
    author = get_object_or_404(Author, author_name=author_name)

    paginator = Paginator(books_by_author, 3)

    page = request.GET.get('page')

    try:
        book_results = paginator.page(page)
        page_int = int(page)
    except PageNotAnInteger:
        book_results = paginator.page(1)
        page_int = 1
    except EmptyPage:
        book_results = paginator.page(paginator.num_pages)        

    return render(request, 'author_detail.html', {'number_of_items': number_of_items, 'author': author, 'categories': categories, 'book_results': book_results, 'page': page, 'page_int': page_int, 'paginator': paginator, 'range': range(paginator.num_pages)})

def library(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.filter(book_recomended=True).order_by('id')
    categories = BOOK_CATEGORIES
    books_chunks = chunks(books, 4)  
    paginator = Paginator(books_chunks, 4)    

    page = request.GET.get('page')

    try:
        book_results = paginator.page(page)
        page_int = int(page)
    except PageNotAnInteger:
        book_results = paginator.page(1)
        page_int = 1
    except EmptyPage:
        book_results = paginator.page(paginator.num_pages)
      
    return render(request, 'library.html', {'number_of_items': number_of_items, 'book_results': book_results, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})    

def cart(request):
    cart_items = []
    cart = BookCartItems.objects.filter(cart_pk=request.user.pk)
    BookFormSet = formset_factory(BookForm, extra=0)
    formset = BookFormSet(initial=cart_items)
    categories = BOOK_CATEGORIES
    number_of_items = cart.count()
    total_bill = 0
    for item in cart:
        total_bill += item.item_price
    total_excl = str(round(total_bill - total_bill * (decimal.Decimal(.14)), 2))
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
                    price = Book.objects.filter(book_title=title)[0]
                    BookCartItems.objects.filter(item_title=title, cart_pk=request.user.pk).update(item_price=price.book_price * quantity)

        return HttpResponseRedirect('/cart/')    
    else:
        formset = BookFormSet(initial=cart_items)
    
    total_number_of_items = 0
    for item in cart:
        total_number_of_items += item.item_quantity
    return render(request, 'cart.html', {'total_number_of_items': total_number_of_items, 'total_excl': total_excl,'total_bill': total_bill,'number_of_items': number_of_items, 'categories': categories, 'formset': formset, 'cart_items': cart_items, 'cart': cart})

def search(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    categories = BOOK_CATEGORIES

    query = request.GET.get('query')
    results = []

    distance_author = Book.objects.annotate(
        distance=TrigramDistance('book_author', query),
    ).filter(distance__lte=0.7).order_by('distance')

    distance_title = Book.objects.annotate(
        distance=TrigramDistance('book_title', query),
    ).filter(distance__lte=0.7).order_by('distance')

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
         
    return render(request, 'search.html', {'number_of_items': number_of_items,'book_results': book_results, 'query': query, 'results': results, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def view_that_asks_for_money(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.order_by('book_title')
    cart = BookCartItems.objects.filter(cart_pk=request.user.pk)
    total_bill = 0
    for item in cart:
        total_bill += item.item_price
    test = request.META['REMOTE_ADDR']
    categories = BOOK_CATEGORIES

    paypal_dict = {
        "business": "justinhammond859@gmail.com",
        "amount": total_bill,
        "item_name": "Test Cart",
        "invoice" : "0001",
        "notify_url": "http://desolate-basin-41691.herokuapp.com" + reverse('paypal-ipn'),
        "return_url": "http://desolate-basin-41691.herokuapp.com/success",
        "cancel_return": "http://desolate-basin-41691.herokuapp.com/cancel",
        "currency_code": "ZAR",
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'payment.html', {'form': form, 'total_bill': total_bill, 'number_of_items': number_of_items, 'categories': categories})

@csrf_exempt
def success(request):

    return render(request, 'success.html', {})

def cancel(request):

    return render(request, 'cancel.html', {})

@csrf_exempt
def notify(request):

    return HttpResponse()

def api(request):
    books_json = serializers.serialize('json', Book.objects.all(), fields=('book_title', 'book_author'))
    
    return HttpResponse(books_json, content_type='application/json')