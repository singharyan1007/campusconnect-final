from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
# Create your models here.

class Clubs(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to='Clubs/images',blank = True)
    instagram = models.URLField(max_length=500, default="", blank=True)
    whatsapp = models.URLField(max_length=500, default="", blank=True)
    description = RichTextUploadingField()