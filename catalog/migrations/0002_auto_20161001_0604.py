# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 06:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='product',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='image_caption',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='thumbnail',
            field=models.ImageField(default='', upload_to='images/products/thumbnails'),
            preserve_default=False,
        ),
        migrations.RemoveField(model_name='product', name='image'),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='', upload_to='images/products/main'),
            preserve_default=False,
        ),
    ]
