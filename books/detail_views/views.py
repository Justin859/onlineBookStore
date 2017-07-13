from books.views import *
from ..models import *

# methods       

def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

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

    return render(request, 'detail_views/category.html', {'number_of_items': number_of_items, 'book_results': book_results, 'books': books, 'categories': categories, 'book_category': book_category, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})


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
    return render(request, 'detail_views/book_detail.html', {'number_of_items': number_of_items, 'book': book, 'categories': categories, 'book_in_cart': book_in_cart})

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

    return render(request, 'detail_views/authors.html', {'number_of_items': number_of_items, 'authors': authors, 'author_result': author_result, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})

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

    return render(request, 'detail_views/author_detail.html', {'number_of_items': number_of_items, 'author': author, 'categories': categories, 'book_results': book_results, 'page': page, 'page_int': page_int, 'paginator': paginator, 'range': range(paginator.num_pages)})

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
      
    return render(request, 'detail_views/library.html', {'number_of_items': number_of_items, 'book_results': book_results, 'categories': categories, 'page': page, 'page_int': page_int , 'paginator': paginator, 'range': range(paginator.num_pages)})    
