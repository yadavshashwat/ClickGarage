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
    # unchecked_cart = ListField(models.DictField)
    uc_cart = DictField()
    saved_address = ListField(DictField())
    address_trnsaction = ListField(models.CharField(max_length=200))
    past_transaction = ListField(models.CharField(max_length=200))
    transactions_temp = ListField(DictField())

# class CartCheckouts(models.Model):

class Transaction(models.Model):
    booking_id         = models.IntegerField()
    trans_timestamp    = models.CharField(max_length=200)
    cust_name          = models.CharField(max_length=200)
    cust_brand         = models.CharField(max_length=200)
    cust_carname       = models.CharField(max_length=200)
    cust_number        = models.CharField(max_length=200)
    cust_email         = models.CharField(max_length=200)
    cust_pickup_add    = models.CharField(max_length=200)
    cust_drop_add      = models.CharField(max_length=200)
    booking_vendor     = models.CharField(max_length=200)
    booking_cat        = models.CharField(max_length=200)
    booking_type       = models.CharField(max_length=200)
    price_labour       = models.CharField(max_length=200)
    price_parts        = models.CharField(max_length=200)
    price_total        = models.CharField(max_length=200)
    date_booking       = models.CharField(max_length=200)
    time_booking       = models.CharField(max_length=200)
    amount_paid        = models.BooleanField()
    status             = models.CharField(max_length=200)
    comments           = models.CharField(max_length=300)


class Transactions(models.Model):
    booking_id         = models.IntegerField()
    trans_timestamp    = models.CharField(max_length=200)
    cust_id            = models.CharField(max_length=200)
    cust_name          = models.CharField(max_length=200)
    cust_brand         = models.CharField(max_length=200)
    cust_carname       = models.CharField(max_length=200)
    cust_carnumber     = models.CharField(max_length=200)
    cust_number        = models.CharField(max_length=200)
    cust_email         = models.CharField(max_length=200)
    cust_pickup_add    = DictField()
    cust_drop_add      = DictField()
    service_items      = ListField( DictField() )
    price_total        = models.CharField(max_length=200)
    date_booking       = models.CharField(max_length=200)
    time_booking       = models.CharField(max_length=200)
    amount_paid        = models.BooleanField()
    status             = models.CharField(max_length=200)
    comments           = models.CharField(max_length=300)


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