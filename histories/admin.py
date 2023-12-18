from django.contrib import admin
from .models import History

# Register your models here.

@admin.register(History)
class author_admin(admin.ModelAdmin):
    pass