# Generated by Django 3.2.13 on 2022-08-31 08:16

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('main_image', models.ImageField(blank=True, upload_to='Project/images')),
                ('description', ckeditor_uploader.fields.RichTextUploadingField()),
                ('github', models.URLField(blank=True, default='', max_length=500)),
                ('deployed_link', models.URLField(blank=True, default='', max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
