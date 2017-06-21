from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import books.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', books.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/(?P<book_title>[\w\s\']+)/$', books.views.book_detail, name='book_detail'),
    url(r'^category/(?P<book_category>[\w\s\']+)/$', books.views.book_category, name='book_category'),
    url(r'^cart/', books.views.cart, name='cart'),
    url(r'^search/$', books.views.search, name='search'),
]
