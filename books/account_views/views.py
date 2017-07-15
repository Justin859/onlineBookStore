from books.views import *
from ..models import *
from django.contrib.auth.decorators import login_required

# methods
@login_required(login_url='/login/' ,redirect_field_name='/login/')
def profile(request):
    number_of_items = BookCartItems.objects.filter(cart_pk=request.user.pk).count()
    categories = BOOK_CATEGORIES

    return render(request, 'accounts/profile.html',
    {
        'number_of_items': number_of_items,
        'categories': categories,
    })