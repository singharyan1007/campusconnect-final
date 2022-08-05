from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
# Create your models here.

class projects(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    main_image = models.ImageField(upload_to='Project/images',blank = True)
    description = RichTextUploadingField()
    github = models.URLField(max_length=500, default="", blank=True)
    deployed_link = models.URLField(max_length=500, default="", blank=True)