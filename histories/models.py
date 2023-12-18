from django.db import models
from account.models import User
from events.models import Category, uploads_custom
from datetime import datetime
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class TextFieldImpl(models.TextField):
    '''
        Implements comma-separated storage of lists.

        class for implementing a TextField for working correctly with postgres
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'TEXT'

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()

        return name, path, args, kwargs

class History(models.Model):
    title = models.CharField(max_length=255)
    article = RichTextUploadingField()
    main_photo = models.ImageField(
        upload_to=uploads_custom('main_histories_images/{}/'.format(datetime.now().strftime('%Y-%m'))))
    small_photo = models.ImageField(
        upload_to=uploads_custom('small_histories_images/{}/'.format(datetime.now().strftime('%Y-%m'))))
    alias = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_show = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=255)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    category = models.ManyToManyField(Category, blank=True, related_name='historiesCat')

    class Meta:
        verbose_name_plural = 'Истории'

    def __str__(self):
        return self.title