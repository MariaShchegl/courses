# Generated by Django 4.0.4 on 2022-12-19 23:01

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('article', ckeditor_uploader.fields.RichTextUploadingField()),
                ('main_photo', models.ImageField(upload_to='main_news_images')),
                ('alias', models.CharField(max_length=255, unique=True)),
                ('is_show', models.BooleanField(default=True)),
                ('is_comment', models.BooleanField(default=True)),
                ('meta_title', models.CharField(max_length=255)),
                ('meta_keywords', models.CharField(max_length=255)),
                ('meta_description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True)),
                ('category', models.ManyToManyField(blank=True, related_name='news', to='events.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('parent_id', models.BigIntegerField(default=0)),
                ('is_publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='news.news')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_news', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
