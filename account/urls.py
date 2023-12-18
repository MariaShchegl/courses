from django.urls import path, include
from . import views

app_name='account'

urlpatterns = [
    path('', views.index, name='index'),
    path('confirm-page/', views.confirm_page, name='confirm'),
    path('confirm-page/<str:alias>/<str:method>', views.confirm_method, name='confirm_method'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]