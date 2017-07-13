from books.views import *
from ..models import *
from books.forms import *

from django.views.decorators.csrf import csrf_exempt

# methods               

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def success(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.order_by('book_title')
    cart = BookCartItems.objects.filter(cart_pk=request.user.pk)

    total_bill = 0
    for item in cart:
        total_bill += item.item_price
    total_number_of_items = 0
    for item in cart:
        total_number_of_items += item.item_quantity

    categories = BOOK_CATEGORIES
    return render(request, 'payment_views/success.html',
    {
         'total_number_of_items': total_number_of_items,
         'total_bill': total_bill,
         'number_of_items': number_of_items,
         'categories': categories
    })

def cancel(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.order_by('book_title')
    cart = BookCartItems.objects.filter(cart_pk=request.user.pk)

    total_bill = 0
    for item in cart:
        total_bill += item.item_price
    total_number_of_items = 0
    for item in cart:
        total_number_of_items += item.item_quantity

    categories = BOOK_CATEGORIES
    return render(request, 'payment_views/cancel.html',
    {
         'total_number_of_items': total_number_of_items,
         'total_bill': total_bill,
         'number_of_items': number_of_items,
         'categories': categories
    })

def view_that_asks_for_money(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    books = Book.objects.order_by('book_title')
    cart = BookCartItems.objects.filter(cart_pk=request.user.pk)

    total_bill = 0
    for item in cart:
        total_bill += item.item_price
    total_number_of_items = 0
    for item in cart:
        total_number_of_items += item.item_quantity

    categories = BOOK_CATEGORIES

    form = CheckOutForm()

    return render(request, 'payment_views/payment.html',
    {
         'form':form,
         'total_number_of_items': total_number_of_items,
         'total_bill': total_bill,
         'number_of_items': number_of_items,
         'categories': categories
    })

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
    total_number_of_items = 0
    for item in cart:
        total_number_of_items += item.item_quantity

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
                
        messages.success(request, "Your Shopping Cart Has been Updated")

        return HttpResponseRedirect('/cart/')    
    else:
        formset = BookFormSet(initial=cart_items)

    return render(request, 'payment_views/cart.html',
    {
         'total_number_of_items': total_number_of_items,
         'total_excl': total_excl,'total_bill': total_bill,
         'number_of_items': number_of_items,
         'categories': categories,
         'formset': formset,
         'cart_items': cart_items,
         'cart': cart
    })

@csrf_exempt
def notify(request):
    host_ip = get_client_ip(request)
    pf_data = request.POST
    valid_ip = ['41.74.179.194', '41.74.179.195', '41.74.179.196', '41.74.179.197', '41.74.179.200',
                '41.74.179.201', '41.74.179.203','41.74.179.204', '41.74.179.210', '41.74.179.211',
                '41.74.179.212', '41.74.179.217', '41.74.179.218', '197.97.145.156'] 

    cart = BookCartItems.objects.filter(cart_pk=pf_data.get('m_payment_id'))
    total_bill = 0
    for item in cart:
        total_bill += item.item_price

    if host_ip in valid_ip:
        if pf_data.get('payment_status') == 'COMPLETE' and float(pf_data.get('amount_gross').encode('utf-8')) == float(total_bill):
            
            new_order = Order.objects.create(
                order_username = pf_data.get('name_first'),
                order_user_pk = pf_data.get('m_payment_id'),
                pf_payment_id = pf_data.get('pf_payment_id'),
                amount_gross = pf_data.get('amount_gross'),
                quantity_of_books = pf_data.get('custom_int1'),
            )
            checked_out_items = BookCartItems.objects.filter(cart_pk=pf_data.get('m_payment_id'))
            for item in checked_out_items:
                new_order_item = OrderedItem.objects.create(
                    order_payment_id = pf_data.get('pf_payment_id'),
                    order_user_pk = pf_data.get('m_payment_id'),
                    item_id = item.cart_item_id,
                    item_title = item.item_title,
                    item_price = item.item_price,
                    item_quantity = item.item_quantity,
                )            
            checked_out_items = BookCartItems.objects.filter(cart_pk=pf_data.get('m_payment_id')).delete()
        else:
            return HttpResponse(status=400)    
    else:
        return HttpResponse(status=500)        

    return HttpResponse()
