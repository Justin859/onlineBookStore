import uuid

from django.db import models
from django.conf import settings
# Create your models here.

from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in

NUMBER_OF_STARS = (
    ('0.5', '1/2 stars'),
    ('1', '1 stars'),
    ('1.5', '1 1/2 stars'),
    ('2', '2 stars'),
    ('2.5', '2 1/2 stars'),
    ('3', '3 stars'),
    ('3.5', '3 1/2 stars'),
    ('4', '4 stars'),
    ('4.5', '4 1/2 stars'),
    ('5', '5 stars'),
)

BOOK_CATEGORIES = (
    ('Science fiction', 'Science fiction'),
    ('Fiction', 'Fiction'),
    ('Drama', 'Drama'),
    ('Comedy', 'Comedy'),
    ('Action and Adventure', 'Action and Adventure'),
    ('Romance', 'Romance'),
    ('Mystery', 'Mystery'),
    ('Horror', 'Horror'),
    ('Fantasy', 'Fantasy'),
)

YES_OR_NO = (
    (True, 'Yes'),
    (False, 'No'),
)

class Book(models.Model):
    book_title = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_description = models.TextField(max_length=1000)
    book_category = models.CharField(max_length=255, choices=BOOK_CATEGORIES, default='Science fiction')
    book_image = models.ImageField(upload_to=('images/book-images'), max_length=255)
    book_recomended = models.BooleanField(default=False, choices=YES_OR_NO)
    book_rating = models.CharField(max_length=3, choices=NUMBER_OF_STARS)
    book_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    book_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.book_title

class Author(models.Model):
    author_name = models.CharField(max_length=255)
    author_description = models.TextField()
    author_image = models.ImageField(upload_to=('images/author-images'), max_length=255)
    author_info = models.TextField()

    def __str__(self):
        return self.author_name

class BookCartItems(models.Model):
    cart_pk = models.IntegerField()
    cart_item_id = models.IntegerField()
    item_title = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    item_quantity = models.IntegerField()

    def __str__(self):
        return self.item_title

    class Meta:
        verbose_name = 'Book Cart'
        verbose_name_plural = 'Book Carts'

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    order_username = models.CharField(max_length=55)
    order_user_pk = models.CharField(max_length=255)
    payment_id = models.UUIDField(default=uuid.uuid4, editable=False)
    pf_payment_id = models.CharField(max_length=255)
    amount_gross = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_of_books = models.IntegerField(default=0)

    def __str__(self):
        return self.order_username + "/"+ str(self.payment_id) + "/" + str(self.created_at)
    
    class META:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderedItem(models.Model):
    order_payment_id = models.CharField(max_length=255, default='0')
    order_user_pk = models.IntegerField(default=0, editable=False)
    item_id = models.CharField(max_length=255)
    item_title = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    item_quantity = models.IntegerField()

    def __str__(self):
        return self.order_payment_id + " " + self.item_title

    class META:
        verbose_name = 'Ordered Item'
        verbose_name_plural = 'Ordered Items'