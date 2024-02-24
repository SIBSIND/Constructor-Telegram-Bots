# Generated by Django 5.0.2 on 2024-02-24 03:46

import donation.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст')),
                ('text_en', models.CharField(max_length=255, null=True, verbose_name='Текст')),
                ('text_uk', models.CharField(max_length=255, null=True, verbose_name='Текст')),
                ('text_ru', models.CharField(max_length=255, null=True, verbose_name='Текст')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('position', models.IntegerField(blank=True, default=donation.models.button_position_default, verbose_name='Позиция')),
            ],
            options={
                'verbose_name': 'Кнопку',
                'verbose_name_plural': 'Кнопки',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.FloatField(verbose_name='Сумма')),
                ('contact_link', models.URLField(verbose_name='Контактная ссылка')),
                ('date', models.DateTimeField(verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Пожертвование',
                'verbose_name_plural': 'Пожертвования',
                'db_table': 'donation',
                'ordering': ('-sum',),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('title_uk', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('text_en', models.TextField(null=True, verbose_name='Текст')),
                ('text_uk', models.TextField(null=True, verbose_name='Текст')),
                ('text_ru', models.TextField(null=True, verbose_name='Текст')),
                ('position', models.IntegerField(blank=True, default=donation.models.section_position_default, verbose_name='Позиция')),
            ],
            options={
                'verbose_name': 'Раздел',
                'verbose_name_plural': 'Разделы',
                'ordering': ('position',),
            },
        ),
    ]
