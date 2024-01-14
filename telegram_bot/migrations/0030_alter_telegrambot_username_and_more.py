# Generated by Django 5.0 on 2024-01-14 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0029_telegrambotvariable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambot',
            name='username',
            field=models.CharField(max_length=32, verbose_name='@username'),
        ),
        migrations.AlterField(
            model_name='telegrambotcommand',
            name='name',
            field=models.CharField(max_length=128, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='telegrambotcommandapirequest',
            name='url',
            field=models.URLField(verbose_name='URL-адрес'),
        ),
        migrations.AlterField(
            model_name='telegrambotcommandcommand',
            name='text',
            field=models.CharField(max_length=255, verbose_name='Команда'),
        ),
        migrations.AlterField(
            model_name='telegrambotcommandkeyboardbutton',
            name='end_diagram_connector',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='telegrambotcommandkeyboardbutton',
            name='start_diagram_connector',
            field=models.TextField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='telegrambotcommandkeyboardbutton',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='URL-адрес'),
        ),
    ]
