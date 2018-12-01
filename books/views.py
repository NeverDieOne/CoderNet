from django.shortcuts import render, redirect
from video.models import Course
from articles.models import Articles
from booklist.models import Book

from django.core.paginator import Paginator
from django.views import View


def main_page(request):
    return redirect('/books')


class SearchView(View):
    template_name = 'search_new.html'

    def get(self, request, *args, **kwargs):

        question = request.GET.get('search')
        if question is not None:
            books = Book.objects.filter(title__icontains=question)
            courses = Course.objects.filter(title__icontains=question)
            articles = Articles.objects.filter(title__icontains=question)
            objects = list(books) + list(courses) + list(articles)

            last_question = '?search=%s' % question

            # Пагинатор начало
            paginator = Paginator(objects, 15)
            page_number = request.GET.get('page', default=1)
            page = paginator.get_page(page_number)
            is_paginated = page.has_other_pages()

            if page.has_previous():
                prev_url = '{}&page={}'.format(last_question, page.previous_page_number())
            else:
                prev_url = ''

            if page.has_next():
                next_url = '{}&page={}'.format(last_question, page.next_page_number())
            else:
                next_url = ''
            # Пагинатор конец

            context = {
                'question': question,
                'last_question': '?search=%s' % question,
                'is_paginated': is_paginated,
                'prev_url': prev_url,
                'next_url': next_url,
                'page_object': page,

            }
        return render(request, self.template_name, context=context)


#  RSS лента
from django.contrib.syndication.views import Feed


class Rss(Feed):
    title = 'CoderNet Портал для помощи программистам'
    description = 'Последние опубликованные книги'
    link = '/'

    def items(self):
        qs = list(Book.objects.all()) + list(Course.objects.all()) + list(Articles.objects.all())
        return qs

    def item_title(self, item):
        return item.title


#  404 кастом

def error_404(request, exception, template_name='404.html'):
    return render(request, template_name, status=404)


def account_detail(request):
    return render(request, 'account.html')
