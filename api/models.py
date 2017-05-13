from django.db import models
from djangotoolbox.fields import DictField, ListField
import datetime
#from dbpreferences.fields import DictField
# Create your models here.


# generic models
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
    complete_vehicle_name = models.CharField(max_length=200)

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

# class Transaction(models.Model):
#     booking_id      = models.IntegerField()
#     trans_timestamp = models.IntegerField()
#     cust_id         = models.CharField(max_length=200)
#     cust_name       = models.CharField(max_length=200)
#     cust_brand      = models.CharField(max_length=200)
#     cust_carname    = models.CharField(max_length=200)
#     cust_number     = models.CharField(max_length=200)
#     cust_email      = models.CharField(max_length=200)
#     cust_pickup_add = models.CharField(max_length=200)
#     cust_drop_add   = models.CharField(max_length=200)
#     booking_vendor  = models.CharField(max_length=200)
#     booking_cat     = models.CharField(max_length=200)
#     booking_type    = models.CharField(max_length=200)
#     price_labour    = models.CharField(max_length=200)
#     price_parts     = models.CharField(max_length=200)
#     price_total     = models.CharField(max_length=200)
#     date_booking    = models.IntegerField()
#     time_booking    = models.IntegerField()
#     amount_paid     = models.CharField(max_length=200)
#     status          = models.CharField(max_length=200)
#     comments        = models.CharField(max_length=200)

class Coupon(models.Model):
    date_issue      = models.CharField(max_length=50, null=True)
    valid_till_date = models.CharField(max_length=50, null=True)
    discount        = models.CharField(max_length=50, null=True)
    cashback        = models.CharField(max_length=50, null=True)
    valid           = models.CharField(max_length=50, null=True)
    #new values
    message         = models.CharField(max_length=500)
    date_init       = models.DateField(default=datetime.date(2016,1,1))
    date_expiry     = models.DateField(default=datetime.date(2016,1,1))
    coupon_code     = models.CharField(max_length=50)
    category        = models.CharField(max_length=50)
    value    = models.FloatField(default=0)
    cap      = models.FloatField(null=True)
    type      = models.CharField(default='discount', max_length=10)
    price_key      = models.CharField(max_length=50, null = True)
    vendor          = models.CharField(max_length=50)
    car_bike        = models.CharField(max_length=50)

    def is_coupon_valid(self, td=None):
        import datetime
        today = datetime.date.today()
        if td:
            today = td
        if self.date_init <= today:
            if self.date_expiry >= today:
                return "valid"
            elif self.date_expiry < today:
                return "expired"
        else:
            return "upcoming"
#{
#price_key :
#type : 'flat', 'discount', 'percent'
#value : 99,50,100,
#cap :
#
#}


# --------------------------------------Website Revamp ------------------------

class Vehicle(models.Model):
    make 				= models.CharField(max_length=50)
    model 				= models.CharField(max_length=50)
    year 				= models.CharField(max_length=50)
    fuel_type 			= models.CharField(max_length=50)
    full_veh_name 		= models.CharField(max_length=200)
    aspect_ratio 		= models.CharField(max_length=20)
    type 				= models.CharField(max_length=200)
    car_bike 			= models.CharField(max_length=50)
    engine_oil			= models.CharField(max_length=50)
    active				= models.CharField(max_length=50)

class ServiceLabour(models.Model):
    city 				= models.CharField(max_length=200)
    vendor              = models.CharField(max_length=200)
    car_bike 			= models.CharField(max_length=50)
    service_cat			= models.CharField(max_length=200)
    job_name 	        = models.CharField(max_length=200)
    job_sub_cat         = models.CharField(max_length=200)
    type                = models.CharField(max_length=200)
    total_price         = models.FloatField(max_length=50)
    total_price_comp    = models.FloatField(max_length=50)
    doorstep            = models.CharField(max_length=50)
    # year 				= models.CharField(max_length=50)
    # fuel_type 			= models.CharField(max_length=50)
    # full_veh_name 		= models.CharField(max_length=200)
    # aspect_ratio 		= models.CharField(max_length=20)
    job_summary         = ListField(models.CharField(max_length=200))
    job_desc            = models.CharField(max_length=500)
    job_symptoms        = ListField(models.CharField(max_length=200))
    job_features        = ListField(models.CharField(max_length=200))
    time                = models.CharField(max_length=50)
    price_active        = models.CharField(max_length=20)
    priority            = models.CharField(max_length=50)
    settlement_cat      = models.CharField(max_length=50)

class ServicePart(models.Model):
    city 				= models.CharField(max_length=200)
    vendor              = models.CharField(max_length=200)
    make 				= models.CharField(max_length=50)
    model 				= models.CharField(max_length=50)
    year 				= models.CharField(max_length=50)
    fuel_type 			= models.CharField(max_length=50)
    full_veh_name 		= models.CharField(max_length=200)
    type 				= models.CharField(max_length=200)
    car_bike 			= models.CharField(max_length=50)
    doorstep            = models.CharField(max_length=50)
    service_cat			= models.CharField(max_length=200)
    job_name 	        = models.CharField(max_length=200)
    job_sub_cat         = models.CharField(max_length=200)
    default_components  = ListField(DictField())
    optional_components = ListField(DictField())
    total_price         = models.FloatField(max_length=50)
    total_price_comp    = models.FloatField(max_length=50)

class Services(models.Model):
    city 				= models.CharField(max_length=200)
    vendor              = models.CharField(max_length=200)
    car_bike 			= models.CharField(max_length=50)
    service_cat			= models.CharField(max_length=200)
    job_name 	        = models.CharField(max_length=200)
    job_sub_cat         = models.CharField(max_length=200)
    type                = models.CharField(max_length=200)
    total_price         = models.FloatField(max_length=50)
    total_price_comp    = models.FloatField(max_length=50)
    doorstep            = models.CharField(max_length=200)
    year 				= models.CharField(max_length=50)
    fuel_type 			= models.CharField(max_length=50)
    full_veh_name 		= models.CharField(max_length=200)
    aspect_ratio 		= models.CharField(max_length=20)
    job_summary         = ListField(models.CharField(max_length=200))
    job_desc            = models.CharField(max_length=500)
    job_symptoms        = ListField(models.CharField(max_length=200))
    job_features        = ListField(models.CharField(max_length=200))
    time                = models.CharField(max_length=200)
    price_active        = models.CharField(max_length=20)
    priority            = models.CharField(max_length=50)
    make 				= models.CharField(max_length=50)
    model 				= models.CharField(max_length=50)
    default_components  = ListField(DictField())
    optional_components = ListField(DictField())
    total_part          = models.FloatField(max_length=50, null=True)
    total_labour        = models.FloatField(max_length=50, null=True)
    total_discount      = models.FloatField(max_length=50, null=True)

# class Leads(models.Model):
#     lead_id              = models.IntegerField()
#     lead_timestamp       = models.CharField(max_length=200)
#     follow_up_date       = models.CharField(max_length=200)
#     last_activity        = models.CharField(max_length=200)
#     # cust_id              = models.CharField(max_length=200)
#     cust_name            = models.CharField(max_length=200)
#     cust_make            = models.CharField(max_length=200)
#     cust_model           = models.CharField(max_length=200)
#     cust_vehicle_type    = models.CharField(max_length=200)
#     cust_fuel_varient    = models.CharField(max_length=200)
#     cust_regnumber       = models.CharField(max_length=200,null=True)
#     cust_number          = models.CharField(max_length=200)
#     cust_email           = models.CharField(max_length=200)
#     cust_address         = models.CharField(max_length=200)
#     cust_locality        = models.CharField(max_length=200)
#     cust_city            = models.CharField(max_length=200)
#     service_items        = ListField(DictField())
#     price_total          = models.CharField(max_length=200)
#     date_booking         = models.CharField(max_length=200)
#     time_booking         = models.CharField(max_length=200)
#     is_paid              = models.BooleanField()
#     amount_paid          = models.CharField(max_length=200)
#     status               = models.CharField(max_length=200)
#     coupon               = models.CharField(max_length=200,null=True)
#     comments             = models.CharField(max_length=300)
#     source               = models.CharField(max_length=200)
#     lead_owner           = models.CharField(max_length=200)
class Subscriptions(models.Model):
    booking_timestamp       = models.CharField(max_length=200)
    subscription_id         = models.IntegerField()
    cust_id                 = models.CharField(max_length=200)
    cust_fname              = models.CharField(max_length=200)
    cust_lname              = models.CharField(max_length=200)
    cust_make               = models.CharField(max_length=200)
    cust_model              = models.CharField(max_length=200)
    cust_vehicle_type       = models.CharField(max_length=200)
    cust_fuel_varient       = models.CharField(max_length=200)
    cust_regnumber          = models.CharField(max_length=200, null=True)
    cust_vehicle_vin        = models.CharField(max_length=200, null=True)
    cust_number_primary     = models.CharField(max_length=200)
    cust_number_secondary   = models.CharField(max_length=200)
    cust_email              = models.CharField(max_length=200)
    cust_address            = models.CharField(max_length=200)
    cust_locality           = models.CharField(max_length=200)
    cust_city               = models.CharField(max_length=200)
    cust_state              = models.CharField(max_length=200)
    subscription_type       = models.CharField(max_length=200)
    package_name            = models.CharField(max_length=200)
    date_veh_purchase       = models.DateField(null=True)
    date_start              = models.DateField(null=True)
    date_end                = models.DateField(null=True)
    is_active               = models.BooleanField(default=False)
    amount_paid             = models.CharField(max_length=200, null=True)
    status                  = models.CharField(max_length=200,default="Under Review")
    comment                 = models.CharField(max_length=500, null=True)
    source                  = models.CharField(max_length=200, null=True)


class Bookings(models.Model):
    # booking_flag = True if booking else False if lead
    booking_flag            = models.BooleanField()
    booking_id              = models.IntegerField()
    booking_timestamp       = models.CharField(max_length=200)
    cust_id                 = models.CharField(max_length=200)
    cust_name               = models.CharField(max_length=200)
    cust_make               = models.CharField(max_length=200)
    cust_model              = models.CharField(max_length=200)
    cust_vehicle_type       = models.CharField(max_length=200)
    cust_fuel_varient       = models.CharField(max_length=200)
    cust_regnumber          = models.CharField(max_length=200,null=True)
    cust_number             = models.CharField(max_length=200)
    cust_email              = models.CharField(max_length=200)
    cust_address            = models.CharField(max_length=200)
    cust_locality           = models.CharField(max_length=200)
    cust_city               = models.CharField(max_length=200)
    service_items           = ListField(DictField())
    price_total             = models.CharField(max_length=200)
    price_labour            = models.CharField(max_length=200,null=True)
    price_part              = models.CharField(max_length=200,null=True)
    price_discount          = models.CharField(max_length=200,null=True)
    date_booking            = models.DateField()
    time_booking            = models.CharField(max_length=200)
    date_delivery           = models.DateField(null=True)
    is_paid                 = models.BooleanField()
    amount_paid             = models.CharField(max_length=200, default = "0", null=True)
    coupon                  = models.CharField(max_length=200, null=True)
    status                  = models.CharField(max_length=200)
    comments                = models.CharField(max_length=500, null=True)
    jobssummary             = ListField(DictField())
    # Price Job Item
    source                  = models.CharField(max_length= 200, null=True)
    agent                   = models.CharField(max_length= 200, null=True)
    estimate_history        = ListField(DictField())
    customer_notes          = models.CharField(max_length= 500, null=True)
    booking_user_type       = models.CharField(max_length= 500, default="User", null=True)
    booking_user_name       = models.CharField(max_length= 200)
    booking_user_number     = models.CharField(max_length= 200)
    clickgarage_flag        = models.BooleanField(default= True)
    booking_owner           = models.CharField(max_length= 200, default="ClickGarage")
    odometer                = models.CharField(max_length= 200, null=True)
    escalation_flag         = models.BooleanField(default= False)
    bill_id                 = models.CharField(max_length = 200)
    bill_generation_flag    = models.BooleanField(default = False)
    payment_status          = models.CharField(max_length = 200)
    payment_booking         = ListField(DictField())
    feedback_1              = models.BooleanField(default=False)
    feedback_2              = models.BooleanField(default=False)
    follow_up_date          = models.DateField(null=True)
    follow_up_time          = models.TimeField(null=True)
    follow_up_status        = ListField(DictField())
    purchase_price_total    = models.CharField(max_length=200)
    commission              = ListField(DictField())
    commission_total        = models.CharField(max_length=200,null=True,default="0")
    job_completion_flag     = models.BooleanField(default=False)
    frozen_flag             = models.BooleanField(default=False)
    settlement_flag         = models.BooleanField(default=False)
    delay_count             = models.IntegerField(default=0)
    # int_job_summary         = ListField(DictField(), null=True)



class BookingsBackup(models.Model):
    # booking_flag = True if booking else False if lead
    booking_flag            = models.BooleanField()
    booking_id              = models.IntegerField()
    booking_timestamp       = models.CharField(max_length=200)
    cust_id                 = models.CharField(max_length=200)
    cust_name               = models.CharField(max_length=200)
    cust_make               = models.CharField(max_length=200)
    cust_model              = models.CharField(max_length=200)
    cust_vehicle_type       = models.CharField(max_length=200)
    cust_fuel_varient       = models.CharField(max_length=200)
    cust_regnumber          = models.CharField(max_length=200,null=True)
    cust_number             = models.CharField(max_length=200)
    cust_email              = models.CharField(max_length=200)
    cust_address            = models.CharField(max_length=200)
    cust_locality           = models.CharField(max_length=200)
    cust_city               = models.CharField(max_length=200)
    service_items           = ListField(DictField())
    price_total             = models.CharField(max_length=200)
    price_labour            = models.CharField(max_length=200,null=True)
    price_part              = models.CharField(max_length=200,null=True)
    price_discount          = models.CharField(max_length=200,null=True)
    date_booking            = models.DateField()
    time_booking            = models.CharField(max_length=200)
    date_delivery           = models.DateField(null=True)
    is_paid                 = models.BooleanField()
    amount_paid             = models.CharField(max_length=200, null=True)
    coupon                  = models.CharField(max_length=200, null=True)
    status                  = models.CharField(max_length=200)
    comments                = models.CharField(max_length=500, null=True)
    jobssummary             = ListField(DictField())
    # Price Job Item
    source                  = models.CharField(max_length=200, null=True)
    agent                   = models.CharField(max_length=200, null=True)
    estimate_history        = ListField(DictField())
    customer_notes          = models.CharField(max_length=500, null=True)
    booking_user_type       = models.CharField(max_length=500, default="User", null=True)
    booking_user_name       = models.CharField(max_length=200)
    booking_user_number     = models.CharField(max_length=200)
    clickgarage_flag        = models.BooleanField(default=True)
    booking_owner           = models.CharField(max_length=200, default="ClickGarage")
    odometer                = models.CharField(max_length=200, null=True)
    escalation_flag         = models.BooleanField(default=False)
    bill_id                 = models.CharField(max_length = 200)
    bill_generation_flag    = models.BooleanField(default=False)
    payment_status          = models.CharField(max_length = 200)
    feedback_1              = models.BooleanField(default=False)
    feedback_2              = models.BooleanField(default=False)
    follow_up_date          = models.DateField(null=True)
    follow_up_time          = models.TimeField(null=True)
    follow_up_status        = ListField(DictField())

class Bills(models.Model):
    clickgarage_flag            = models.BooleanField()
    invoice_number              = models.IntegerField()
    total_amount                = models.CharField(max_length=200)
    part_amount                 = models.CharField(max_length=200)
    lube_amount                 = models.CharField(max_length=200)
    consumable_amount           = models.CharField(max_length=200)
    labour_amount               = models.CharField(max_length=200)
    vat_part                    = models.CharField(max_length=200)
    vat_lube                    = models.CharField(max_length=200)
    vat_consumable              = models.CharField(max_length=200)
    service_tax                 = models.CharField(max_length=200)
    components                  = ListField(DictField())
    status                      = models.CharField(max_length=200)
    booking_data_id             = models.CharField(max_length=200)
    date_created                = models.DateField()
    time_stamp                  =  models.CharField(max_length=50)
    owner                       = models.CharField(max_length=200)
    file_name                   = models.CharField(max_length=200, null=True)
    payment_status              = models.CharField(max_length=200, null=True)
    amount_paid                 = models.BooleanField(default=False)
    payment_mode                = models.CharField(max_length=200)
    notes                       = models.CharField(max_length=500, null=True)
    state                       = models.CharField(max_length=200)
    vat_part_percent            = models.CharField(max_length=50)
    vat_lube_percent            = models.CharField(max_length=50)
    vat_consumable_percent      = models.CharField(max_length=50)
    service_tax_percent         = models.CharField(max_length=50)
    agent_name                  = models.CharField(max_length=200)
    agent_address               = models.CharField(max_length=200)
    # agent_locality              = models.CharField(max_length=200)
    # agent_city                  = models.CharField(max_length=200)
    agent_vat_no                = models.CharField(max_length=200)
    agent_cin                   = models.CharField(max_length=200)
    agent_stax                  = models.CharField(max_length=200)
    cust_name                   = models.CharField(max_length=200)
    cust_address                = models.CharField(max_length=200,null=True)
    cust_locality               = models.CharField(max_length=200,null=True)
    cust_city                   = models.CharField(max_length=200,null=True)
    reg_number                  = models.CharField(max_length=200,null=True)
    vehicle                     = models.CharField(max_length=200)
    bill_type                   = models.CharField(max_length=200)
    date_due                    = models.DateField()
    cust_id                     = models.CharField(max_length=200,null=True)
    cust_number                 =  models.CharField(max_length=200,null=True)
    cust_email                  = models.CharField(max_length=200,null=True)
    payment_bill                = ListField(DictField())
    total_recieved_amount       = models.CharField(max_length=200,null=True, default = "0")


class Feedback(models.Model):
    clickgarage_flag            = models.BooleanField()
    booking_data_id             = models.CharField(max_length=200)
    time_stamp                  = models.CharField(max_length=50)
    pick_on_time                = models.CharField(max_length=50,null=True)
    delivery_on_time            = models.CharField(max_length=50,null=True)
    courteous                   = models.CharField(max_length=50,null=True)
    washing                     = models.CharField(max_length=50,null=True)
    quality_of_service          = models.CharField(max_length=50,null=True)
    experience                  = models.CharField(max_length=50,null=True)
    additional                  = models.CharField(max_length=600,null=True)
    recommend_factor            = models.CharField(max_length=50,null=True)

class Expenses(models.Model):
    timestamp_expense    = models.CharField(max_length=200)
    date_expense    = models.DateField()
    category        = models.CharField(max_length=200)
    sub_category    = models.CharField(max_length=200)
    reason          = models.CharField(max_length=200)
    comment         = models.CharField(max_length=500)
    amount          = models.CharField(max_length=200)
    expense_owner   = models.CharField(max_length=200,default="ClickGarage")
    added_by        = models.CharField(max_length=200)

class Messages(models.Model):
    firstname           = models.CharField(max_length=50)
    lastname            = models.CharField(max_length=50)
    number              = models.CharField(max_length=50)
    message             = models.CharField(max_length=1000)
    email               = models.CharField(max_length=50)
    time_stamp          = models.CharField(max_length=50)

class Otp(models.Model):
    mobile = models.CharField(max_length=50)
    otp = models.CharField(max_length=50)
    created      =   models.DateTimeField(default=None)
    updated      =   models.DateTimeField(default=None)
    username     = models.CharField(max_length=50)

class CouponNew(models.Model):
    datetime_created    = models.CharField(max_length=50)
    date_start          = models.DateField(default=None)
    expiry_date         = models.DateField(default=None)
    type                = models.CharField(max_length=50, null=True)
    active              = models.BooleanField()
    message             = models.CharField(max_length=500)
    coupon_code         = models.CharField(max_length=50)
    category            = models.CharField(max_length=50)
    value               = models.FloatField()
    car_bike            = models.CharField(max_length=50)
    cap                 = models.FloatField(null=True)


class Taxes(models.Model):
    state             = models.CharField(max_length=200)
    vat_parts         = models.CharField(max_length=50)
    vat_lubes            = models.CharField(max_length=50)
    vat_consumable = models.CharField(max_length=50)
    service_tax = models.CharField(max_length=50)




