from django.db import models

# Create your models here.

class Almuni(models.Model):
    name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    designation = models.CharField(max_length=60)
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=4,default = "")
    USN = models.CharField(max_length=10,default="")
    contact = models.CharField(max_length=10,default="0000000000")
    main_image = models.ImageField(upload_to='Almuni/images',blank = True)
    instagram = models.URLField(max_length=1000, default="", blank=True)
    linkedin = models.URLField(max_length=1000, default="", blank=True)
    mail = models.URLField(max_length=500, default="", blank=True)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return self.name

