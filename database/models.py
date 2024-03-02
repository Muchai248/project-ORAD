from enum import unique
from os import name
from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=256, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class UserManager(BaseUserManager):

#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('Email for user must be set.')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#     def create_superuser(self,email,password):
#         user = self.create_user(email=email, password=password, is_staff=True,is_superuser=True)
#         user.is_admin = True
#         user.is_active = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user



# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     fullname = models.CharField(max_length=50, null=True, blank=True)
#     email = models.CharField(max_length=57, unique=True)
#     password = models.CharField(max_length=20, null=True)
#     is_active = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = 'email'
#     objects = UserManager()
    



class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="documents/", null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Site(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class QCDocument(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    document = models.FileField(upload_to="documents/")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document.name



# class Post(models.Model):
#     uploader = models.ForeignKey(CustomUser, on_delete=models.PROTECT, blank=False, null=True)
#     title = models.CharField(max_length=200)


# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)

#     objects = CustomUser()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_permissions',
#         blank=True,
#     )

#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_groups',
#         blank=True,
#     )

#     def __str__(self):
#         return self.email

# class Engineer(models.Model):
#     user_id = self.model(email)
#     upload_file =

# class Document(models.Model):
#     title = models.CharField(max_length=256)
#     file = models.FileField(upload_to="documents/")
#     uploader = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     uploaded_at = models.DateField(auto_now_add=True)


#     def __str__(self):
#         return self.title
