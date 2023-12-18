from django.urls import path, include
from . import views

app_name='events'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:alias>/', views.show, name='show'),
    path('events', views.index_event, name='index_event'),
    path('events/<str:alias>/', views.show_event, name='show_event'),
    path('load_data', views.loadData, name='load_data'),
    path('add_comment', views.addComment, name='add_comment'),
    path('edit_comment/<int:id>', views.editComment, name='edit_comment'),
    path('delete_comment/<int:id>', views.deleteComment, name='delete_comment'),
    path('add_event/<str:type>', views.addEvent, name='add_event'),
    path('edit_event/<str:alias>', views.editEvent, name='edit_event'),
    path('delete_event/<str:alias>', views.deleteEvent, name='delete_event'),
]