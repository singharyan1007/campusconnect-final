from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image
# Create your models here.

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default=0)
    subcategory = models.CharField(max_length=50, default=0)
    size = models.JSONField(max_length=7)
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    images = models.ImageField(upload_to="shop/images", default="")
    backimages = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        return self.product_name

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    Hostel_name = models.CharField(max_length=500)
    Unit = models.CharField(max_length=4)
    City = models.CharField(max_length=15)
    pincode = models.IntegerField()
    landmark = models.CharField(max_length=50)

    def __str__(self):
        return self.Hostel_name


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.CharField(max_length=500, default='none')
    size = models.CharField(max_length=10, default='S')
    qty = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return self.items