from django.db import models
from djangotoolbox.fields import DictField, ListField

#from dbpreferences.fields import DictField
# Create your models here.


#generic models
class Address(models.Model):
    full_address = models.TextField()
    street_address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class Car(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    year = models.IntegerField()
    aspect_ratio = models.CharField(max_length=20)
    size = models.CharField(max_length=50)

#two sets of DBs
#1 - data entry
class Dealer(models.Model):
    name = models.CharField(max_length=200)
    address = DictField()
    pub_date = models.DateTimeField()
    servicing = ListField(DictField())
    tyres = ListField(DictField())
    wheels = ListField(DictField())
    emergency = ListField(DictField())
    misc = ListField(DictField())

#2 - auto populate
class Servicing(models.Model):
    name                = models.CharField(max_length=200)

    #while uploading servicing list file
    brand               = models.CharField(max_length=50)
    carname             = models.CharField(max_length=50)
    odometer            = models.IntegerField()
    year                = models.CharField(max_length=50)
    regular_checks      = ListField(models.CharField(max_length=200))

    #while uploading servicing labour
    paid_free           = models.CharField(max_length=50)
    part_replacement    = ListField(models.CharField(max_length=200))
    dealer              = ListField(models.CharField(max_length=200))
    
class ServiceDealerCat(models.Model):
    name                = models.CharField(max_length=200)
    brand               = models.CharField(max_length=50)
    carname             = models.CharField(max_length=50)
    odometer            = models.IntegerField()
    year                = models.CharField(max_length=50)
    dealer_category     = models.CharField(max_length=200)
    part_replacement    = ListField(models.CharField(max_length=200))
   #while uploading part frequency
    price_parts         = models.CharField(max_length=50)
    price_labour        = models.CharField(max_length=50)
    wheel_alignment     = models.CharField(max_length=50)
    wheel_balancing     = models.CharField(max_length=50)
    WA_WB_Inc           = models.BooleanField()
    detail_dealers      = ListField(DictField())
    paid_free           = models.CharField(max_length=50)
    regular_checks      = ListField(models.CharField(max_length=200))


class ServiceDealerName(models.Model):
    name            = models.CharField(max_length=200)
    make            = models.CharField(max_length=200)
    dealer_category = models.CharField(max_length=200)
    address         = models.CharField(max_length=200)
    phone           = models.CharField(max_length=200)
    timing          = models.CharField(max_length=200)
    rating          = models.CharField(max_length=50)
    reviews         = ListField(models.CharField(max_length=500))

class CleaningDealerName(models.Model):
    vendor  = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class CleaningServiceCat(models.Model):
    vendor = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class CleaningCategoryServices(models.Model):
    vendor          = models.CharField(max_length=50)
    category        = models.CharField(max_length=50)
    car_cat         = models.CharField(max_length=50)
    service         = models.CharField(max_length=200)
    price_labour    = models.CharField(max_length=50)
    price_parts     = models.CharField(max_length=50)
    price_total     = models.CharField(max_length=50)
    description     = models.CharField(max_length=500)
    rating          = ListField(models.CharField(max_length=50))
    reviews         = ListField(models.CharField(max_length=500))


class VASDealerName(models.Model):
    vendor  = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class VASServiceCat(models.Model):
    vendor = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class VASCategoryServices(models.Model):
    vendor          = models.CharField(max_length=50)
    category        = models.CharField(max_length=50)
    car_cat         = models.CharField(max_length=50)
    service         = models.CharField(max_length=200)
    price_labour    = models.CharField(max_length=50)
    price_parts     = models.CharField(max_length=50)
    price_total     = models.CharField(max_length=50)
    description     = models.CharField(max_length=500)
    rating          = ListField(models.CharField(max_length=50))
    reviews         = ListField(models.CharField(max_length=500))

class WindShieldCat(models.Model):
    brand    = models.CharField(max_length=50)
    vendor   = models.CharField(max_length=50)
    carname  = models.CharField(max_length=50)   
    ws_type  = models.CharField(max_length=50)   



class WindShieldServiceDetails(models.Model):
    vendor          = models.CharField(max_length=50)
    brand           = models.CharField(max_length=50)
    carname         = models.CharField(max_length=50)
    ws_type         = models.CharField(max_length=50)
    ws_subtype      = models.CharField(max_length=50)
    price_ws        = models.CharField(max_length=50)
    price_sealant   = models.CharField(max_length=50)
    price_labour    = models.CharField(max_length=50)
    price_insurance = models.CharField(max_length=50)
    price_total     = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    description     = models.CharField(max_length=50)
    rating          = ListField(models.CharField(max_length=50))
    reviews         = ListField(models.CharField(max_length=500))

#Wheel Services 
#List of wheel services 
class WheelServices(models.Model):
    name        = models.CharField(max_length=50)
    service     = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

#List of wheel service providers with price
class WheelServiceProvider(models.Model):
    name    = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone   = models.CharField(max_length=200)
    timing  = models.CharField(max_length=200)
    rating  = models.CharField(max_length=50)
    reviews = ListField(models.CharField(max_length=500))
    service = models.CharField(max_length=50)
    car     = models.CharField(max_length=50)
    price   = models.CharField(max_length=50)


#List of tyre sales
class TyreSale(models.Model):
    name          = models.CharField(max_length=50)
    address       = models.CharField(max_length=50)
    rating_dealer = models.CharField(max_length=50)
    aspect_key    = models.CharField(max_length=50)
    brand         = models.CharField(max_length=50)
    model         = models.CharField(max_length=50)
    width         = models.CharField(max_length=50)
    aspect_ratio  = models.CharField(max_length=50)
    rim_size      = models.CharField(max_length=50)
    load_rating   = models.CharField(max_length=50)
    speed_rating  = models.CharField(max_length=50)
    warranty      = models.CharField(max_length=50)
    rating        = models.CharField(max_length=50)
    reviews       = ListField(models.CharField(max_length=500))
    price         = models.CharField(max_length=50)

#service : [Quick Wash (Exterior),Quick Clean (Interior),Full Wash,Interior Detailing Package,Exterior Detailing Package,Complete Car Detailing]

class Coating(models.Model):
    name = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
#service : [Quick Wash (Exterior),Quick Clean (Interior),Full Wash,Interior Detailing Package,Exterior Detailing Package,Complete Car Detailing]

class MiscServices(models.Model):
    name = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
#service :

class Emergency(models.Model):
    name = models.CharField(max_length=50)
    service = models.CharField(max_length=50)

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



