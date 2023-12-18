from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from events.models import Category
from .models import History
from django.http import Http404
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
def index(request):
    categories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    new_article = History.objects.filter(is_show=True).order_by('-created_at')[:3]

    context = {'new_article': new_article, 'categories': categories}

    if request.GET.get('search'):
        histories = History.objects.filter(title__icontains=request.GET.get('search'), is_show=True).order_by('created_at')
    else:
        histories = History.objects.filter(is_show=True).order_by('created_at')

        if request.GET.get('subsubcategories') and request.GET.get('subsubcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                       parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                    parent_id=category.id).order_by('category')
            context.update({'subsubcategories': subsubcategories, 'subcategories': subcategories})

            histories = histories.filter(category__alias=request.GET.get('subsubcategories'))

        elif request.GET.get('subcategories') and request.GET.get('subcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                    parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                       parent_id=category.id).order_by('category')
            context.update({'subsubcategories': subsubcategories, 'subcategories': subcategories})

            str_query = "Q(category__alias='" + request.GET.get('subcategories') + "')"
            for item in subsubcategories:
                str_query += " | Q(category__alias='" + item.alias + "')"

            histories = histories.filter(eval(str_query))

        elif request.GET.get('categories') and request.GET.get('categories') != '0':
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                    parent_id=category.id).order_by('category')
            context.update({'subcategories': subcategories})

            str_query = "Q(category__alias='" + request.GET.get('categories') + "')"
            for item in subcategories:
                str_query += " | Q(category__alias='" + item.alias + "')"
                subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                           parent_id=item.id).order_by('category')
                for itemSub in subsubcategories:
                    str_query += " | Q(category__alias='" + itemSub.alias + "')"

            histories = histories.filter(eval(str_query))

    histories = histories.distinct()

    paginator = Paginator(histories, 5)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    list_page = list(paginator.get_elided_page_range(page_number, on_each_side=1))

    context.update({'histories': page_obj, 'paginationList': list_page})

    return render(request, 'histories/history.html', context)

@api_view(['GET'])
def show(request, alias=""):
    categories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    new_article = History.objects.filter(is_show=True).order_by('-created_at')[:3]
    try:
        if request.user.is_staff:
            article = History.objects.get(alias=alias)
        else:
            article = History.objects.get(is_show=True, alias=alias)
    except History.DoesNotExist:
        raise Http404("История не найдена")

    context = {'new_article': new_article, 'categories': categories, 'article': article}

    return render(request, 'histories/note.html', context)