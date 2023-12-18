from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from account.forms import UserLoginForm, UserRegistrationForm, ChangePasswordForm
from django.contrib import auth, messages
from events.models import Event, Comment
from account.models import User
from news.models import Comment as CommentNews
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def index(request):
    articles = Event.objects.filter(type_event=2, user=request.user).order_by('-created_at')
    events = Event.objects.filter(type_event=1, user=request.user).order_by('-created_at')
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.set_password(form.data['password1'])
            user.save()
            messages.success(request, 'Вы успешно изменили пароль!')
    else:
        form = ChangePasswordForm()
    context = {'events': events, 'articles': articles, 'form': form}
    return render(request, 'account/account.html', context)

@api_view(['GET', 'POST'])
def register(request):
    if request.user and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('events:index'))

    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid() and request.POST.get('rule', False):
            form.save()
            messages.success(request, 'Вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('account:login'))
        else:
            if not request.POST.get('rule', False):
                form.add_error('isRule', 'Соглашение должно быть принято')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)

@api_view(['GET', 'POST'])
def login(request):
    if request.user and request.user.is_authenticated:
        return HttpResponseRedirect(reverse('events:index'))

    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('events:index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'account/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('events:index'))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirm_page(request):
    articles = Event.objects.filter(type_event=2, is_publish=False).order_by('-created_at')
    events = Event.objects.filter(type_event=1, is_publish=False).order_by('-created_at')
    comments = Comment.objects.filter(is_publish=False)
    comments_news = CommentNews.objects.filter(is_publish=False)

    context = {'events': events, 'articles': articles, 'comments': comments, 'comments_news': comments_news}

    return render(request, 'account/confirm-page.html', context)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def confirm_method(request, alias="", method=""):
    if method == "addComment":
        comment = Comment.objects.get(id=alias)
        comment.is_publish = True
        comment.save()
    elif method == "addCommentN":
        comment = CommentNews.objects.get(id=alias)
        comment.is_publish = True
        comment.save()
    elif method == "addEvent":
        event = Event.objects.get(alias=alias)
        event.is_publish = True
        event.save()
    elif method == "deleteComment":
        Comment.objects.get(id=alias).delete()
    elif method == "deleteCommentN":
        CommentNews.objects.get(id=alias).delete()
    elif method == "deleteEvent":
        Event.objects.get(alias=alias).delete()

    return HttpResponseRedirect(reverse('account:confirm'))