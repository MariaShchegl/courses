from django.contrib import admin
from .models import Category, Photo, TypeEvent, Area, TypeCity, City, District, Street, Age, Venue, Event, Comment

# Register your models here.

@admin.register(Category, Photo, TypeEvent, Area, TypeCity, City, District, Street, Age, Venue, Event, Comment)
class author_admin(admin.ModelAdmin):
    pass