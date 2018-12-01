from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator

from .forms import CommentForm
from django.shortcuts import redirect


# Create your views here.
def articles_list(request):
    articles = Articles.objects.all()
    categories = Category.objects.all()

    # Пагинатор начало
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    # Пагинатор конец

    context = {
        'articles': articles,
        'categories': categories,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'page_object': page,
    }
    return render(request, 'articles/article_list.html', context=context)


def article_detail(request, **kwargs):
    article = Articles.objects.get(slug__iexact=kwargs['slug'])
    categories = Category.objects.all()
    comments = Comments.objects.filter(comment_article__slug__iexact=kwargs['slug'])
    form_comments = CommentForm
    context = {
        'article': article,
        'categories': categories,
        'comments': comments,
        'form_comments': form_comments,
    }
    return render(request, 'articles/article_detail.html', context=context)


def category_detail(request, slug):
    category = Category.objects.get(slug__iexact=slug)
    categories = Category.objects.all()
    articles = Articles.objects.filter(category=category)

    # Пагинатор начало
    paginator = Paginator(articles, 12)
    page_number = request.GET.get('page', default=1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    # Пагинатор конец

    context = {
        'category': category,
        'categories': categories,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'page_object': page,
        'articles': articles
    }
    return render(request, 'articles/category_list.html', context=context)


def addcomment(request, slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_author = request.user
            comment.comment_article = Articles.objects.get(slug__iexact=slug)
            form.save()
    return redirect(Articles.objects.get(slug__iexact=slug))
