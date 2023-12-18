from django import forms
from django.forms import widgets

from .models import Comment, Event, Category, Age

class CustomDateInput(forms.DateInput):
    input_type = "date"

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea)
    comment.label = 'Сообщение'

    comment.widget.attrs.update({'class': 'form-control', 'placeholder':'Ваш комментарий*'})
    comment.widget.attrs.update(rows=8)

    class Meta:
        model = Comment
        fields = ['comment']

class EventForm(forms.ModelForm):
    title = forms.CharField(max_length=255)
    title.label = "Название"
    title.widget.attrs.update({'class': 'form-control', 'placeholder': 'Название объявления*'})

    description = forms.CharField(widget=forms.Textarea)
    description.label = "Описание объявления*"
    description.widget.attrs.update({'class': 'form-control', 'placeholder': 'Описание объявления*'})
    description.widget.attrs.update(rows=5)

    main_photo = forms.ImageField()
    main_photo.label = "Изображение карточки объявения"
    main_photo.widget.attrs.update({'class': 'form-control', 'placeholder': 'Изображение карточки объявения'})

    contacts = forms.CharField(max_length=255, widget=forms.Textarea)
    contacts.label = "Контакты* (+375 29 123-45-67, www.example.com)"
    contacts.widget.attrs.update({'class': 'form-control', 'placeholder': 'Контакты* (+375 29 123-45-67, www.example.com)'})
    contacts.widget.attrs.update(rows=5)

    meta_title = forms.CharField(max_length=255)
    meta_title.label = "Мета заголовок"
    meta_title.widget.attrs.update({'class': 'form-control', 'placeholder': 'Мета заголовок'})

    meta_keywords = forms.CharField(max_length=255)
    meta_keywords.label = "Мета ключевые слова"
    meta_keywords.widget.attrs.update({'class': 'form-control', 'placeholder': 'Мета ключевые слова (до 255 символов)'})

    meta_description = forms.CharField(widget=forms.Textarea)
    meta_description.label = "Мета описание"
    meta_description.widget.attrs.update({'class': 'form-control', 'placeholder': 'Мета описание'})
    meta_description.widget.attrs.update(rows=5)

    age = forms.ModelChoiceField(queryset=Age.objects.filter(is_publish=True))
    age.label = "Возраст"
    age.widget.attrs.update({'class': 'selectpicker', 'data-live-search': "true"})

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.filter(access=0, is_publish=True, is_show=True).order_by('category'))
    categories.label = "Категории"
    categories.widget.attrs.update({'class': 'selectpicker mb-2', 'data-live-search': "true", 'size': 5})

    is_show = forms.BooleanField(required=False)

    start_event = forms.DateField(required=False, widget=CustomDateInput)
    start_event.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Event
        fields = ['title', 'description', 'main_photo', 'contacts', 'meta_title', 'meta_description', 'meta_keywords', 'age', 'is_show', 'start_event']