from django.db import models
from datetime import datetime
from account.models import User
import hashlib
import os


# Create your models here.

def uploads_custom(path):
    def wrapper(instance, filename):
        now = datetime.now()
        name, ext = os.path.splitext(filename)
        filename = now.strftime("%m%d%Y%H%M%S") + hashlib.md5(name.encode()).hexdigest() + ext
        return os.path.join(path, filename)

    return wrapper


class Photo(models.Model):
    path = models.ImageField(upload_to=uploads_custom('events_images/{}/'.format(datetime.now().strftime('%Y-%m'))))
    is_show = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Фото'


class Category(models.Model):
    category = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, unique=True)
    parent_id = models.BigIntegerField(default=0)
    is_show = models.BooleanField(default=True)
    is_publish = models.BooleanField(default=False)
    access = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category


class TypeEvent(models.Model):
    type = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = 'Тип мероприятия'

    def __str__(self):
        return self.type


class Area(models.Model):
    area = models.CharField(max_length=50)
    is_publish = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Область'

    def __str__(self):
        return self.area


class TypeCity(models.Model):
    type = models.CharField(max_length=30)
    abbreviation = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Тип населенного пункта'

    def __str__(self):
        return self.type


class City(models.Model):
    city = models.CharField(max_length=50)
    is_publish = models.BooleanField(default=False)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    type_city = models.ForeignKey(TypeCity, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Населенный пункт'

    def __str__(self):
        return self.city


class District(models.Model):
    district = models.CharField(max_length=50)
    is_publish = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Район'

    def __str__(self):
        return self.district


class Street(models.Model):
    street = models.CharField(max_length=50)
    is_publish = models.BooleanField(default=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Улица'

    def __str__(self):
        return self.street


class Age(models.Model):
    age = models.CharField(max_length=10)
    is_publish = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Возраст'

    def __str__(self):
        return self.age


class Venue(models.Model):
    title = models.CharField(max_length=30, blank=True)
    house = models.CharField(max_length=10)
    office = models.CharField(max_length=10, blank=True)
    description = models.CharField(max_length=255, blank=True)
    is_reserve = models.BooleanField(default=False)
    street = models.ForeignKey(Street, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Место проведения'


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    main_photo = models.ImageField(
        upload_to=uploads_custom('main_events_images/{}/'.format(datetime.now().strftime('%Y-%m'))))
    contacts = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, unique=True)
    is_publish = models.BooleanField(default=False)
    is_show = models.BooleanField(default=True)
    value = models.JSONField()
    price = models.CharField(max_length=20)
    meta_title = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()
    type_event = models.ForeignKey(TypeEvent, on_delete=models.PROTECT)
    age = models.ForeignKey(Age, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    start_event = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True)
    photo = models.ManyToManyField(Photo, blank=True)
    venue = models.ManyToManyField(Venue, blank=True)

    class Meta:
        verbose_name_plural = 'Мероприятие'

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    parent_id = models.BigIntegerField(default=0)
    is_publish = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comment_event_user')
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='comment_event')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Комментарии мероприятий'

    def __str__(self):
        return self.event.title + "|" + self.user.username
