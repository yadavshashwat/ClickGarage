from django.conf.urls import include, url
#from django.conf.urls.defaults import patterns, include, url
#from django.conf import settings

#import api

#from access import features
urlpatterns = [
    url(r'fetch_all_cars/$','api.views.fetch_all_cars',name='fetch_all_cars'),
    url(r'fetch_car_list/$','api.views.fetch_car_list',name='fetch_car_list'),
    url(r'fetch_car/$','api.views.fetch_car',name='fetch_car'),

    url(r'fetch_car_autocomplete/$','api.views.fetch_car_autocomplete',name='fetch_car_autocomplete'),

    url(r'fetch_user_details/$','api.views.getUserDetails',name='getUserDetails'),
    url(r'add_to_cart/$','api.views.addItemToCart',name='addItemToCart'),
    url(r'place_order/$','api.views.place_order',name='place_order'),
    url(r'place_emergency_order/$','api.views.place_emergency_order',name='place_emergency_order'),
    #car_<servicename>, <servicename>_details
    # params : c_id,
    url(r'fetch_car_servicing/$','api.views.fetch_car_services',name='fetch_car_services'),
    # params : service_id
    url(r'fetch_servicing_details/$','api.views.fetch_car_servicedetails',name='fetch_car_servicedetails'),

    # params : c_id,
    url(r'fetch_car_servicing_new/$','api.views.fetch_car_services_new',name='fetch_car_services'),
    # params : service_id
    url(r'fetch_servicing_details_new/$','api.views.fetch_car_servicedetails_new',name='fetch_car_servicedetails'),

    # params : none
    url(r'fetch_car_cleaning/$','api.views.fetch_all_cleaning',name='fetch_all_cleaning'),
    # params : service_id, c_id
    url(r'fetch_cleaning_details/$','api.views.fetch_clean_service',name='fetch_clean_service'),
        # params : none
    url(r'fetch_car_cleaning_new/$','api.views.fetch_all_cleaning',name='fetch_all_cleaning'),
    # params : service_id, c_id
    url(r'fetch_cleaning_details_new/$','api.views.fetch_clean_service',name='fetch_clean_service'),



    # params : none
    url(r'fetch_car_vas/$','api.views.fetch_all_vas',name='fetch_all_vas'),
    # params : service_id, c_id
    url(r'fetch_vas_details/$','api.views.fetch_vas_service',name='fetch_vas_service'),
    # params : c_id
    url(r'fetch_car_windshield/$','api.views.fetch_car_windshieldservices',name='fetch_car_windshieldservices'),
    # params : service_id
    url(r'fetch_windshield_details/$','api.views.fetch_car_windshieldcatdetails',name='fetch_car_windshieldcatdetails'),
    # url(r'fetch_car_servicedealercat/$','api.views.fetch_car_servicedealercat',name='fetch_car_servicedealercat'),
    
    # Booking page jugad
    url(r'fetch_car_booking/$','api.views.fetch_car_booking',name='fetch_car_booking'),
    url(r'fetch_all_booking/$','api.views.fetch_all_booking',name='fetch_all_booking'),
    url(r'fetch_car_cancelled/$','api.views.fetch_car_cancelled',name='fetch_car_cancelled'),
    url(r'cancel_booking/$','api.views.cancel_booking',name='cancel_booking'),
    url(r'order_complete/$','api.views.order_complete',name='order_complete'),
    url(r'cancel_booking_new/$','api.views.cancel_booking_new',name='cancel_booking_new'),
    url(r'fetch_all_users/$','api.views.fetch_all_users',name='fetch_all_users'),
    url(r'fetch_additional_details/$','api.views.fetch_additional_details',name='fetch_additional_details'),

    #url(r'fetch_all_cleaning/$','api.views.fetch_all_cleaning',name='fetch_all_cleaning'),
    #url(r'fetch_clean_service/$','api.views.fetch_clean_service',name='fetch_clean_service'),
    #
    #url(r'fetch_all_cleaningdealer/$','api.views.fetch_all_cleaningdealer',name='fetch_all_cleaningdealer'),
    #url(r'fetch_dealer_cleancat/$','api.views.fetch_dealer_cleancat',name='fetch_dealer_cleancat'),
    #url(r'fetch_clean_catservice/$','api.views.fetch_clean_catservice',name='fetch_clean_catservice'),
    #url(r'fetch_all_cleaningcat/$','api.views.fetch_all_cleaningcat',name='fetch_all_cleaningcat'),
    #url(r'fetch_all_cleaningcatservices/$','api.views.fetch_all_cleaningcatservices',name='fetch_all_cleaningcatservices'),
    #  
    #url(r'fetch_all_vas/$','api.views.fetch_all_vas',name='fetch_all_vas'),
    #url(r'fetch_vas_service/$','api.views.fetch_vas_service',name='fetch_vas_service'),
    #
    #url(r'fetch_all_vasdealer/$','api.views.fetch_all_vasdealer',name='fetch_all_vasdealer'),
    #url(r'fetch_dealer_vascat/$','api.views.fetch_dealer_vascat',name='fetch_dealer_vascat'),
    #url(r'fetch_vas_catservice/$','api.views.fetch_vas_catservice',name='fetch_vas_catservice'),
    #url(r'fetch_all_vascat/$','api.views.fetch_all_vascat',name='fetch_all_vascat'),
    #url(r'fetch_all_vascatservices/$','api.views.fetch_all_vascatservices',name='fetch_all_vascatservices'),
    #  
    #url(r'fetch_all_windshieldcatdetails/$','api.views.fetch_all_windshieldcatdetails',name='fetch_all_windshieldcatdetails'),
    #url(r'fetch_all_windshieldservices/$','api.views.fetch_all_windshieldservices',name='fetch_all_windshieldservices'),
    #url(r'fetch_car_windshieldcatdetails/$','api.views.fetch_car_windshieldcatdetails',name='fetch_car_windshieldcatdetails'),
    #url(r'fetch_car_windshieldservices/$','api.views.fetch_car_windshieldservices',name='fetch_car_windshieldservices'),
            


    # url(r'fetch_location/$','api.views.fetch_location',name='fetch_location'),


    url(r'fetch_all_services/$','api.views.fetch_all_services',name='fetch_all_services'),
    url(r'fetch_all_servicedealercat/$','api.views.fetch_all_servicedealercat',name='fetch_all_servicedealercat'),
    url(r'fetch_all_servicedealername/$','api.views.fetch_all_servicedealername',name='fetch_all_servicedealername'),
    
	url(r'fetch_car_tyres/$','api.views.fetch_car_tyres',name='fetch_car_tyres'),

    url(r'fetch_all_wheelservices/$','api.views.fetch_all_wheelservices',name='fetch_all_wheelservices'),
    url(r'fetch_all_wheelserviceprovider/$','api.views.fetch_all_wheelserviceprovider',name='fetch_all_wheelserviceprovider'),
    url(r'fetch_all_tyresales/$','api.views.fetch_all_tyresales',name='fetch_all_tyresales')
	
	
    ]
