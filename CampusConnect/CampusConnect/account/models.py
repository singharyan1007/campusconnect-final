from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	name = models.CharField(max_length=15, default="",blank=True)
	surname = models.CharField(max_length=15, default="", blank=True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	profile_image = models.ImageField(max_length=255, upload_to='account/images/profile', null=True, blank=True, default="")
	image = models.ImageField(upload_to='account/images', blank=True)
	word1 = models.CharField(max_length=20,default="",blank=True)
	word2 = models.CharField(max_length=20,default="",blank=True)
	word3 = models.CharField(max_length=20,default="",blank=True)
	description = models.TextField(max_length=2000, default="", blank=True)
	mjskl= models.CharField(max_length=50,default="", blank=True)
	skills1 = models.CharField(max_length=50,default="", blank=True)
	skills2 = models.CharField(max_length=50,default="", blank=True)
	skills3 = models.CharField(max_length=50,default="", blank=True)
	skills4 = models.CharField(max_length=50,default="", blank=True)
	skills5 = models.CharField(max_length=50,default="", blank=True)
	github = models.URLField(max_length=500, default="", blank=True)
	linkedin = models.URLField(max_length=500,default="", blank=True)
	hide_email = models.BooleanField(default=True)

	USERNAME_FIELD = 'username'

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True