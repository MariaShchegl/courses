from django.contrib import admin
from .models import News, Comment

# Register your models here.

@admin.register(News, Comment)
class author_admin(admin.ModelAdmin):
    pass