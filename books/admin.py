from django.contrib import admin
from django.db import models
# Register your models here.
from .models import *

admin.site.register(Book)
admin.site.register(BookCartItems)
admin.site.register(Author)
admin.site.register(Order)
admin.site.register(OrderedItem)

