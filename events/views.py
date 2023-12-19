from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.urls import reverse
from .models import City, TypeCity, Category, Age, Event, Area, District, Comment, Venue, Street, Photo
from .forms import CommentForm, EventForm
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.crypto import get_random_string
from django.contrib import messages
import pytz, json

# Create your views here.

def index(request):
    categories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    ages = Age.objects.filter(is_publish=True)
    new_events = Event.objects.filter(is_publish=True, is_show=True, type_event=2).order_by('-created_at')[:3]
    areas = Area.objects.filter(is_publish=True)
    context = {'categories': categories, 'areas': areas, 'ages': ages, 'new_events': new_events}

    if request.GET.get('search'):
        events = Event.objects.filter(Q(title__icontains=request.GET.get('search')) | Q(description__icontains=request.GET.get('search'))).filter(is_publish=True, is_show=True, type_event=2).order_by('created_at')
    else:
        events = Event.objects.filter(is_publish=True, is_show=True, type_event=2).order_by('created_at')

        if request.GET.get('subsubcategories') and request.GET.get('subsubcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            context.update({'subsubcategories':subsubcategories, 'subcategories':subcategories})

            events = events.filter(category__alias=request.GET.get('subsubcategories'))

        elif request.GET.get('subcategories') and request.GET.get('subcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            context.update({'subsubcategories': subsubcategories, 'subcategories': subcategories})

            str_query = "Q(category__alias='" + request.GET.get('subcategories') + "')"
            for item in subsubcategories:
                str_query += " | Q(category__alias='" + item.alias + "')"

            events = events.filter(eval(str_query))

        elif request.GET.get('categories') and request.GET.get('categories') != '0':
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            context.update({'subcategories': subcategories})

            str_query = "Q(category__alias='" + request.GET.get('categories') + "')"
            for item in subcategories:
                str_query += " | Q(category__alias='" + item.alias + "')"
                subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=item.id).order_by('category')
                for itemSub in subsubcategories:
                    str_query += " | Q(category__alias='" + itemSub.alias + "')"

            events = events.filter(eval(str_query))

        if request.GET.get('ages') and request.GET.get('ages') != '0':
            events = events.filter(age_id=request.GET.get('ages'))

        if request.GET.get('districts') and request.GET.get('districts') != '0':
            districts = District.objects.filter(is_publish=True, city_id=request.GET.get('cities'))
            cities = City.objects.filter(is_publish=True, area_id=request.GET.get('areas'))
            context.update({'districts': districts, 'cities': cities})

            events = events.filter(venue__street__district_id=request.GET.get('districts'))

        elif request.GET.get('cities') and request.GET.get('cities') != '0':
            districts = District.objects.filter(is_publish=True, city_id=request.GET.get('cities'))
            cities = City.objects.filter(is_publish=True, area_id=request.GET.get('areas'))
            context.update({'districts': districts, 'cities': cities})

            str_query = "Q(venue__street__district__city_id='" + request.GET.get('cities') + "')"
            for item in districts:
                str_query += " | Q(venue__street__district_id='" + str(item.id) + "')"

            events = events.filter(eval(str_query))

        elif request.GET.get('areas') and request.GET.get('areas') != '0':
            cities = City.objects.filter(is_publish=True, area_id=request.GET.get('areas'))
            context.update({'cities': cities})

            str_query = "Q(venue__street__district__city__area_id='" + request.GET.get('areas') + "')"
            for item in cities:
                str_query += " | Q(venue__street__district__city_id='" + str(item.id) + "')"
                districts = District.objects.filter(is_publish=True, city_id=item.id)
                for itemD in districts:
                    str_query += " | Q(venue__street__district_id='" + str(itemD.id) + "')"

            events = events.filter(eval(str_query))

        if request.GET.get('free'):
            events = events.filter(price__icontains="Бесплатно")

    events = events.distinct()

    paginator = Paginator(events, 5)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    list_page = list(paginator.get_elided_page_range(page_number, on_each_side=1))

    context.update({'events': page_obj, 'paginationList': list_page})
    return render(request, 'events/index.html', context)

def show(request, alias=""):
    try:
        article = Event.objects.get(type_event=2, alias=alias)
        if not (request.user.is_staff or request.user == article.user):
            article = Event.objects.get(is_publish=True, is_show=True, type_event=2, alias=alias)
    except Event.DoesNotExist:
        raise Http404("Объявление не найдено")
    categories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    ages = Age.objects.filter(is_publish=True)
    new_events = Event.objects.filter(is_publish=True, is_show=True, type_event=2).order_by('-created_at')[:3]
    areas = Area.objects.filter(is_publish=True)

    values = article.value.get('social_links')

    form = CommentForm()

    context = {'form': form, 'article': article, 'categories': categories, 'areas': areas, 'ages': ages, 'new_events': new_events, "values": values}

    return render(request, 'events/article.html', context)

def index_event(request):
    categories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    ages = Age.objects.filter(is_publish=True)
    new_events = Event.objects.filter(is_publish=True, is_show=True, type_event=1, start_event__gte=datetime.now()).order_by('-created_at')[:3]
    areas = Area.objects.filter(is_publish=True)
    context = {'categories': categories, 'areas': areas, 'ages': ages, 'new_events': new_events}

    if request.GET.get('search'):
        events = Event.objects.filter(
            Q(title__icontains=request.GET.get('search')) | Q(description__icontains=request.GET.get('search'))).filter(
            is_publish=True, is_show=True, type_event=1, start_event__gte=datetime.now()).order_by('created_at')
    else:
        events = Event.objects.filter(is_publish=True, is_show=True, type_event=1, start_event__gte=datetime.now()).order_by('created_at')

        if request.GET.get('subsubcategories') and request.GET.get('subsubcategories') != '0':
            category = Category.objects.filter(alias=request.GET.get('subcategories')).first()
            subsubcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                       parent_id=category.id).order_by('category')
            category = Category.objects.filter(alias=request.GET.get('categories')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True,
                                                    parent_id=category.id).order_by('category')
            context.update({'subsubcategories': subsubcategories, 'subcategories': subcategories})

            events = events.filter(category__alias=request.GET.get('subsubcategories'))

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

            events = events.filter(eval(str_query))

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

            events = events.filter(eval(str_query))

        if request.GET.get('ages') and request.GET.get('ages') != '0':
            events = events.filter(age_id=request.GET.get('ages'))

        print(datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d'))
        print(datetime.strptime(request.GET.get('start_event'), '%Y-%m-%d'))
        now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
        if request.GET.get('start_event') and datetime.strptime(request.GET.get('start_event'), '%Y-%m-%d') >= now:
            print('yes')
            events = events.filter(start_event__year=request.GET.get('start_event').split('-')[0],
                                   start_event__month=request.GET.get('start_event').split('-')[1],
                                   start_event__day=request.GET.get('start_event').split('-')[2])
        else:
            print('no')

        if request.GET.get('districts') and request.GET.get('districts') != '0':
            districts = District.objects.filter(is_publish=True, city_id=request.GET.get('cities'))
            cities = City.objects.filter(is_publish=True, area_id=request.GET.get('areas'))
            context.update({'districts': districts, 'cities': cities})

            events = events.filter(venue__street__district_id=request.GET.get('districts'))

        elif request.GET.get('cities') and request.GET.get('cities') != '0':
            districts = District.objects.filter(is_publish=True, city_id=request.GET.get('cities'))
            cities = City.objects.filter(is_publish=True, area_id=request.GET.get('areas'))
            context.update({'districts': districts, 'cities': cities})

            str_query = "Q(venue__street__district__city_id='" + request.GET.get('cities') + "')"
            for item in districts:
                str_query += " | Q(venue__street__district_id='" + str(item.id) + "')"

            events = events.filter(eval(str_query))

        elif request.GET.get('areas') and request.GET.get('areas') != '0':
            cities = City.objects.filter(is_publish=True, area_id=request.GET.get('areas'))
            context.update({'cities': cities})

            str_query = "Q(venue__street__district__city__area_id='" + request.GET.get('areas') + "')"
            for item in cities:
                str_query += " | Q(venue__street__district__city_id='" + str(item.id) + "')"
                districts = District.objects.filter(is_publish=True, city_id=item.id)
                for itemD in districts:
                    str_query += " | Q(venue__street__district_id='" + str(itemD.id) + "')"

            events = events.filter(eval(str_query))

        if request.GET.get('free'):
            events = events.filter(price__icontains="Бесплатно")

    events = events.distinct()

    paginator = Paginator(events, 5)

    if request.GET.get('page'):
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)
    list_page = list(paginator.get_elided_page_range(page_number, on_each_side=1))

    context.update({'events': page_obj, 'paginationList': list_page})
    return render(request, 'events/event.html', context)

def show_event(request, alias=""):
    try:
        article = Event.objects.get(type_event=1, alias=alias)
        if not (request.user.is_staff or request.user == article.user):
            article = Event.objects.get(is_publish=True, is_show=True, type_event=1, alias=alias, start_event__gt=datetime.now())
    except Event.DoesNotExist:
        raise Http404("Объявление не найдено")
    categories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=0).order_by('category')
    ages = Age.objects.filter(is_publish=True)
    new_events = Event.objects.filter(is_publish=True, is_show=True, type_event=1).order_by('-created_at')[:3]
    areas = Area.objects.filter(is_publish=True)

    soc_values = article.value.get('social_links')
    values = article.value.get('venues')

    form = CommentForm()

    context = {'form': form, 'article': article, 'categories': categories, 'areas': areas, 'ages': ages, 'new_events': new_events, "soc_values": soc_values, "values": values}

    return render(request, 'events/event-note.html', context)

def loadData(request):
    if request.POST:
        if 'category' in request.POST.get('type'):
            category = Category.objects.filter(access=0, is_publish=True, is_show=True, alias=request.POST.get('alias')).first()
            subcategories = Category.objects.filter(access=0, is_publish=True, is_show=True, parent_id=category.id).order_by('category')
            res = serializers.serialize('json', subcategories)
        elif 'areas' in request.POST.get('type'):
            cities = City.objects.filter(is_publish=True, area_id=request.POST.get('id'))
            type_cities = TypeCity.objects.all()
            cities_json = serializers.serialize('json', cities)
            type_cities_json = serializers.serialize('json', type_cities)
            res = '{ "cities":' + cities_json + ', "type":' + type_cities_json + '}'
        elif 'cities' in request.POST.get('type'):
            districts = District.objects.filter(is_publish=True, city_id=request.POST.get('id'))
            res = serializers.serialize('json', districts)
        else:
            res = "Error"

    return HttpResponse(res, content_type='application/json')

@permission_classes([IsAuthenticated])
def addComment(request):
    try:
        article = Event.objects.get(is_publish=True, is_show=True, alias=request.POST.get('alias'))
    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse('events:index'))

    minskTz = pytz.timezone("Europe/Minsk")

    if request.user.date_muted:
        if request.user.date_muted > datetime.now(minskTz):
            return HttpResponseRedirect(reverse('events:index'))

    parent_id = request.POST.get('parent-id')

    if parent_id != '0':
        try:
            comment = Comment.objects.get(id=parent_id)
            if comment.parent_id != 0:
                parent_id = comment.parent_id
        except Comment.DoesNotExist:
            return HttpResponseRedirect(reverse('events:index'))

    form = CommentForm(data=request.POST)
    if form.is_valid():
        Comment.objects.create(user=request.user, event=article, parent_id=parent_id, comment=form.data['comment'])

    if article.type_event.id == 2:
        return HttpResponseRedirect(reverse('events:show', kwargs={'alias': request.POST.get('alias')}))
    elif article.type_event.id == 1:
        return HttpResponseRedirect(reverse('events:show_event', kwargs={'alias': request.POST.get('alias')}))
    else:
        return HttpResponseRedirect(reverse('events:index'))

@permission_classes([IsAuthenticated])
def deleteComment(request, id=0):
    try:
        article = Event.objects.get(is_publish=True, is_show=True, alias=request.POST.get('alias'))
    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse('events:index'))

    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse('events:index'))

    if not (comment.user == request.user or request.user.has_perm('events.delete_comment')):
        return HttpResponseRedirect(reverse('events:index'))

    comment.delete()

    if article.type_event.id == 2:
        return HttpResponseRedirect(reverse('events:show', kwargs={'alias': request.POST.get('alias')}))
    elif article.type_event.id == 1:
        return HttpResponseRedirect(reverse('events:show_event', kwargs={'alias': request.POST.get('alias')}))
    else:
        return HttpResponseRedirect(reverse('events:index'))

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def editComment(request, id=0):
    try:
        article = Event.objects.get(is_publish=True, is_show=True, alias=request.POST.get('alias'))
    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse('events:index'))

    minskTz = pytz.timezone("Europe/Minsk")

    if request.user.date_muted:
        if request.user.date_muted > datetime.now(minskTz):
            return HttpResponseRedirect(reverse('events:index'))

    try:
        comment = Comment.objects.get(id=id)
    except Comment.DoesNotExist:
        return HttpResponseRedirect(reverse('events:index'))

    if not (comment.user == request.user or request.user.has_perm('events.change_comment')):
        return HttpResponseRedirect(reverse('events:index'))

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment.comment = form.data['comment']
        comment.is_publish = False
        comment.save()
    else:
        return HttpResponseRedirect(reverse('events:index'))

    if article.type_event.id == 2:
        return HttpResponseRedirect(reverse('events:show', kwargs={'alias': request.POST.get('alias')}))
    elif article.type_event.id == 1:
        return HttpResponseRedirect(reverse('events:show_event', kwargs={'alias': request.POST.get('alias')}))
    else:
        return HttpResponseRedirect(reverse('events:index'))

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def addEvent(request, type=''):
    if type == 'event':
        if request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                while True:
                    alias = get_random_string(length=32)
                    event = Event.objects.filter(alias=alias)
                    if not event:
                        break
                if request.POST.get('free') == 'yes':
                    price = 'Бесплатно'
                else:
                    price = request.POST.get('price')

                list_soc = []
                for ind, item in enumerate(request.POST.getlist('socials_val')):
                    if item:
                        list_soc.append({request.POST.getlist('socials_type')[ind]: item})
                value = {"social_links": list_soc, "venues": json.loads(request.POST.get('hidden-block'))}

                if request.POST.get('event_venues'):
                    venue = Venue.objects.filter(id=request.POST.get('event_venues')).first()
                elif request.POST.get('venues'):
                    street = Street.objects.filter(id=request.POST.get('venues')).first()
                    if street:
                        venue = Venue.objects.filter(street=street, house=request.POST.get('house'),
                                                     office=request.POST.get('office')).first()
                        if not venue:
                            venue = Venue.objects.create(street_id=street.id, house=request.POST.get('house'),
                                                         office=request.POST.get('office'),
                                                         description=request.POST.get('description'))

                is_show = True if request.POST.get('is_show') == "on" else False

                minskTz = pytz.timezone("Europe/Minsk")
                start_event_datetime = datetime.strptime(request.POST.get('start_event'), '%Y-%m-%d')
                start_event = minskTz.normalize(start_event_datetime.astimezone(minskTz))

                if price and venue:
                    event = Event.objects.create(age_id=form.data['age'], user=request.user, type_event_id=1,
                                                 value=value, price=price, title=form.data['title'],
                                                 description=form.data['description'],
                                                 meta_title=form.data['meta_title'],
                                                 meta_keywords=form.data['meta_keywords'],
                                                 meta_description=form.data['meta_description'],
                                                 main_photo=request.FILES.get('main_photo'),
                                                 contacts=form.data['contacts'], alias=alias, is_show=is_show, start_event=start_event)
                    event.venue.add(venue)

                    for category_id in request.POST.getlist('categories'):
                        category = Category.objects.filter(id=category_id).first()
                        if category:
                            event.category.add(category)
                    for item in request.FILES.getlist('photos'):
                        photo = Photo.objects.create(path=item)
                        if photo:
                            event.photo.add(photo)

                    messages.success(request, 'Мероприятие создано и отправлено на модерацию')
                    return HttpResponseRedirect(reverse('account:index'))
        else:
            form = EventForm()
        venue = Venue.objects.all()
        street = Street.objects.all()
        context = {'form': form, 'venue': venue, 'street': street}
        return render(request, 'events/edit-event.html', context)
    elif type == 'article':
        if request.POST:
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                while True:
                    alias = get_random_string(length=32)
                    event = Event.objects.filter(alias=alias)
                    if not event:
                        break
                if request.POST.get('free') == 'yes':
                    price = 'Бесплатно'
                else:
                    price = request.POST.get('price')

                list_soc = []
                for ind, item in enumerate(request.POST.getlist('socials_val')):
                    if item:
                        list_soc.append({request.POST.getlist('socials_type')[ind]: item})
                value = {"social_links": list_soc}

                venues = []
                for ven_id in list(dict.fromkeys(request.POST.getlist('event_venues'))):
                    venues.append(Venue.objects.filter(id=ven_id).first())
                for id, ven_id in enumerate(request.POST.getlist('venues')):
                    street = Street.objects.filter(id=ven_id).first()
                    if street:
                        venue = Venue.objects.filter(street=street, house=request.POST.getlist('houses')[id], office=request.POST.getlist('offices')[id]).first()
                        if not venue:
                            ven = Venue.objects.filter(street_id=street.id, house=request.POST.getlist('houses')[id],
                                                 office=request.POST.getlist('offices')[id]).first()
                            if not ven:
                                ven = Venue.objects.create(street_id=street.id, house=request.POST.getlist('houses')[id],
                                                 office=request.POST.getlist('offices')[id],
                                                 description=request.POST.getlist('venue_descriptions')[id])
                            venues.append(ven)

                is_show = True if request.POST.get('is_show') == "on" else False

                if price and len(venues) > 0:
                    event = Event.objects.create(age_id=form.data['age'], user=request.user, type_event_id=2,
                                                 value=value, price=price, title=form.data['title'],
                                                 description=form.data['description'],
                                                 meta_title=form.data['meta_title'],
                                                 meta_keywords=form.data['meta_keywords'],
                                                 meta_description=form.data['meta_description'],
                                                 main_photo=request.FILES.get('main_photo'),
                                                 contacts=form.data['contacts'], alias=alias, is_show=is_show)
                    for ven in venues:
                        event.venue.add(ven)
                    for category_id in request.POST.getlist('categories'):
                        category = Category.objects.filter(id=category_id).first()
                        if category:
                            event.category.add(category)
                    for item in request.FILES.getlist('photos'):
                        photo = Photo.objects.create(path=item)
                        if photo:
                            event.photo.add(photo)

                    messages.success(request, 'Объявление создано и отправлено на модерацию')
                    return HttpResponseRedirect(reverse('account:index'))
        else:
            form = EventForm
        venue = Venue.objects.all()
        street = Street.objects.all()
        context = {'form': form, 'venue': venue, 'street': street}
        return render(request, 'events/edit-article.html', context)
    else:
        return HttpResponseRedirect(reverse('account:index'))

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def editEvent(request, alias=''):
    try:
        article = Event.objects.get(alias=alias, user=request.user)
    except Event.DoesNotExist:
        raise Http404("Объявление не найдено")

    if article.type_event_id == 1:
        if request.POST:
            form = EventForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                if request.POST.get('free') == 'yes':
                    price = 'Бесплатно'
                else:
                    price = request.POST.get('price')

                list_soc = []
                for ind, item in enumerate(request.POST.getlist('socials_val')):
                    list_soc.append({request.POST.getlist('socials_type')[ind]: item})
                value = {"social_links": list_soc, "venues": json.loads(request.POST.get('hidden-block'))}

                if request.POST.get('event_venues'):
                    venue = Venue.objects.filter(id=request.POST.get('event_venues'))
                elif request.POST.get('venues'):
                    street = Street.objects.filter(id=request.POST.get('venues')).first()
                    if street:
                        venue = Venue.objects.filter(street=street, house=request.POST.get('house'),
                                                     office=request.POST.get('office')).first()
                        if not venue:
                            venue = Venue.objects.create(street_id=street.id, house=request.POST.get('house'),
                                                         office=request.POST.get('office'),
                                                         description=request.POST.get('description'))

                is_show = True if request.POST.get('is_show') == "on" else False

                minskTz = pytz.timezone("Europe/Minsk")
                start_event_datetime = datetime.strptime(request.POST.get('start_event'), '%Y-%m-%d')
                start_event = minskTz.normalize(start_event_datetime.astimezone(minskTz))

                if price and venue:
                    article.age_id = form.data['age']
                    article.venue = venue
                    article.value = value
                    article.price = price
                    article.title = form.data['title']
                    article.description = form.data['description']
                    article.meta_title = form.data['meta_title']
                    article.meta_keywords = form.data['meta_keywords']
                    article.meta_description = form.data['meta_description']
                    if request.FILES.get('main_photo'):
                        article.main_photo = request.FILES.get('main_photo')
                    article.contacts = form.data['contacts']
                    article.is_show = is_show
                    article.is_publish = False
                    article.start_event = start_event
                    article.save()

                    for category in article.category.all():
                        article.category.remove(category)
                    for category_id in request.POST.getlist('categories'):
                        category = Category.objects.filter(id=category_id).first()
                        if category:
                            article.category.add(category)

                    for item in request.FILES.getlist('photos'):
                        photo = Photo.objects.create(path=item)
                        if photo:
                            article.photo.add(photo)

                    messages.success(request, 'Мероприятие обновлено и отправлено на модерацию')
                    return HttpResponseRedirect(reverse('account:index'))
        else:
            form = EventForm(instance=article, initial={"start_event": datetime.strptime(str(article.start_event), "%Y-%m-%d %H:%M:%S%z").strftime("%Y-%m-%d")})
        venue = Venue.objects.all()
        street = Street.objects.all()
        context = {'article': article, 'venue': venue, 'street': street, 'form': form}
        return render(request, 'events/edit-event.html', context)
    elif article.type_event_id == 2:
        if request.POST:
            form = EventForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                if request.POST.get('free') == 'yes':
                    price = 'Бесплатно'
                else:
                    price = request.POST.get('price')

                list_soc = []
                for ind, item in enumerate(request.POST.getlist('socials_val')):
                    list_soc.append({request.POST.getlist('socials_type')[ind]: item})
                value = {"social_links": list_soc}

                if request.POST.get('event_venues'):
                    venue = Venue.objects.filter(id=request.POST.get('event_venues'))
                elif request.POST.get('venues'):
                    street = Street.objects.filter(id=request.POST.get('venues')).first()
                    if street:
                        venue = Venue.objects.filter(street=street, house=request.POST.get('house'), office=request.POST.get('office')).first()
                        if not venue:
                            venue = Venue.objects.create(street_id=street.id, house=request.POST.get('house'), office=request.POST.get('office'), description=request.POST.get('description'))

                is_show = True if request.POST.get('is_show') == "on" else False

                if price and venue:
                    article.age_id = form.data['age']
                    article.venue = venue
                    article.value = value
                    article.price = price
                    article.title = form.data['title']
                    article.description = form.data['description']
                    article.meta_title = form.data['meta_title']
                    article.meta_keywords = form.data['meta_keywords']
                    article.meta_description = form.data['meta_description']
                    if request.FILES.get('main_photo'):
                        article.main_photo = request.FILES.get('main_photo')
                    article.contacts = form.data['contacts']
                    article.is_show = is_show
                    article.is_publish = False
                    article.save()

                    for category in article.category.all():
                        article.category.remove(category)
                    for category_id in request.POST.getlist('categories'):
                        category = Category.objects.filter(id=category_id).first()
                        if category:
                            article.category.add(category)

                    for item in request.FILES.getlist('photos'):
                        photo = Photo.objects.create(path=item)
                        if photo:
                            article.photo.add(photo)

                    messages.success(request, 'Объявление обновлено и отправлено на модерацию')
                    return HttpResponseRedirect(reverse('account:index'))
        else:
            form = EventForm(instance=article)
        venue = Venue.objects.all()
        street = Street.objects.all()
        context = {'article': article, 'venue': venue, 'street': street, 'form': form}
        return render(request, 'events/edit-article.html', context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deleteEvent(request, alias=''):
    try:
        article = Event.objects.get(alias=alias)
    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse('account:index'))

    if not (article.user == request.user or request.user.has_perm('events.delete_event')):
        return HttpResponseRedirect(reverse('account:index'))

    article.delete()

    messages.success(request, 'Объявление удалено')
    return HttpResponseRedirect(reverse('account:index'))
