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
    car_bike = models.CharField(max_length=50)
    cleaning_cat = models.CharField(max_length=50)

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
    WA_WB_Inc           = models.CharField(max_length=50)
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

###########################   New Servicing models ############################

class ServicingNew(models.Model):
    name                = models.CharField(max_length=200)
    #while uploading servicing list file
    brand               = models.CharField(max_length=50)
    carname             = models.CharField(max_length=50)
    type_service        = models.CharField(max_length=200)
    service_desc        = models.CharField(max_length=500)
        #year                = models.CharField(max_length=50)
    regular_checks      = ListField(models.CharField(max_length=200))
    #while uploading servicing labour
    #paid_free           = models.CharField(max_length=50)
    part_replacement    = ListField(models.CharField(max_length=200))
    part_dic = ListField(DictField())
    dealer       = ListField(models.CharField(max_length=200))
    priority_service           = models.CharField(max_length=50)

class ServiceDealerCatNew(models.Model):
    name                = models.CharField(max_length=200)
    brand               = models.CharField(max_length=50)
    carname             = models.CharField(max_length=50)
    type_service        = models.CharField(max_length=200)
    service_desc        = models.CharField(max_length=500)

    #year               = models.CharField(max_length=50)
    dealer_category     = models.CharField(max_length=200)
    part_dic = ListField(DictField())
    part_replacement    = ListField(models.CharField(max_length=200))
   # while uploading part frequency
    price_parts         = models.CharField(max_length=50)
    price_labour        = models.CharField(max_length=50)
    wheel_alignment     = models.CharField(max_length=50)
    wheel_balancing     = models.CharField(max_length=50)
    # WA_WB_Inc           = models.CharField(max_length=50)
    detail_dealers      = ListField(DictField())
    #paid_free          = models.CharField(max_length=50)
    regular_checks      = ListField(models.CharField(max_length=200))
    discount            = models.CharField(max_length=50)
    priority            = models.CharField(max_length=50)
    priority_service           = models.CharField(max_length=50)
    car_bike = models.CharField(max_length=50)
    # vas_dic = ListField(DictField())
    dry_cleaning        = models.CharField(max_length=50)
    engine_additive     = models.CharField(max_length=50)
    injector_cleaning   = models.CharField(max_length=50)
    rubbing_polishing   = models.CharField(max_length=50)
    anti_rust           = models.CharField(max_length=50)
    teflon              = models.CharField(max_length=50)
    engine_flush        = models.CharField(max_length=50)
    ac_servicing        = models.CharField(max_length=50)
    ac_disinfection     = models.CharField(max_length=50)



class ServiceDealerNameNew(models.Model):
    name            = models.CharField(max_length=200)
    make            = models.CharField(max_length=200)
    dealer_category = models.CharField(max_length=200)
    address         = models.CharField(max_length=200)
    timing          = models.CharField(max_length=200)
    day_opening     = models.CharField(max_length=200)
    website         = models.CharField(max_length=200)
    email           = models.CharField(max_length=200)
    telephone       = models.CharField(max_length=200)
    mobile          = models.CharField(max_length=200)
    latitude        = models.CharField(max_length=200)
    longitude       = models.CharField(max_length=200)
    region          = models.CharField(max_length=200)
    rating          = models.CharField(max_length=50)
    reviews         = ListField(models.CharField(max_length=500))

##########################################################################################

class CleaningDealerName(models.Model):
    vendor  = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class CleaningCatName(models.Model):
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    car_bike = models.CharField(max_length=50)

class CleaningServiceCat(models.Model):
    vendor = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    car_bike = models.CharField(max_length=50)

class CleaningCategoryServices(models.Model):
    vendor          = models.CharField(max_length=50)
    category        = models.CharField(max_length=50)
    car_cat         = models.CharField(max_length=50)
    service         = models.CharField(max_length=200)
    price_labour    = models.CharField(max_length=50)
    price_parts     = models.CharField(max_length=50)
    price_total     = models.CharField(max_length=50)
    description     = models.CharField(max_length=1000)
    discount        = models.CharField(max_length=50)
    doorstep        = models.CharField(max_length=50)
    car_bike = models.CharField(max_length=50)
    priority        = models.CharField(max_length=50)
    rating          = ListField(models.CharField(max_length=50))
    reviews         = ListField(models.CharField(max_length=500))


class VASDealerName(models.Model):
    vendor  = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class VASCatName(models.Model):
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    car_bike = models.CharField(max_length=50)

class VASServiceCat(models.Model):
    vendor = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    car_bike = models.CharField(max_length=50)


class VASCategoryServices(models.Model):
    vendor          = models.CharField(max_length=50)
    category        = models.CharField(max_length=50)
    car_cat         = models.CharField(max_length=50)
    service         = models.CharField(max_length=200)
    price_labour    = models.CharField(max_length=50)
    price_parts     = models.CharField(max_length=50)
    price_total     = models.CharField(max_length=50)
    description     = models.CharField(max_length=500)
    doorstep        = models.CharField(max_length=50)
    discount        = models.CharField(max_length=50)
    priority        = models.CharField(max_length=50)
    rating          = ListField(models.CharField(max_length=50))
    reviews         = ListField(models.CharField(max_length=500))
    car_bike = models.CharField(max_length=50)

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
    colour          = models.CharField(max_length=50)
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
    booking_id      = models.IntegerField()
    trans_timestamp = models.IntegerField()
    cust_id         = models.CharField(max_length=200)
    cust_name       = models.CharField(max_length=200)
    cust_brand      = models.CharField(max_length=200)
    cust_carname    = models.CharField(max_length=200)
    cust_number     = models.CharField(max_length=200)
    cust_email      = models.CharField(max_length=200)
    cust_pickup_add = models.CharField(max_length=200)
    cust_drop_add   = models.CharField(max_length=200)
    booking_vendor  = models.CharField(max_length=200)
    booking_cat     = models.CharField(max_length=200)
    booking_type    = models.CharField(max_length=200)
    price_labour    = models.CharField(max_length=200)
    price_parts     = models.CharField(max_length=200)
    price_total     = models.CharField(max_length=200)
    date_booking    = models.IntegerField()
    time_booking    = models.IntegerField()
    amount_paid     = models.CharField(max_length=200)
    status          = models.CharField(max_length=200)
    comments        = models.CharField(max_length=200)

class Coupon(models.Model):
    coupon_code     = models.CharField(max_length=50)
    date_issue      = models.CharField(max_length=50)
    valid_till_date = models.CharField(max_length=50)
    discount        = models.CharField(max_length=50)
    cashback        = models.CharField(max_length=50)
    message         = models.CharField(max_length=500)
    valid           = models.CharField(max_length=50)
    category        = models.CharField(max_length=50)
    car_bike        = models.CharField(max_length=50)
    vendor          = models.CharField(max_length=50)


class Otp(models.Model):
    mobile = models.CharField(max_length=50)
    otp = models.CharField(max_length=50)
    created      =   models.DateTimeField(default=None)
    updated      =   models.DateTimeField(default=None)
    username     = models.CharField(max_length=50)

