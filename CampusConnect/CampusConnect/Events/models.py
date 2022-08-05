from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
# Create your models here.

class Events(models.Model):
    name = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to='Events/images',blank = True)
    description = RichTextUploadingField()
    organiser = models.CharField(max_length=50,default="")
    date = models.DateField(default="")
    link = models.URLField(max_length=500,default="", blank=True) 