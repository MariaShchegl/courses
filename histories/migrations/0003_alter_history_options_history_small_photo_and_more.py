# Generated by Django 4.0.4 on 2023-12-14 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_age_options_alter_area_options_and_more'),
        ('histories', '0002_alter_history_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={'verbose_name_plural': 'Истории'},
        ),
        migrations.AddField(
            model_name='history',
            name='small_photo',
            field=models.ImageField(default='def.png', upload_to='small_histories_images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='history',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='historiesCat', to='events.category'),
        ),
        migrations.AlterField(
            model_name='history',
            name='main_photo',
            field=models.ImageField(upload_to='main_histories_images/'),
        ),
    ]