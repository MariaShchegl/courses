from django.urls import path, include
from . import views

app_name='histories'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:alias>/', views.show, name='show'),
]