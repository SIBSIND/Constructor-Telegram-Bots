# Generated by Django 5.0 on 2023-12-28 01:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0023_rename_data_telegrambotcommandapirequest_body_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrambot',
            name='diagram_current_scale',
        ),
    ]