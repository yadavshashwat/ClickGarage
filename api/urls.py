from django.conf.urls import include, url
#from django.conf.urls.defaults import patterns, include, url
#from django.conf import settings

#import api

#from access import features
urlpatterns = [
    url(r'fetch_all_cars/$','api.views.fetch_all_cars',name='fetch_all_cars'),
    url(r'fetch_car_list/$','api.views.fetch_car_list',name='fetch_car_list'),
    url(r'fetch_car/$','api.views.fetch_car',name='fetch_car'),
    url(r'request_quote/$','api.views.request_quote',name='request_quote'),

    url(r'fetch_car_autocomplete/$','api.views.fetch_car_autocomplete',name='fetch_car_autocomplete'),

    url(r'fetch_user_login/$','api.views.fetch_user_login',name='fetch_user_login'),
    url(r'fetch_user_details/$','api.views.getUserDetails',name='getUserDetails'),
    url(r'add_to_cart/$','api.views.addItemToCart',name='addItemToCart'),
    url(r'place_order/$','api.views.place_order',name='place_order'),
    url(r'send_contact/$','api.views.send_contact',name='send_contact'),
    url(r'add_guest_transaction/$','api.views.add_guest_transaction',name='add_guest_transaction'),
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
    url(r'fetch_car_complete/$','api.views.fetch_car_complete',name='fetch_car_complete'),
    url(r'fetch_all_booking/$','api.views.fetch_all_booking',name='fetch_all_booking'),
    url(r'fetch_car_cancelled/$','api.views.fetch_car_cancelled',name='fetch_car_cancelled'),
    url(r'cancel_booking/$','api.views.cancel_booking',name='cancel_booking'),
    url(r'apply_coupon/$','api.views.apply_coupon',name='apply_coupon'),
    url(r'add_coupon/$','api.views.add_coupon',name='add_coupon'),
    url(r'send_otp/$','api.views.send_otp',name='send_otp'),
    url(r'fetch_all_otp/$','api.views.fetch_all_otp',name='fetch_all_otp'),
    url(r'create_otp_user/$','api.views.create_otp_user',name='create_otp_user'),
    url(r'order_complete/$','api.views.order_complete',name='order_complete'),
    url(r'cancel_booking_new/$','api.views.cancel_booking_new',name='cancel_booking_new'),
    url(r'service_selected/$','api.views.service_selected',name='service_selected'),
    url(r'fetch_all_users/$','api.views.fetch_all_users',name='fetch_all_users'),
    url(r'fetch_user_cart/$','api.views.fetch_user_cart',name='fetch_user_cart'),
    url(r'fetch_additional_details/$','api.views.fetch_additional_details',name='fetch_additional_details'),

    #url(r'fetch_all_cleaning/$','api.views.fetch_all_cleaning',name='fetch_all_cleaning'),
    #url(r'fetch_clean_service/$','api.views.fetch_clean_service',name='fetch_clean_service'),
    #
    #url(r'fetch_all_cleaningdealer/$','api.views.fetch_all_cleaningdealer',name='fetch_all_cleaningdealer'),
    #url(r'fetch_dealer_cleancat/$','api.views.fetch_dealer_cleancat',name='fetch_dealer_cleancat'),
    #url(r'fetch_clean_catservice/$','api.views.fetch_clean_catservice',name='fetch_clean_catservice'),
    #url(r'fetch_all_cleaningcat/$','api.views.fetch_all_cleaningcat',name='fetch_all_cleaningcat'),
    # url(r'fetch_all_cleaningcatservices/$','api.views.fetch_all_cleaningcatservices',name='fetch_all_cleaningcatservices'),
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
    url(r'fetch_all_tyresales/$','api.views.fetch_all_tyresales',name='fetch_all_tyresales'),

    #drivers
    # url(r'signUpDriver/$','api.views.signUpDriver',name='signUpDriver'),
    # url(r'updateBookingStatus/$','api.views.updateBookingStatus',name='updateBookingStatus'),
    # url(r'getDriverBookings/$','api.views.getDriverBookings',name='getDriverBookings'),



# <<------------- Website revamp --------------->>

    url(r'get_make_model/$', 'api.views.get_make_model', name='get_make_model'),
    url(r'get_type_make/$', 'api.views.get_type_make', name='get_type_make'),
    url(r'get_jobs_vehicle/$', 'api.views.get_jobs_vehicle', name='get_jobs_vehicle'),
    url(r'add_job_cart/$', 'api.views.add_job_cart', name='add_job_cart'),
    url(r'get_location/$', 'api.views.get_location', name='get_location'),
    url(r'post_message/$', 'api.views.post_message', name='post_message'),
    url(r'send_otp_new/$', 'api.views.send_otp_new', name='send_otp_new'),
    # url(r'send_otp_booking/$', 'api.views.send_otp_booking', name='send_otp_booking'),
    url(r'view_all_bookings/$', 'api.views.view_all_bookings', name='view_all_bookings'),
    url(r'verify_otp_password_cookie/$', 'api.views.verify_otp_password_cookie', name='verify_otp_password_cookie'),
    url(r'set_password_otp/$', 'api.views.set_password_otp', name='set_password_otp'),
    url(r'sign_up_otp/$', 'api.views.sign_up_otp', name='sign_up_otp'),
    url(r'logout_view/$', 'api.views.logout_view', name='logout_view'),
    url(r'view_all_bookings/$', 'api.views.view_all_bookings', name='view_all_bookings'),
    url(r'update_user/$', 'api.views.update_user', name='update_user'),
    url(r'update_booking/$', 'api.views.update_booking', name='update_booking'),
    url(r'update_estimate/$', 'api.views.update_estimate', name='update_estimate'),
    url(r'update_agent/$', 'api.views.update_agent', name='update_agent'),
    url(r'change_status/$', 'api.views.change_status', name='change_status'),
    url(r'call_customer/$', 'api.views.call_customer', name='call_customer'),
    url(r'add_modify_coupon/$', 'api.views.add_modify_coupon', name='add_modify_coupon'),
    url(r'view_all_coupons/$', 'api.views.view_all_coupons', name='view_all_coupons'),
    url(r'check_coupon/$', 'api.views.check_coupon', name='check_coupon'),
    url(r'send_booking/$', 'api.views.send_booking', name='send_booking'),
    url(r'send_lead/$', 'api.views.send_lead', name='send_lead'),
    url(r'generate_bill/$', 'api.views.generate_bill', name='generate_bill'),

    # Website Api Check
    url(r'get_all_models/$', 'api.views.get_all_models', name='get_all_models'),
    url(r'get_all_jobs/$', 'api.views.get_all_jobs', name='get_all_jobs'),
    url(r'get_all_labour/$', 'api.views.get_all_labour', name='get_all_labour'),
    url(r'get_all_part/$', 'api.views.get_all_part', name='get_all_part'),
    url(r'get_all_taxes/$', 'api.views.get_all_taxes', name='get_all_taxes'),
    url(r'view_all_bills/$', 'api.views.view_all_bills', name='view_all_bills'),

]
