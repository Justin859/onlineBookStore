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

import detail_views.views
import payment_views.views

from django.views.decorators.csrf import csrf_exempt

from .forms import BookForm, CheckOutForm
from .models import *

# Create your views here.

def index(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.order_by('book_title')
    categories = BOOK_CATEGORIES

    return render(request, 'index.html', {'number_of_items': number_of_items, 'categories': categories})


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
         
    return render(request, 'detail_views/search.html', {'number_of_items': number_of_items,'book_results': book_results, 'query': query, 'results': results, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

def api(request):
    books_json = serializers.serialize('json', Book.objects.all(), fields=('book_title', 'book_author'))
    
    return HttpResponse(books_json, content_type='application/json')