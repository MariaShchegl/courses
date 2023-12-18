from django.urls import path, include
from . import views

app_name='news'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:alias>/', views.show, name='show'),
    path('add_comment', views.addComment, name='add_comment'),
    path('edit_comment/<int:id>', views.editComment, name='edit_comment'),
    path('delete_comment/<int:id>', views.deleteComment, name='delete_comment'),
]