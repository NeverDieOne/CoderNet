from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import redirect
from .forms import CommentForm


# Create your views here.
def category_list(request):
    categories = Category.objects.all()
    courses = Course.objects.all()

    # Пагинатор начало
    paginator = Paginator(courses, 12)
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
        'categories': categories,
        'courses': courses,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'page_object': page,
    }
    return render(request, 'video/category_list.html', context=context)


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    categories = Category.objects.all()
    courses = Course.objects.filter(category=category)

    # Пагинатор начало
    paginator = Paginator(courses, 12)
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
        'categories': categories,
        'category': category,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url,
        'page_object': page,
        'courses': courses
    }
    return render(request, 'video/category_detail.html', context=context)


def course_detail(request, **kwargs):
    categories = Category.objects.all()
    course = Course.objects.get(slug=kwargs['slug'])
    comments = Comments.objects.filter(comment_article__slug__iexact=kwargs['slug'])
    form_comments = CommentForm
    context = {
        'comments': comments,
        'form_comments': form_comments,
        'categories': categories,
        'course': course
    }
    return render(request, 'video/course_detail.html', context=context)


def addcomment(request, slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_author_course = request.user
            comment.comment_article = Course.objects.get(slug__iexact=slug)
            form.save()
    return redirect(Course.objects.get(slug__iexact=slug))
