from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    books = Book.objects.order_by('book_title')
    recomended_books = []

    for book in books:
        if book.book_recomended:
            recomended_books.append(book)
    
    return render(request, 'index.html', {'recomended_books': recomended_books, 'books': book})