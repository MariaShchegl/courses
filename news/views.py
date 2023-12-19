from django.shortcuts import render, HttpResponseRedirect
from .models import News, Comment
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import Http404
from django.db.models import Q
from events.models import Category
from events.forms import CommentForm
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import pytz

# Create your views here.

@api_view(['GET'])
def index(request):
    categories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    new_article = News.objects.filter(is_show=True).order_by('-created_at')[:3]

    context = {'new_article': new_article, 'categories': categories}

    if request.GET.get('search'):
        news = News.objects.filter(title__icontains=request.GET.get('search'), is_show=True).order_by('created_at')
    else:
        news = News.objects.filter(is_show=True).order_by('created_at')

        if request.GET.get('subsubcategories') and request.GET.get('subsubcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            context.update({'subsubcategories':subsubcategories, 'subcategories':subcategories})

            news = news.filter(category__alias=request.GET.get('subsubcategories'))

        elif request.GET.get('subcategories') and request.GET.get('subcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            context.update({'subsubcategories': subsubcategories, 'subcategories': subcategories})

            str_query = "Q(category__alias='" + request.GET.get('subcategories') + "')"
            for item in subsubcategories:
                str_query += " | Q(category__alias='" + item.alias + "')"

            news = news.filter(eval(str_query))

        elif request.GET.get('categories') and request.GET.get('categories') != '0':
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            context.update({'subcategories': subcategories})

            str_query = "Q(category__alias='" + request.GET.get('categories') + "')"
            for item in subcategories:
                str_query += " | Q(category__alias='" + item.alias + "')"
                subsubcategories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=item.id).order_by('category')
                for itemSub in subsubcategories:
                    str_query += " | Q(category__alias='" + itemSub.alias + "')"

            news = news.filter(eval(str_query))

    news = news.distinct()

    paginator = Paginator(news, 5)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    list_page = list(paginator.get_elided_page_range(page_number, on_each_side=1))

    context.update({'news': page_obj, 'paginationList': list_page})

    return render(request, 'news/news.html', context)

@api_view(['GET'])
def show(request, alias=""):
    categories = Category.objects.filter(access__gte=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    new_news = News.objects.filter(is_show=True).order_by('-created_at')[:3]
    try:
        if request.user.is_staff:
            article = News.objects.get(alias=alias)
        else:
            article = News.objects.get(is_show=True, alias=alias)
    except News.DoesNotExist:
        raise Http404("Новость не найдена")

    form = CommentForm()

    context = {'form':form, 'new_news': new_news, 'categories': categories, 'article': article}

    return render(request, 'news/note.html', context)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addComment(request):
    try:
        article = News.objects.get(is_show=True, alias=request.POST.get('alias'))
    except News.DoesNotExist:
        return HttpResponseRedirect(reverse('news:index'))

    minskTz = pytz.timezone("Europe/Minsk")

    if request.user.date_muted:
        if request.user.date_muted > datetime.now(minskTz):
            return HttpResponseRedirect(reverse('news:index'))

    parent_id = request.POST.get('parent-id')

    if parent_id != '0':
        try:
            comment = Comment.objects.get(id=parent_id)
            if comment.parent_id != 0:
                parent_id = comment.parent_id
        except Comment.DoesNotExist:
            return HttpResponseRedirect(reverse('news:index'))

    form = CommentForm(data=request.POST)
    if form.is_valid():
        Comment.objects.create(user=request.user, news=article, parent_id=parent_id, comment=form.data['comment'])

    return HttpResponseRedirect(reverse('news:show', kwargs={'alias': request.POST.get('alias')}))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteComment(request, id=0):
    try:
        article = News.objects.get(is_show=True, alias=request.POST.get('alias'))
    except News.DoesNotExist:
        return HttpResponseRedirect(reverse('news:index'))

    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse('news:index'))

    if not (comment.user == request.user or request.user.has_perm('news.delete_comment')):
        return HttpResponseRedirect(reverse('news:index'))

    comment.delete()

    return HttpResponseRedirect(reverse('news:show', kwargs={'alias': request.POST.get('alias')}))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def editComment(request, id=0):
    try:
        article = News.objects.get(is_show=True, alias=request.POST.get('alias'))
    except News.DoesNotExist:
        return HttpResponseRedirect(reverse('news:index'))

    minskTz = pytz.timezone("Europe/Minsk")

    if request.user.date_muted:
        if request.user.date_muted > datetime.now(minskTz):
            return HttpResponseRedirect(reverse('news:index'))

    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse('news:index'))

    if not (comment.user == request.user or request.user.has_perm('news.change_comment')):
        return HttpResponseRedirect(reverse('news:index'))

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment.comment = form.data['comment']
        comment.is_publish = False
        comment.save()
    else:
        return HttpResponseRedirect(reverse('news:index'))

    return HttpResponseRedirect(reverse('news:show', kwargs={'alias': request.POST.get('alias')}))
