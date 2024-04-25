# Generated by Django 5.0.2 on 2024-02-24 11:59

import instruction.models
from django.db import migrations, models


class Migration(migrations.Migration):
	initial = True

	dependencies = []

	operations = [
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
				(
					'position',
					models.PositiveSmallIntegerField(
						blank=True, default=instruction.models.section_position_default, verbose_name='Позиция'
					),
				),
			],
			options={
				'verbose_name': 'Раздел',
				'verbose_name_plural': 'Разделы',
				'ordering': ('position',),
			},
		),
	]
