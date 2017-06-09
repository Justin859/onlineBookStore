import moneyed
from djmoney.models.fields import MoneyField
from django.db import models

# Create your models here.

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
    book_image = models.ImageField(upload_to=('books/static/images/book-images'), max_length=255)
    book_recomended = models.BooleanField(default=False, choices=YES_OR_NO)
    book_rating = models.CharField(max_length=3, choices=NUMBER_OF_STARS)
    book_price = MoneyField(max_digits=8, decimal_places=2, default=0, default_currency='ZAR')
    book_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.book_title
