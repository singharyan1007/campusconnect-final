# Generated by Django 3.2.13 on 2022-08-31 08:16

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('main_image', models.ImageField(blank=True, upload_to='Events/images')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('organiser', models.CharField(default='', max_length=50)),
                ('date', models.DateField(default='')),
                ('link', models.URLField(blank=True, default='', max_length=500)),
            ],
        ),
    ]
