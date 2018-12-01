"""books URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import main_page, SearchView

from django.contrib.sitemaps.views import sitemap
from books.sitemaps import *

from .views import Rss, account_detail

from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from authorization.views import LoginView, register

handler404 = 'books.views.error_404'

sitemaps = {
    'articles_category': ArticlesCategorySitemap,
    'video_category': VideoCategorySitemap,
    'books_category': BookCategorySitemap,
    'books': BookSitemap,
    'courses': CourseSitemap,
    'articles': ArticleSitemap,
    'static': StaticViewSitemap
}

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('main_page_url')), name='logout_url'),
    path('rss.xml', Rss(), name='rss_url'),
    path('admin/', admin.site.urls),
    path('search/', SearchView.as_view(), name='search_url'),
    path('', main_page, name='main_page_url'),
    path('books/', include('booklist.urls')),
    path('videos/', include('video.urls')),
    path('articles/', include('articles.urls')),
    path('sitemaps.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('register/', register, name='register_url'),
    path('account/', account_detail, name='account_url')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
