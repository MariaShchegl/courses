# Generated by Django 4.0.4 on 2022-12-19 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_is_distribution_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_blocked',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='date_muted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]