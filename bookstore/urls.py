from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

import books.views
import books.detail_views.views
import books.payment_views.views
import books.account_views.views
# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', books.views.index, name='index'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^accounts/signup/$', books.views.signUp, name='signup'),
    url(r'^accounts/profile/$', books.account_views.views.profile, name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^book/(?P<book_title>[\w\s\']+)/$', books.detail_views.views.book_detail, name='book_detail'),
    url(r'^authors/$', books.detail_views.views.authors, name='authors'),
    url(r'^author/(?P<author_name>[\w\s\']+)/$', books.detail_views.views.author_detail, name='author_detail'),
    url(r'^category/(?P<book_category>[\w\s\']+)/$', books.detail_views.views.book_category, name='book_category'),
    url(r'^library/$', books.detail_views.views.library, name='library'),
    url(r'^cart/', books.payment_views.views.cart, name='cart'),
    url(r'^api/data/$', books.views.api, name='api'),
    url(r'^search/$', books.views.search, name='search'),
    url(r'^payment/$', books.payment_views.views.view_that_asks_for_money, name='payment'),
    url(r'^success/$', books.payment_views.views.success, name='success'),
    url(r'^cancel/$', books.payment_views.views.cancel, name='cancel'),
    url(r'^notify/', books.payment_views.views.notify, name='notify'),
]
