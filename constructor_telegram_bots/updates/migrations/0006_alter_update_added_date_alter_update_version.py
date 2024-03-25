# Generated by Django 4.2.3 on 2023-09-03 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('updates', '0005_alter_update_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Добавлено'),
        ),
        migrations.AlterField(
            model_name='update',
            name='version',
            field=models.CharField(max_length=255, verbose_name='Версия'),
        ),
    ]