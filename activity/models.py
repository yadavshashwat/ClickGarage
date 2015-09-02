from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
from djangotoolbox.fields import DictField, ListField

# Create your models here.

# class Client(models.Model):
#    email = models.EmailField(unique=True, max_length=100)
#    password = models.CharField(max_length=128)

class CGUser(AbstractUser):
    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    car_ids = ListField(models.CharField(max_length=200))
    lastest_car_history = ListField(models.CharField(max_length=200))
    unchecked_cart = ListField(models.CharField(max_length=200))
    address_trnsaction = ListField(models.CharField(max_length=200))
    past_transaction = ListField(models.CharField(max_length=200))

# class CartCheckouts(models.Model):



class CGUserFullCustom(AbstractBaseUser):
    user_email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # user_email = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(max_length=40)
    USERNAME_FIELD = 'user_email'
    # REQUIRED_FIELDS = ['user_email']