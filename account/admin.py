from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class author_admin(admin.ModelAdmin):
    pass