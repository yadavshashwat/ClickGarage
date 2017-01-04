from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
import datetime, time, calendar
import urllib
from urllib2 import Request, urlopen
import random

from django.db.models import Max

import operator
import json
import ast
import re
import requests
from django.views.decorators.csrf import csrf_exempt

from models import *
from dataEntry.runentry import carMakers, cleanstring
from activity import views as ac_vi
from mailing import views as mviews
from api import tasks as tasks

from activity.models import Transactions, CGUser
# from lxml import html


tempSecretKey = 'dmFydW5ndWxhdGlsaWtlc2dhbG91dGlrZWJhYg=='
tempSecretParkwheel = 'dGhpcyBrZXkgaXMgZm9yIFBhcmt3aGVlbHM='

repair_map = {
    'diagnostics':{'name':'Diagnostics','detail':"I don't know what is wrong with my car"},
    'dent-paint':{'name':'Denting / Painting','detail':""},
    'custom':{'name':'Custom Repair Request','detail':""}
}

additionalFeatures = {
       'car' : ['Clutch Overhaul', 'Interior Dry-cleaning', 'Brake Repair', 'Wheel Balancing', 'Wheel Alignment', 'AC Servicing', 'Injector Cleaning'],
       'bike' : ['Front Brake Repair',  'Rear Brake repair', 'Wheel Balancing', 'Wheel Alignment']
}
#login views

staffmails = ["shashwat@clickgarage.in", "bhuvan@clickgarage.in","bookings@clickgarage.in","smriti.parmar@clickgarage.in", "rajiv@clickgarage.in","amit.kumar@clickgarage.in"]

def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

def loginview(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def auth_and_login(request, onsuccess='/', onfail='/login/'):
    user = authenticate(username=request.POST['email'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect(onsuccess)
    else:
        return redirect(onfail)

def create_user(username, email, password):
    user = CGUser(username=username, email=email)
    mviews.send_signup_mail(username, "NA", email)
    user.set_password(password)
    # mviews.send_signup_mail(username, "NA", email)
    user.user_type = 'User'
    user.save()
    return user

def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def sign_up_in(request):
    post = request.POST
    # mviews.send_signup_mail(name, "NA", post['email'])
    if not user_exists(post['email']):
        user = create_user(username=post['email'], email=post['email'], password=post['password'])
    	return auth_and_login(request)
    else:
    	return redirect("/login/")
    # mviews.send_signup_mail(name, "NA", post['email'])

@login_required(login_url='/login/')
def secured(request):
    return render_to_response("secure.html")

# Create your views here.
def get_param(req, param, default):
    req_param = None
    if req.method == 'GET':
        q_dict = req.GET
        if param in q_dict:
            req_param = q_dict[param]
    elif req.method == 'POST':
        q_dict = req.POST
        if param in q_dict:
            req_param = q_dict[param]
    if not req_param and default:
        req_param = default
    return req_param

def random_req_auth(request):
    r_id = get_param(request, 'r_id', None)
    if r_id:
        if r_id == tempSecretKey:
            return True

    backend = get_param(request, 'backend', None)
    if backend:
        if ac_vi.register_by_access_token(request, backend):
            return True

    return False

def fetch_all_cars(request):
    obj = {}
    result = []
    allCars = Car.objects.all()
    for car in allCars:
        result.append({'name':car.name, 'make':car.make, 'aspect_ratio':car.aspect_ratio,'size':car.size,'car_bike':car.car_bike,'id':car.id,'cleaning_cat':car.cleaning_cat, 'complete_name':car.complete_vehicle_name})

    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_additional_features(request):
    car_bike = get_param(request,'cb_id', None)
    obj = {}
    obj['status'] = False
    result = []

    if (car_bike == 'car') or (car_bike == 'bike'):
        result=additionalFeatures[car_bike]
        obj['status'] = True

    obj['result'] = result
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')



def fetch_car(request, HTTPFlag=True):
    car_id = get_param(request, 'c_id', None)
    print car_id
    obj = {}
    obj['status'] = False
    carObj = None
    if car_id:
        carObj = Car.objects.filter(id=car_id)
    elif 'clgacarid' in request.COOKIES:
        car_id = request.COOKIES['clgacarid']
        if car_id:
            carObj = Car.objects.filter(id=car_id)

    if carObj and len(carObj):
        carObj = carObj[0]
        result = {'name':carObj.name, 'make':carObj.make, 'aspect_ratio':carObj.aspect_ratio, 'car_bike':carObj.car_bike,'size':carObj.size,'id':carObj.id}
        obj['result'] = result
        obj['status'] = True

    obj['counter'] = 1
    obj['msg'] = "Success"
    if(HTTPFlag):
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return obj

def fetch_car_services(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    import re
    regex = re.compile('^HTTP_')
    headerDict = dict((regex.sub('', header), value) for (header, value) in request.META.items() if header.startswith('HTTP_'))
    print headerDict

    if 1 or random_req_auth(request) or (request.user and request.user.is_authenticated()):
        car_id = get_param(request, 'c_id', None)
        car = None
        make = None
        if car_id:
            carObj = Car.objects.filter(id=car_id)

            if len(carObj):
                carObj = carObj[0]
                car_old = carObj.name
                make = carObj.make
                car = make + " " + car_old
                if car:
                    ServiceObjs = Servicing.objects.filter(carname = car, brand = make).order_by('odometer')
                    #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
                    for service in ServiceObjs:
                        obj['result'].append({
                            'id':service.id
                            ,'name':service.name
                            ,'brand':service.brand
                            ,'car_name':service.carname
                            ,'odometer':service.odometer
                            ,'year':service.year
                            ,'regular_checks':service.regular_checks
                            ,'paid_free':service.paid_free
                            ,'parts_replaced':service.part_replacement
                            ,'dealers_list':service.dealer} )



        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        obj['headers'] = headerDict
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_servicedetails(request):
    service_id = get_param(request, 'service_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    print '-----'
    print request.user
    if 1 or random_req_auth(request) or (request.user and request.user.is_authenticated()):

        car = None
        make = None
        odo = None
        car_2 = None
        if service_id:
            serviceObj = Servicing.objects.filter(id=service_id)
            if len(serviceObj):
                serviceObj = serviceObj[0]
                car = serviceObj.carname
                make = serviceObj.brand
                odo = serviceObj.odometer
                car_2 = cleanstring(car.replace(make,""))
                print car_2
            carObj = Car.objects.filter(name=car_2)
            if len(carObj):
                carObj = carObj[0]
                car_bike = carObj.car_bike
                print car_bike
                if car:
                    ServicedetailObjs = ServiceDealerCat.objects.filter(carname = car, brand = make, odometer=odo).order_by('odometer','dealer_category')
                    for service in ServicedetailObjs:
                        obj['result'].append({
                            'id':service.id
                              ,'name':service.name
                              ,'brand':service.brand
                              ,'car':service.carname
                              ,'odometer':service.odometer
                              ,'vendor':service.dealer_category
                              ,'parts_list':service.part_replacement
                              ,'parts_price':service.price_parts
                              ,'labour_price':service.price_labour
                              ,'wa_price':service.wheel_alignment
                              ,'wb_price':service.wheel_balancing
                              # ,'wa_wb_present':service.WA_WB_Inc
                              ,'dealer_details':service.detail_dealers
                              ,'car_bike':car_bike} )


        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_car_cleaning(request):
    dealers = fetch_all_cleaningdealer(request, False)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if 1 or random_req_auth(request) or (request.user and request.user.is_authenticated()):

        if dealers['result'] and len(dealers['result']):
            obj['status'] = True
            for dealer in dealers['result']:
                print dealer
                CleanCatObjs = CleaningServiceCat.objects.filter(vendor = dealer['name'])
                oneObj = {
                    'name':dealer['name'],
                    'list':[]
                                     }
                for service in CleanCatObjs:
                    oneObj['list'].append({
                            'id':service.id
                          ,'name':service.vendor
                          ,'category':service.category
                          ,'description':service.description
                    })
                obj['result'].append(oneObj)


        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_car_vas(request):
    dealers = fetch_all_vasdealer(request, False)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if random_req_auth(request) or (dealers['result'] and len(dealers['result'])):
        obj['status'] = True
        for dealer in dealers['result']:
            # print dealer
            VASCatObjs = VASServiceCat.objects.filter(vendor = dealer['Name'])
            # CleanCatObjs = CleaningServiceCat.objects.filter(vendor = dealer['Name'])
            oneObj = {
                'name':dealer['Name'],
                'list':[]
                                 }
            for service in VASCatObjs:
                oneObj['list'].append({
                        'id':service.id
                          ,'name':service.vendor
                          ,'category':service.category
                          ,'description':service.description
                })
            obj['result'].append(oneObj)


    return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_all_services(request):
    obj = {}
    result = []
    #Service_wo_sort = Servicing.objects.all()
    allServices = ServicingNew.objects.order_by('type_service')
    for service in allServices:
        result.append({'id':service.id,
                        'name' : service.name  
                        ,'brand' : service.brand     
                        ,'car_name' : service.carname                   
                        ,'type_service' : service.type_service
                        #,'time_reading' : service.year
                        ,'checks_done' : service.regular_checks                    
                        #,'paid_free' : service.paid_free
                        ,'parts_replaced' : service.part_replacement       
                        ,'dealer_category' : service.dealer} )


    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_all_servicedealercat(request):
    obj = {}
    result = []
    allDealerCat = ServiceDealerCatNew.objects.order_by('type_service','dealer_category')

    for service in allDealerCat:

        result.append({ 'id':service.id
                        ,'name':service.name                
                        ,'brand_name':service.brand               
                        ,'car_name':service.carname             
                        ,'type_service':service.type_service
#                        ,'year':service.year

                        ,'dealer_category':service.dealer_category
                        ,'part_dic':service.part_dic
                        ,'parts_replaced':service.part_replacement    
                        ,'parts_price':service.price_parts         
                        ,'labour_price':service.price_labour        
                        ,'wheel_alignment_price':service.wheel_alignment     
                        ,'wheel_balancing_price':service.wheel_balancing     
                        # ,'WA_WB?':service.WA_WB_Inc
                        ,'dealer_details':service.detail_dealers
                        #,'paid_free?':service.paid_free
                        ,'regular_checks':service.regular_checks
                        ,'discount':service.discount
                        ,'priority':service.priority

                        } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_servicedealername(request):
    obj = {}
    result = []
    allDealerCat = ServiceDealerName.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id, 'Name':service.name           
                        ,'make':service.make           
                        ,'dealer_category':service.dealer_category
                        ,'address':service.address        
                        ,'phone':service.phone          
                        ,'timing':service.timing         
                        ,'rating':service.rating         
                        ,'reviews':service.reviews        } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_all_cleaningdealer(request, HTTPFlag = True):
    obj = {}
    result = []
    allDealerCat = CleaningDealerName.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id, 'name':service.vendor           
                        ,'rating':service.rating           
                        ,'description':service.description} )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"


    if(HTTPFlag):
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return obj




def fetch_dealer_cleancat(request):
    vendor_id = get_param(request, 'v_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    car = None
    make = None
    odo = None
    if vendor_id:
        cleanObj = CleaningDealerName.objects.filter(id=vendor_id)
        
        if len(cleanObj):
            cleanObj = cleanObj[0]
            vendor = cleanObj.vendor

            if vendor:
                CleanCatObjs = CleaningServiceCat.objects.filter(vendor = vendor)
                for service in CleanCatObjs:
                    obj['result'].append({
                        'id':service.id
                          ,'name':service.vendor  
                          ,'category':service.category             
                          ,'description':service.description               
                              } )
                      
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_clean_catservice(request):
    catg_id = get_param(request, 'service_id', None)
    car_id = get_param(request,'c_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    car = None
    make = None
    odo = None
    vendor = None
    size = None

    if car_id:
        carObj = Car.objects.filter(id=car_id)
       
        if len(carObj):
            carObj = carObj[0]
            size = carObj.size
            cleaning_cat = carObj.cleaning_cat

    if catg_id:
        cleanObj = CleaningServiceCat.objects.filter(id=catg_id)
        
        if len(cleanObj):
            cleanObj = cleanObj[0]
            vendor = cleanObj.vendor
            category = cleanObj.category


    if vendor:
        if category:
            if size:
             CleanCatObjs = CleaningCategoryServices.objects.filter(vendor = vendor, category = category,car_cat = size).order_by('priority')
             for service in CleanCatObjs:
                obj['result'].append({
                        'id':service.id
                        ,'vendor':service.vendor          
                        ,'category':service.category        
                        ,'car_cat':service.car_cat         
                        ,'service':service.service         
                        ,'price_labour':service.price_labour
                        ,'price_parts':service.price_parts     
                        ,'total_price':service.price_total     
                        ,'description':service.description
                        ,'discount':service.discount
                        ,'rating':service.rating          
                        ,'reviews':service.reviews
                        ,'priority':service.priority
                              } )
                      
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')




def fetch_all_cleaningcat(request):
    obj = {}
    result = []
    allDealerCat = CleaningServiceCat.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id, 'name':service.vendor           
                        ,'category':service.category          
                        ,'description':service.description} )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_cleaningcatservices(request):
    obj = {}
    result = []
    allDealerCat = CleaningCategoryServices.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id
            ,'name':service.vendor         
            ,'category':service.category       
            ,'car_cat':service.car_cat        
            ,'service':service.service        
            ,'price_labour':service.price_labour   
            ,'price_parts':service.price_parts    
            ,'price_total':service.price_total
            ,'discount':service.discount
            ,'service_description':service.description    
            ,'rating':service.rating         
            ,'reviews':service.reviews
            ,'priority':service.priority       } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_vasdealer(request, HTTPFlag=True):
    obj = {}
    result = []
    allDealerCat = VASDealerName.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id, 'Name':service.vendor           
                        ,'Rating':service.rating           
                        ,'Description':service.description} )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    if HTTPFlag:
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return obj


def fetch_dealer_vascat(request):
    vendor_id = get_param(request, 'v_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    car = None
    make = None
    odo = None
    if vendor_id:
        vasObj = VASDealerName.objects.filter(id=vendor_id)
        
        if len(vasObj):
            vasObj = vasObj[0]
            vendor = vasObj.vendor

            if vendor:
                VASCatObjs = VASServiceCat.objects.filter(vendor = vendor)
                for service in VASCatObjs:
                    obj['result'].append({
                        'id':service.id
                          ,'name':service.vendor  
                          ,'category':service.category             
                          ,'description':service.description               
                              } )
                      
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_vas_catservice(request):
    catg_id = get_param(request, 'service_id', None)
    car_id = get_param(request,'c_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    car = None
    make = None
    odo = None
    vendor = None

    if car_id:
        carObj = Car.objects.filter(id=car_id)
       
        if len(carObj):
            carObj = carObj[0]
            size = carObj.size

    if catg_id:
        vasObj = VASServiceCat.objects.filter(id=catg_id)
        
        if len(vasObj):
            vasObj = vasObj[0]
            vendor = vasObj.vendor
            category = vasObj.category


    if vendor:
        if category:
            if size:
             VASCatObjs = VASCategoryServices.objects.filter(vendor = vendor, category = category,car_cat = size).order_by('priority')
             for service in VASCatObjs:
                obj['result'].append({
                        'id':service.id
                        ,'vendor':service.vendor          
                        ,'category':service.category        
                        ,'car_cat':service.car_cat         
                        ,'service':service.service         
                        ,'price_labour':service.price_labour    
                        ,'price_parts':service.price_parts     
                        ,'total_price':service.price_total     
                        ,'description':service.description
                        ,'discount':service.discount
                        ,'doorstep':service.doorstep     
                        ,'rating':service.rating          
                        ,'reviews':service.reviews
                        ,'priority':service.priority
                              } )
                      
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_vascat(request):
    obj = {}
    result = []
    allDealerCat = VASServiceCat.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id, 'name':service.vendor           
                        ,'category':service.category          
                        ,'description':service.description} )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_vascatservices(request):
    obj = {}
    result = []
    allDealerCat = VASCategoryServices.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id
            ,'name':service.vendor         
            ,'category':service.category       
            ,'car_cat':service.car_cat        
            ,'service':service.service        
            ,'price_labour':service.price_labour   
            ,'price_parts':service.price_parts    
            ,'price_total':service.price_total
            ,'discount':service.discount
            ,'service_description':service.description   
            ,'doorstep':service.doorstep 
            ,'rating':service.rating         
            ,'reviews':service.reviews        } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_windshieldservices(request):
    car_id = get_param(request, 'c_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    car = None
    make = None
    if car_id:
        carObj = Car.objects.filter(id=car_id)
        if len(carObj):
            carObj = carObj[0]
            car_old = carObj.name
            make = carObj.make
            car = make + " " + car_old
            if car:
                ServiceObjs = WindShieldCat.objects.filter(carname = car, brand = make).order_by('ws_type')
                #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
                for service in ServiceObjs:
                    obj['result'].append({'id':service.id,
                                        'vendor': service.vendor
                                        , 'brand' :service.brand
                                        , 'carname' :service.carname
                                        , 'ws_type' :service.ws_type } )
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_windshieldcatdetails(request):
    catg_id = get_param(request, 'service_id', None)
    city = get_param(request,'city_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    vendor  = None
    brand   = None
    carname = None
    ws_type = None
    
    
    if catg_id:
        wsObj = WindShieldCat.objects.filter(id=catg_id)
        
        if len(wsObj):
            wsObj = wsObj[0]
            vendor  = wsObj.vendor
            brand   = wsObj.brand
            carname = wsObj.carname
            ws_type = wsObj.ws_type


    if ws_type:
        wsTypeObjs = WindShieldServiceDetails.objects.filter(city=city,vendor = vendor, ws_type = ws_type, carname = carname, brand=brand)
        for service in wsTypeObjs:
            obj['result'].append({'id':service.id
                                    ,'vendor':service.vendor
                                    ,'brand':service.brand
                                    ,'carname':service.carname
                                    ,'colour':service.colour
                                    ,'ws_type':service.ws_type
                                    ,'ws_subtype':service.ws_subtype
                                    ,'price_ws':service.price_ws
                                    ,'price_sealant':service.price_sealant
                                    ,'price_labour':service.price_labour
                                    ,'price_insurance':service.price_insurance 
                                    ,'price_total'    :service.price_total
                                    ,'city'           :service.city
                                    ,'description':service.description
                                    ,'rating':service.rating
                                    ,'reviews':service.reviews
                              } )
                      
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_windshieldservices(request):
    obj = {}
    result = []
    allDealerCat = WindShieldCat.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id
            ,'vendor': service.vendor
            , 'brand' :service.brand
            , 'carname' :service.carname
            , 'ws_type' :service.ws_type } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_windshieldcatdetails(request):
    obj = {}
    result = []
    allDealerCat = WindShieldServiceDetails.objects.all()
    for service in allDealerCat:

        result.append({'id':service.id
            ,'vendor':service.vendor
            ,'brand':service.brand
            ,'carname':service.carname
            ,'ws_type':service.ws_type
            ,'ws_subtype':service.ws_subtype
            ,'price_ws':service.price_ws
            ,'price_sealant':service.price_sealant
            ,'price_labour':service.price_labour
            ,'price_insurance':service.price_insurance  
            ,'city'           :service.city
            ,'description':service.description
            ,'rating':service.rating
            ,'reviews':service.reviews              } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')





def fetch_all_wheelservices(request):
    obj = {}
    result = []
    allServices = WheelServices.objects.all()
    for service in allServices:
        result.append({'id':service.id,
                        'name':service.name        
                        ,'service':service.service     
                        ,'description':service.description     

            } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_wheelserviceprovider(request):
    obj = {}
    result = []
    allServices = WheelServiceProvider.objects.all()
    for service in allServices:
        result.append({'id':service.id,
                'name':service.name    
                ,'address':service.address 
                ,'phone':service.phone   
                ,'timing':service.timing  
                ,'rating':service.rating  
                ,'reviews':service.reviews 
                ,'service':service.service 
                ,'car':service.car     
                ,'price':service.price   } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_tyresales(request):
    obj = {}
    result = []
    allServices = TyreSale.objects.all()
    for service in allServices:
        result.append({'id':service.id,
                    'name':service.name          
                    ,'address':service.address       
                    ,'rating_dealer':service.rating_dealer 
                    ,'aspect_key':service.aspect_key    
                    ,'brand':service.brand         
                    ,'model':service.model         
                    ,'width':service.width         
                    ,'aspect_ratio':service.aspect_ratio  
                    ,'rim_size':service.rim_size      
                    ,'load_rating':service.load_rating   
                    ,'speed_rating':service.speed_rating  
                    ,'warranty':service.warranty      
                    ,'rating':service.rating        
                    ,'reviews':service.reviews       
                    ,'price':service.price                         

                 } )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_tyres(request):
    car_id = get_param(request, 'c_id', None)
    obj = {}
    aspect = None
    obj['status'] = False
    obj['result'] =[]
    if car_id:
        carObj = Car.objects.filter(id=car_id)

        if len(carObj):
            carObj = carObj[0]
            aspect = carObj.aspect_ratio.replace("R","")    
            
            if aspect:
                tyreObjs = TyreSale.objects.filter(aspect_key = aspect)

                for tyre in tyreObjs:
                    obj['result'].append({'id':tyre.id,
                    'name':tyre.name          
                    ,'address':tyre.address       
                    ,'rating_dealer':tyre.rating_dealer 
                    ,'aspect_key':tyre.aspect_key    
                    ,'brand':tyre.brand         
                    ,'model':tyre.model         
                    ,'width':tyre.width         
                    ,'aspect_ratio':tyre.aspect_ratio  
                    ,'rim_size':tyre.rim_size      
                    ,'load_rating':tyre.load_rating   
                    ,'speed_rating':tyre.speed_rating  
                    ,'warranty':tyre.warranty      
                    ,'rating':tyre.rating        
                    ,'reviews':tyre.reviews       
                    ,'price':tyre.price                         
                 } )
                  
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"

    return HttpResponse(json.dumps(obj), content_type='application/json')

@csrf_exempt
def addItemToCart(request):
    cookie_data = get_param(request, 'cookie',None)
    car_id = get_param(request, 'car_id',None)
    remove = get_param(request, 'delete',False)
    additional_info = get_param(request, 'additional', None)
    obj = {}
    obj['status'] = False
    obj['result'] =[]

    # print request
    if remove:
        print 'remove this'
    if request.user.is_authenticated():
        if cookie_data:
            if remove:
                resp = ac_vi.updateCart(request.user, cookie_data, 'delete', car_id, None)
            else:
                resp = ac_vi.updateCart(request.user, cookie_data, 'add', car_id, additional_info)


    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"

    return HttpResponse(json.dumps(obj), content_type='application/json')

def getUserDetails(request):
    obj = {}
    obj['status'] = True
    obj['result'] ={}

    if request.user.is_authenticated() or random_req_auth(request) :
        res = {}
        res['userid'] = request.user.id
        res['u_cart'] = request.user.unchecked_cart
        res['uc_cart'] = request.user.uc_cart
        res['saved_addresses'] = request.user.saved_address
        obj['result'] = res
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_user_login(request):
    obj = {}
    obj['status'] = True
    obj['result'] ={}
    res = {}

    if request.user.is_authenticated() or random_req_auth(request):
        res['userid'] = request.user.id
        if request.user.first_name and len(request.user.first_name):
            res['username'] = request.user.first_name
        else:
            res['username'] = request.user.username
        # res['username'] = request.user.first_name
        res['contact'] = request.user.contact_no
        res['email'] = request.user.email
        res['auth'] = True
    else:
        res['auth'] = False
    # mviews.send_signup_mail(request.user.first_name, request.user.contact_no, request.user.email)
    obj['result'] = res

    return HttpResponse(json.dumps(obj), content_type='application/json')


def getCarObjFromName(carNameArray):
    res = []
    for carCompoundName in carNameArray:
         carCompoundName = cleanstring(carCompoundName)
         make = carCompoundName.split(' ')[0]
         make2 = " ".join([carCompoundName.split(' ')[0], carCompoundName.split(' ')[1]])
         name_model = ''

         if make in carMakers:
             name_model = carCompoundName.split(' ', 1)[1]
         elif make2 in carMakers:
             make = make2
             name_model = carCompoundName.split(' ', 2)[2]
         else:
             make = ''
             name_model = carCompoundName


         # if make not in carMakers:
         #     make = ''
         #     name_model = carCompoundName
         # elif make2 in
         # else:
         #     name_model = carCompoundName.split(' ', 1)[1]

         # print name_model
         findCar = Car.objects.filter(name=name_model, make=make)
         if len(findCar):
            carObj = findCar[0]
            result = {'name':carObj.name, 'make':carObj.make, 'aspect_ratio':carObj.aspect_ratio, 'size':carObj.size,'id':carObj.id, 'car_bike':carObj.car_bike}
            res.append(result)

    return res

def fetch_all_cleaning(request, HTTPFlag = True):
    obj = {}
    result = []
    car_id = get_param(request,'c_id',None)
    car_bike = None
    if car_id:
        carObj = Car.objects.filter(id=car_id)
       
        if len(carObj):
            carObj = carObj[0]
            size = carObj.size
            car_bike = carObj.car_bike
            print size

    allDealerCat = CleaningCatName.objects.filter(car_bike = car_bike)
    for service in allDealerCat:

        result.append({'id':service.id         
                        ,'category':service.category          
                        ,'description':service.description
                        ,'car_bike':service.car_bike} )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"


    if(HTTPFlag):
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return obj

def fetch_clean_service(request):
    catg_id = get_param(request, 'service_id', None)
    car_id = get_param(request,'c_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if 1 or random_req_auth(request) or (request.user and request.user.is_authenticated()):

        car = None
        make = None
        odo = None
        vendor = None
        size = None
        category = None
        car_bike = None

        if car_id:
            carObj = Car.objects.filter(id=car_id)

            if len(carObj):
                carObj = carObj[0]
                size = carObj.size
                car_bike = carObj.car_bike
                cleaning_cat = carObj.cleaning_cat
                print size
        if catg_id:
            cleanObj = CleaningCatName.objects.filter(id=catg_id)

            if len(cleanObj):
                cleanObj = cleanObj[0]
                category = cleanObj.category

                print category


        if category:
            if size:
                CleanCatObjs2 = CleaningCategoryServices.objects.filter(category = category,car_cat = cleaning_cat , car_bike = car_bike).order_by('priority')
                CleanCatObjs1 = CleaningCategoryServices.objects.filter(category = category,car_cat = size, car_bike = car_bike).order_by('priority')
                # CleanCatObjs =
                for service in CleanCatObjs2:
                    obj['result'].append({
                            'id':service.id
                            ,'vendor':service.vendor
                            ,'category':service.category
                            ,'car_cat':service.car_cat
                            ,'service':service.service
                            ,'price_labour':service.price_labour
                            ,'price_parts':service.price_parts
                            ,'total_price':service.price_total
                            ,'discount':service.discount
                            ,'description':service.description
                            ,'doorstep':service.doorstep
                            ,'rating':service.rating
                            ,'reviews':service.reviews
                            ,'car_bike': service.car_bike
                            ,'priority':service.priority
                                  } )
                for service in CleanCatObjs1:
                    obj['result'].append({
                            'id':service.id
                            ,'vendor':service.vendor
                            ,'category':service.category
                            ,'car_cat':service.car_cat
                            ,'service':service.service
                            ,'price_labour':service.price_labour
                            ,'price_parts':service.price_parts
                            ,'total_price':service.price_total
                            ,'discount':service.discount
                            ,'description':service.description
                            ,'doorstep':service.doorstep
                            ,'rating':service.rating
                            ,'reviews':service.reviews
                            ,'car_bike': service.car_bike
                            ,'priority':service.priority
                                  } )

        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')

    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_all_vas(request, HTTPFlag = True):
    obj = {}
    result = []
    car_id = get_param(request,'c_id',None)
    car_bike = None
    if car_id:
        carObj = Car.objects.filter(id=car_id)
       
        if len(carObj):
            carObj = carObj[0]
            size = carObj.size
            car_bike = carObj.car_bike
            print size

    allDealerCat = VASCatName.objects.filter(car_bike = car_bike)   
    for service in allDealerCat:
        result.append({'id':service.id         
                        ,'category':service.category          
                        ,'description':service.description} )
    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"


    if(HTTPFlag):
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return obj


def fetch_vas_service(request):
    catg_id = get_param(request, 'service_id', None)
    car_id = get_param(request,'c_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    car = None
    make = None
    odo = None
    vendor = None
    size = None
    car_bike = None
    if car_id:
        carObj = Car.objects.filter(id=car_id)
       
        if len(carObj):
            carObj = carObj[0]
            size = carObj.size
            car_bike = carObj.car_bike
            print size
    if catg_id:
        cleanObj = VASCatName.objects.filter(id=catg_id)
    
        if len(cleanObj):
            cleanObj = cleanObj[0]
            category = cleanObj.category
            print category

    
    if category:
        if size:
            CleanCatObjs = VASCategoryServices.objects.filter(category = category,car_cat = size, car_bike = car_bike).order_by('priority')
            for service in CleanCatObjs:
                obj['result'].append({
                        'id':service.id
                        ,'vendor':service.vendor          
                        ,'category':service.category        
                        ,'car_cat':service.car_cat         
                        ,'service':service.service         
                        ,'price_labour':service.price_labour
                        ,'price_parts':service.price_parts     
                        ,'total_price':service.price_total     
                        ,'description':service.description  
                        ,'doorstep':service.doorstep
                        ,'discount':service.discount
                        ,'rating':service.rating          
                        ,'reviews':service.reviews   
                        ,'car_bike': service.car_bike
                        ,'priority':service.priority
                              } )
                      
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

#add views before this
#below has to be the last view - i have spoken

from dataEntry import runentry
from dataEntry.carTrie import carsTrie
from pytrie import SortedStringTrie as trie

def fetch_car_autocomplete(request):
    car_query = get_param(request, 'query', None)
    car_list = []
    obj = {}
    obj['status'] = False
    obj['result'] =[]
    import re
    regex = re.compile('^HTTP_')
    headerDict = dict((regex.sub('', header), value) for (header, value) in request.META.items() if header.startswith('HTTP_'))
    print headerDict

    def getMatchList(word):

        res = []
        car_list = carTrieObj.items(word)
        for match in car_list:
            res = res + match[1]
        return res
    if len(car_query):
        words = car_query.split(' ')
        if len(words) > 1 :
            matchArray = []
            res = []
            index = 0
            for word in words:
                matchArray.append(getMatchList(word.lower()))
                # print word
            # print matchArray
            res = matchArray[0]
            for matchRow in matchArray:
                res = list(set(res).intersection(matchRow))
            obj['result'] = res
        else :
            obj['result'] = getMatchList(car_query.lower())
            # car_list = carTrieObj.items(car_query.lower())
            # for match in car_list:
            #     obj['result'] = obj['result'] + match[1]
        obj['status'] = True

    obj['result'] = getCarObjFromName(obj['result'])
    obj['counter'] = 1
    obj['msg'] = "Success"
    obj['headers'] = headerDict

    return HttpResponse(json.dumps(obj), content_type='application/json')

@csrf_exempt
def place_emergency_order(request):
    # print 'p'
    android_flag = get_param(request, 'android', None)
    loc = get_param(request, 'loc', None)


    if (request.user and request.user.is_authenticated()) or random_req_auth(request) or (loc == 'mobile'):
        # email = request.user.email
        name = get_param(request, 'name', None)
        number = get_param(request, 'number', None)
        car_reg_number = get_param(request, 'reg_no', None)
        pick_obj = get_param(request, 'pick', None)
        # drop_obj = get_param(request, 'drop', None)
        order_list = get_param(request, 'order_list', None)
        car_name = get_param(request, 'car_name', None)
        # car_id = get_param(request, 'car_id', None)

        # obj_pick = json.loads(pick_obj)
        pick_obj = ast.literal_eval(pick_obj)
        # drop_obj = ast.literal_eval(drop_obj)
        # pick_obj = ast.literal_eval(pick_obj)
        # print pick_obj
        # pick_obj = json.loads(pick_obj)

        # print pick_obj

        # for key in pick_obj.keys():
        #     print key
        # print json.loads(drop_obj)
        order_list = json.loads(order_list)

        print order_list
        print pick_obj
        # print drop_obj

        # tran_len = len(Transaction.objects.all())
        booking_id = 1
        # if tran_len > 0:
        #     tran = Transaction.objects.all().aggregate(Max('booking_id'))
        #     booking_id = tran['booking_id'] + 1



        tran_len = len(Transactions.objects.all())
        if tran_len > 0:
            tran = Transactions.objects.all().aggregate(Max('booking_id'))
            booking_id = int(tran['booking_id__max'] + 1)

        html_list = []
        html_list.append('<b>Booking ID #')
        html_list.append(    booking_id)
        html_list.append(            '</b><br><p>Hi ')
        html_list.append(name)
        html_list.append(',<br> Your ClickGarage emergency service booking has been confirmed.  ')
        html_list.append(            '. If further assistance is needed, please contact us on 09717353148 and quote your booking confirmation number #')
        html_list.append(            booking_id)
        html_list.append(            '.</p>')
        # html_script = ' '.join(str(x) for x in html_list)
        html_list.append('<p>The selected services are for ')
        html_list.append(car_name)
        html_list.append(' (')
        html_list.append(car_reg_number)
        html_list.append(') ')
        html_list.append(':</p>')

        transList = []

        for order in order_list:
            print order
            ts = order['ts']
            service = 'emergency'
            service = service.lower()
            service_id = order['service_id']

            listItem = {}
            listItem['service'] = service
            listItem['service_id'] = service_id
            listItem['ts'] = ts
            listItem['status'] = True
            html_list.append('<div> <span>')
            html_list.append(service_id)
            html_list.append('</span></div>')

            if not android_flag and (request.user and request.user.is_authenticated()):
                ac_vi.updateCart(request.user, ts+'*emergency', 'delete', '', None)
            transList.append(listItem)


        html_list.append('<div> <span>Pickup Address : </span><span>')
        # html_list.append(pick_obj['street'])
        if 'street' in pick_obj:
            # html_list.append('</span><span> street : ')
            html_list.append(pick_obj['street'])
        if 'locality' in pick_obj:
            html_list.append(pick_obj['locality'])
        html_list.append('</span><span> City : ')
        html_list.append(pick_obj['city'])
        if 'pincode' in pick_obj:
            html_list.append('</span><span> Pincode : ')
            html_list.append(pick_obj['pincode'])
        html_list.append('</span></div>')

        html_list.append('<div><span> Contact No. : ')
        html_list.append(str(number))
        html_list.append('</span></div>')

        userID = None
        email = None
        is_guest = False
        if request.user.is_authenticated():
            userID = request.user.id
            email = request.user.email
        else:
            usr = CGUser.objects.filter(is_staff=True)
            email = get_param(request, 'email', None)
            if len(usr):
                usr = usr[0]
                userID = usr.id
                is_guest = True
                if not email:
                    email = usr.email

        if userID:
            tt = Transactions(
                booking_id      = booking_id,
                trans_timestamp = time.time(),
                cust_id         = userID,
                cust_name       = name,
                cust_brand      = '',
                cust_carname    = car_name,
                cust_number     = number,
                cust_carnumber  = car_reg_number,
                cust_email      = email,

                cust_pickup_add = pick_obj,
                cust_drop_add   = {},

                service_items   = transList,

                price_total     = '',

                date_booking    = pick_obj['date'],
                time_booking    = pick_obj['time'],
                amount_paid     = '',
                status          = '',
                comments        = ''
            )
            tt.save()

            html_script = ' '.join(str(x) for x in html_list)
            mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
            obj = {}
            obj['status'] = True
            obj['result'] = pick_obj
            return HttpResponse(json.dumps(obj), content_type='application/json')
        else:
            obj = {}
            obj['status'] = True
            obj['result'] = 'Failed to find a staff user. Guest transaction failed'
            return HttpResponse(json.dumps(obj), content_type='application/json')

    else:
        redirect('/loginPage/')


@csrf_exempt
def request_quote(request):

    name = get_param(request, 'name', None)
    number = get_param(request, 'number', None)
    category = get_param(request, 'category', None)
    service = get_param(request, 'service', None)

    # if (doorstep_counter==1):
    #     mviews.send_booking_final_doorstep(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
    # else:
    #     mviews.send_booking_final_pick(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)

    resp = {}
    obj = {'name':name, 'number':number, 'category':category, 'service':service  }
    mviews.send_adwords_mail(name,number,category,service)
    resp['status'] = True
    resp['result'] = obj
    return HttpResponse(json.dumps(resp), content_type='application/json')


@csrf_exempt
def place_order(request):

    # print 'p'
    android_flag = get_param(request, 'android', None)
    loc = get_param(request, 'loc', None)

    if (request.user and request.user.is_authenticated()) or random_req_auth(request) or (loc == 'mobile'):
        name = get_param(request, 'name', None)
        number = get_param(request, 'number', None)
        car_reg_number = get_param(request, 'reg_no', '--')
        pick_obj = get_param(request, 'pick', None)
        drop_obj = get_param(request, 'drop', None)
        order_list = get_param(request, 'order_list', None)
        car_name = get_param(request, 'car_name', None)
        coupon_data = get_param(request, 'global_coupon', None)
        s_coupon = get_param(request, 'single_coupon', None)



        #get car_bike
        carObj = []
        carObj = Car.objects.filter(complete_vehicle_name=car_name)
        carObj = carObj[0]
        car_bike = carObj.car_bike

        print car_bike

        print coupon_data
        # car_id = get_param(request, 'car_id', None)
        doorstep_counter = 0
        # obj_pick = json.loads(pick_obj)
        # pick_obj = ast.literal_eval(pick_obj)
        print 'po',pick_obj
        if pick_obj and (isinstance(pick_obj,str) or isinstance(pick_obj,unicode)):
            try:
                pick_obj = ast.literal_eval(pick_obj)
            except ValueError:
                import traceback
                traceback.print_exc()

                pick_obj = None

        if drop_obj and (isinstance(drop_obj,str) or isinstance(drop_obj,unicode)):
            try:
                drop_obj = ast.literal_eval(drop_obj)
            except ValueError:
                drop_obj = None

                
        # pick_obj = ast.literal_eval(pick_obj)
        # print pick_obj
        # pick_obj = json.loads(pick_obj)

        # print pick_obj

        # for key in pick_obj.keys():
        #     print key
        # print json.loads(drop_obj)
        import json
        order_list = json.loads(order_list)

        print order_list
        print '*'*100
        print pick_obj
        print '*' * 100
        print drop_obj
        # tran_len = len(Transaction.objects.all())
        booking_id = 1
        # if tran_len > 0:
        #     tran = Transaction.objects.all().aggregate(Max('booking_id'))
        #     booking_id = tran['booking_id'] + 1



        tran_len = len(Transactions.objects.all())
        if tran_len > 0:
            tran = Transactions.objects.all().aggregate(Max('booking_id'))
            booking_id = int(tran['booking_id__max'] + 1)

        html_list = []
        html_list.append('<b>Booking ID #')
        html_list.append(    booking_id)
        html_list.append(            '</b><br>Name: ')
        html_list.append(name)
        html_list.append('<br> Time :')
        html_list.append(pick_obj['time'])
        html_list.append(            '<br> Date :')
        html_list.append(            pick_obj['date'])
        # html_list.append(            '. If further assistance is needed, please contact us on 09717353148 and quote your booking confirmation number #')
        # html_list.append(            booking_id)
        # html_list.append(            '.</p>')
        # html_script = ' '.join(str(x) for x in html_list)
        html_list.append('<br>Vehicle :')
        html_list.append(car_name)
        html_list.append('<br> Registration Number : ')
        html_list.append(car_reg_number)
        # html_list.append(') ')
        # html_list.append(':</p>')

        transList = []
        alist = []
        custom_req = ''

        for order in order_list:
            print order
            ts = order['ts']
            service = order['service']
            service = service.lower()
            service_id = order['service_id']

            listItem = {}
            listItem['service'] = service
            listItem['service_id'] = service_id
            listItem['ts'] = ts
            listItem['status'] = True
            if service == 'servicing':
                doorstep_counter = 2
                serviceDetail = ServiceDealerCat.objects.filter(id=service_id)
                serviceDetailNew = ServiceDealerCatNew.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)
                    html_list.append('<div>')
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        'odometer':serviceDetail.odometer,
                        'dealer_cat':serviceDetail.dealer_category,
                        'parts_list':serviceDetail.part_replacement,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'wa_price':serviceDetail.wheel_alignment,
                        'wb_price':serviceDetail.wheel_balancing,
                        # 'wa_wb_present':serviceDetail.WA_WB_Inc,
                        'dealer_details':serviceDetail.detail_dealers,
                        'year':serviceDetail.year,
                        'total_price':total_price,
                        'status':True,
                        'ts':ts
                    }


                    listItem['served_data'] = item
                    html_list.append('<span> regular servicing </span>')
                    html_list.append('<span> due at : ')
                    html_list.append(item['odometer'])
                    html_list.append(' / ')
                    html_list.append(item['year'])
                    html_list.append('</span>')

                    html_list.append('<span> dealer : ')
                    html_list.append(item['dealer_cat'])
                    html_list.append('</span>')

                    html_list.append('<span> price : ')
                    html_list.append(total_price)
                    html_list.append('</span>')

                    html_list.append('</div>')

                elif len(serviceDetailNew):
                    serviceDetail = serviceDetailNew[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)
                    html_list.append('<div>')
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        'type_service':serviceDetail.type_service,
                        'dealer_cat':serviceDetail.dealer_category,
                        'parts_list':serviceDetail.part_replacement,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'wa_price':serviceDetail.wheel_alignment,
                        'wb_price':serviceDetail.wheel_balancing,
                        # 'wa_wb_present':serviceDetail.WA_WB_Inc,
                        'dealer_details':serviceDetail.detail_dealers,
                        # 'year':serviceDetail.year,
                        'total_price':total_price,
                        'status':True,
                        'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Servicing </span>')
                    html_list.append('<br><span> Type : ')
                    html_list.append(item['type_service'])
                    html_list.append('</span>')

                    html_list.append('<br><span> dealer : ')
                    html_list.append(item['dealer_cat'])
                    html_list.append('</span>')
                        # html_list.append('<span> price : ')
                    # html_list.append(total_price)
                    # html_list.append('</span><br/>')
                    # tookan integration start

                    # car_bike_type = serviceDetail.car_bike
                    category = "Servicing/ Repair"
                    if car_bike == "Car":
                        template = "Servicing_Car"
                        servicing_meta_data = [{"label": "Car_Name", "data": serviceDetail.carname},
                                               {"label": "Labour_Estimate", "data": float(serviceDetail.price_labour)},
                                               {"label": "Parts_Estimate", "data": float(serviceDetail.price_parts)}]

                    elif car_bike == "Bike":
                        template = "Servicing_Bike"
                        servicing_meta_data = [{"label": "Bike_Name", "data": serviceDetail.carname},
                                               {"label": "Labour_Estimate", "data": float(serviceDetail.price_labour)},
                                               {"label": "Parts_Estimate", "data": float(serviceDetail.price_parts)}]

                        # tookan integration end

                    additional = None
                    if request.user and request.user.is_authenticated():
                        if ts in request.user.uc_cart:
                            this_order = request.user.uc_cart[ts]
                            if 'additional_data' in this_order:
                                additional = this_order['additional_data']
                    if (loc == 'mobile') or android_flag:
                        if 'additional_data' in order:
                            additional = order['additional_data']
                            additional = json.loads(additional)

                    if additional:
                        addStr = '<span> Additional Features : '
                        custAddStr = ''
                        listItem['served_data']['additional'] = additional
                        for feat, status in additional.iteritems():
                            print 'ai',feat,status
                            if status:
                                if feat == 'Custom Requests':
                                    custAddStr = '<br/><span> Custom Requests : %s </span>' %(status)
                                    custom_req = status
                                elif feat == 'Selected Authorized':
                                    d_name = ''
                                    d_address = ''
                                    if 'name' in status:
                                        d_name = status['name']
                                    if 'address' in status:
                                        d_address = status['address']
                                    custAddStr = '<br/><span> Authorized Dealer Selected : %s (%s) </span>' %(d_name,d_address)
                                else:
                                    addStr = '%s [%s] - ' %(addStr,feat)
                                    alist.append(feat)
                        addStr = addStr + '</span>' + custAddStr
                        html_list.append(addStr)

                    if alist:
                        category += ' ('+','.join(alist)+')'

                    if custom_req:
                        category += ' Custom : '+custom_req

                    html_list.append('</div>')

            elif service == 'cleaning':
                serviceDetail = CleaningCategoryServices.objects.filter(id=service_id)
                if (doorstep_counter<2):
                    doorstep_counter = 1
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    html_list.append('<div>')

                    item = {
                        'id':serviceDetail.id,
                        'category':serviceDetail.category,
                        'car_cat':serviceDetail.car_cat,
                        'service':serviceDetail.service,
                        'vendor':serviceDetail.vendor,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'total_price':serviceDetail.price_total,
                        # 'total_price':total_price,
                        'description':serviceDetail.description,
                        'status':True,
                        'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Cleaning </span>')
                    html_list.append('<br><span> Category : ')
                    html_list.append(item['category'])
                    html_list.append('</span>')

                    html_list.append('<br><span>')
                    html_list.append(item['vendor'])
                    html_list.append(' - ')
                    html_list.append(item['service'])
                    html_list.append('</span>')

                    # html_list.append('<span> price : ')
                    # html_list.append(total_price)
                    # html_list.append('</span>')

                    # tookan integration start vas

                    category = "Value Added Service"
                    template = "VAS_Car"
                    servicing_meta_data = [{"label": "Car_Name", "data": car_name},
                                           {"label": "Service_Estimate", "data": float(serviceDetail.price_total)},
                                           {"label": "Service_Requested", "data": serviceDetail.service}]

                    # tookan integration end

                    html_list.append('</div>')
            elif service == 'vas':
                serviceDetail = VASCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    html_list.append('<div>')

                    item = {
                        'id':serviceDetail.id,
                        'category':serviceDetail.category,
                        'car_cat':serviceDetail.car_cat,
                        'service':serviceDetail.service,
                        'vendor':serviceDetail.vendor,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'total_price':serviceDetail.price_total,
                        # 'total_price':total_price,
                        'description':serviceDetail.description,
                        'status':True,
                        'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Vas </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(item['category'])
                    html_list.append('</span>')

                    html_list.append('<span>')
                    html_list.append(item['vendor'])
                    html_list.append(' - ')
                    html_list.append(item['service'])
                    html_list.append('</span>')

                    html_list.append('<span> price : ')
                    html_list.append(total_price)
                    html_list.append('</span>')

                    html_list.append('</div>')

            elif service == 'windshield':
                serviceDetail = WindShieldServiceDetails.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    # if len(serviceDetail.price_parts):
                    #     total_price = total_price+ float(serviceDetail.price_parts)
                    # if len(serviceDetail.price_labour):
                    #     total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    html_list.append('<div>')

                    item = {
                        'id':serviceDetail.id
                                ,'vendor'         :serviceDetail.vendor
                                ,'brand'          :serviceDetail.brand
                                ,'carname'        :serviceDetail.carname
                                ,'ws_type'        :serviceDetail.ws_type
                                ,'ws_subtype'     :serviceDetail.ws_subtype
                                ,'colour'         :serviceDetail.colour
                                ,'price_ws'       :serviceDetail.price_ws
                                ,'price_sealant'  :serviceDetail.price_sealant
                                ,'price_labour'   :serviceDetail.price_labour
                                ,'price_insurance':serviceDetail.price_insurance
                                ,'price_total'   :serviceDetail.price_total
                                ,'city'           :serviceDetail.city
                                ,'description':serviceDetail.description
                                ,'status':True
                                ,'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Windshield </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(item['ws_subtype'])
                    html_list.append('&nbsp;(')
                    html_list.append(item['ws_type'])
                    html_list.append('&nbsp;)')
                    html_list.append('</span>')

                    html_list.append('<span>')
                    html_list.append(item['vendor'])
                    html_list.append(' - ')
                    html_list.append(item['colour'])
                    html_list.append('</span>')

                    html_list.append('<span> price : ')
                    html_list.append(item['price_total'])
                    html_list.append('</span>')

                    html_list.append('</div>')
            elif service == 'repair':

                if len(service_id) and (service_id in repair_map):
                    html_list.append('<div>')
                    html_list.append('<span> Repairs </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(repair_map[service_id]['name'])
                    html_list.append('</span>')

                    additional = None
                    if request.user and request.user.is_authenticated():
                        if ts in request.user.uc_cart:
                            this_order = request.user.uc_cart[ts]
                            if 'additional_data' in this_order:
                                additional = this_order['additional_data']
                    if (loc == 'mobile') or android_flag:
                        if 'additional_data' in order:
                            additional = order['additional_data']
                            additional = json.loads(additional)
                    if additional:
                        addStr = '<span> Repair Queries : '
                        custAddStr = ''
                        listItem['served_data'] = {}
                        listItem['served_data']['additional'] = additional
                        for feat, status in additional.iteritems():
                            print
                            if status:
                                if feat == 'Custom Requests':
                                    custAddStr = '<br/><span> Custom Requests : %s </span>' %(status)
                                    custom_req = status
                                elif feat == 'Damage Type':
                                    custAddStr = '<br/><span> Damage Type : %s </span>' %(status)
                                    custom_req = status
                                # elif feat == 'Selected Authorized':
                                #     d_name = ''
                                #     d_address = ''
                                #     if 'name' in status:
                                #         d_name = status['name']
                                #     if 'address' in status:
                                #         d_address = status['address']
                                #     custAddStr = '<br/><span> Authorized Dealer Selected : %s (%s) </span>' %(d_name,d_address)
                                else:
                                    addStr = '%s [%s] - ' %(addStr,feat)
                                    alist.append(feat)
                        addStr = addStr + '</span>' + custAddStr

                        html_list.append(addStr)

                    html_list.append('</div>')

                    category = "Repair"
                    if car_bike == "Car":
                        template = "Servicing_Car"
                        servicing_meta_data = [{"label": "Car_Name", "data": car_name}]

                    elif car_bike == "Bike":
                        template = "Servicing_Bike"
                        servicing_meta_data = [{"label": "Bike_Name", "data": car_name}]
                    if alist:
                        category += ' ('+','.join(alist)+')'

                    if custom_req:
                        category += ' Custom : '+custom_req


            if (not android_flag) and (request.user and request.user.is_authenticated()):
                ac_vi.updateCart(request.user, str(ts)+'*', 'delete', '', None)
            transList.append(listItem)


        html_list.append('<div> <span>Pickup Address : </span><span>')

        # html_list.append(pick_obj['street'])

        # if 'landmark' in pick_obj:
        #     html_list.append('</span><span> Landmark : ')
        #     html_list.append(pick_obj['landmark'])


        if 'street' in pick_obj:
            html_list.append(pick_obj['street'])

        if 'locality' in pick_obj:
            html_list.append(pick_obj['locality'])

        html_list.append('</span><span> City : ')
        html_list.append(pick_obj['city'])
        if 'pincode' in pick_obj:
            html_list.append('</span><span> Pincode : ')
            html_list.append(pick_obj['pincode'])
        html_list.append('</span></div>')

        if coupon_data and len(coupon_data) and None:
            coupon_json = json.loads(coupon_data)
            if isinstance(coupon_json, dict):
                html_list.append('<div><span> Coupons. : ')
                for coupon in coupon_json.keys():
                    html_list.append(coupon)
                    html_list.append(' [')
                    html_list.append(coupon_json[coupon])
                    html_list.append('] ')
                html_list.append('</span></div>')
        if s_coupon and len(s_coupon):
            coupon_json = json.loads(urllib.unquote(s_coupon))
            if isinstance(coupon_json, dict):
                html_list.append('<div><span>Single Coupon. : ')
                for coupon in coupon_json.keys():
                    html_list.append(coupon)
                    html_list.append(' [')
                    html_list.append(coupon_json[coupon])
                    html_list.append('] ')
                html_list.append('</span></div>')

        html_list.append('<div><span> Contact No. : ')
        html_list.append(str(number))
        html_list.append('</span></div>')

        # html_list.append('<div> <span>Drop Address : </span><span>')
        # html_list.append(drop_obj['street'])
        # if 'landmark' in pick_obj:
        #     html_list.append('</span><span> Landmark : ')
        #     html_list.append(drop_obj['landmark'])
        # html_list.append('</span><span> City : ')
        # html_list.append(drop_obj['city'])
        #
        # if 'pincode' in drop_obj:
        #     html_list.append('</span><span> Pincode : ')
        #     html_list.append(drop_obj['pincode'])
        # html_list.append('</span></div>')


        userID = None
        email = None
        is_guest = False
        if request.user.is_authenticated():
            userID = request.user.id
            email = request.user.email
            if not email:
                email = get_param(request, 'email', None)
            if not email:
                usr = CGUser.objects.filter(is_staff=True)
                if len(usr):
                    email = usr[0].email

        else:
            usr = CGUser.objects.filter(is_staff=True)
            email = get_param(request, 'email', None)
            print 'email',email

            if len(usr):
                usr = usr[0]
                userID = usr.id
                is_guest = True
                if not email:
                    email = usr.email
        if userID:
            tt = Transactions(
                booking_id      = booking_id,
                trans_timestamp = time.time(),
                cust_id         = userID,
                cust_name       = name,
                cust_brand      = '',
                cust_carname    = car_name,
                cust_number     = number,
                cust_carnumber  = car_reg_number,
                cust_email      = email,

                cust_pickup_add = pick_obj,
                cust_drop_add   = drop_obj,

                service_items   = transList,
                is_guest        = is_guest,
                price_total     = '',

                date_booking    = pick_obj['date'],
                time_booking    = pick_obj['time'],
                amount_paid     = '',
                status          = '',
                comments        = ''
            )
            tt.save()

            html_script = ' '.join(str(x) for x in html_list)

            if (doorstep_counter==1):
                mviews.send_booking_final_doorstep(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
            else:
                mviews.send_booking_final_pick(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
            obj = {}
            obj['status'] = True
            obj['result'] = pick_obj

            # Tookan Integration Start
            if 1:
                from dateutil import parser as dt_parser
                customer_address = ', '.join(
                    [pick_obj.get('street', ''), pick_obj.get('landmark', ''), pick_obj.get('city', '')])
                start_time = pick_obj.get('date') + ' ' + pick_obj.get('time').split(' - ')[0]
                print 'st0', start_time

                # start_time = my_date_parser(start_time)
                start_time = dt_parser.parse(start_time)

                print 'st', start_time.month, start_time.year, start_time.day
                start_time = start_time.strftime('%m/%d/%Y %I:%M %p')
                end_time = pick_obj.get('date') + ' ' + pick_obj.get('time').split(' - ')[1]
                print 'et0', end_time
                end_time = dt_parser.parse(end_time)
                print 'et', end_time.month, end_time.year, end_time.day
                end_time = end_time.strftime('%m/%d/%Y %I:%M %p')
                print start_time
                print end_time

                # a = {"label": "Servicing_Labour", "data": "100"}
                values = {
                    "customer_email": email,
                    "order_id": str(booking_id),
                    "customer_username": name,
                    "customer_phone": number,
                    "customer_address": customer_address,
                    "latitude": "",
                    "longitude": "",
                    "job_description": category,
                    "job_pickup_datetime": start_time,
                    "job_delivery_datetime": end_time,
                    "has_pickup": "0",
                    "has_delivery": "0",
                    "layout_type": "1",
                    "tracking_link": 1,
                    "timezone": "-330",
                    "team_id":"12376",
                    "custom_field_template": template,
                    "meta_data": servicing_meta_data,
                    "api_key": "a18332760b2847468d7b569f88ff0fce345c32a0580b095657c81890251fc0a0",
                    "team_id": "255",
                    "auto_assignment": "0",
                    "fleet_id": "636",
                    "ref_images": ["https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/8b0df50f-a54b-4a7b-9ef6-c31d66aff1f1.jpg"                                   ],
                    "notify": 1,
                    # "tags": "tag1,tag2",
                    "geofence": 0
                }

                print values

                headers = {
                    'Content-type': 'application/json'
                }

                # import requests
                url = 'https://api.tookanapp.com/v2/create_task'
                # import json
                req = requests.post(url, data=json.dumps(values), headers=headers, verify= False, timeout = 10)

                # req = Request(url, data=json.dumps(values), headers=headers)
                # obj['took'] = urlopen(req).read()


                obj['took'] = req.json() if req.status_code == 200 else req.content
                # obj['took'] = res_body.json() if res_body.status_code == 200 else res_body.content
                # Tookan Integration End

            return HttpResponse(json.dumps(obj), content_type='application/json')
        else:
            obj = {}
            obj['status'] = True
            obj['result'] = 'Failed to find a staff user. Guest transaction failed'
            return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        redirect('/loginPage/')

def insert_tran(request):
    cust_id         = get_param(request,'cust_id',None)   
    trans_timestamp = datetime.datetime.now()
    cust_name       = get_param(request,'cust_name',None)   
    cust_brand      = get_param(request,'cust_brand',None)   
    cust_carname    = get_param(request,'cust_carname',None)
    cust_number     = get_param(request,'cust_number',None)   
    cust_email      = get_param(request,'cust_email',None)   
    cust_pickup_add = get_param(request,'cust_pickup_add',None)   
    cust_drop_add   = get_param(request,'cust_drop_add',None)   
    booking_vendor  = get_param(request,'booking_vendor',None)   
    booking_cat     = get_param(request,'booking_cat',None)   
    booking_type    = get_param(request,'booking_type',None)   
    price_labour    = get_param(request,'price_labour',None)   
    price_parts     = get_param(request,'price_parts',None)   
    price_total     = get_param(request,'price_total',None)   
    date_booking    = get_param(request,'date_booking',None)   
    time_booking    = get_param(request,'time_booking',None)   
    amount_paid     = get_param(request,'amount_paid',None)   
    status          = get_param(request,'status',None)   
    comments        = get_param(request,'comments',None)   

    tran_len = len(Transactions.objects.all())
    if tran_len > 0:
        tran = Transactions.objects.all().aggregate(Max('booking_id'))
        booking_id = int(tran['booking_id']) + 1
    else:
        booking_id = 1
    cc = ServiceDealerCat(
        booking_id       = booking_id
        ,trans_timestamp = trans_timestamp
        ,cust_id         = cust_id
        ,cust_name       = cust_name       
        ,cust_brand      = cust_brand      
        ,cust_carname    = cust_carname    
        ,cust_number     = cust_number     
        ,cust_email      = cust_email      
        ,cust_pickup_add = cust_pickup_add 
        ,cust_drop_add   = cust_drop_add   
        ,booking_vendor  = booking_vendor  
        ,booking_cat     = booking_cat     
        ,booking_type    = booking_type    
        ,price_labour    = price_labour    
        ,price_parts     = price_parts     
        ,price_total     = price_total     
        ,date_booking    = date_booking    
        ,time_booking    = time_booking    
        ,amount_paid     = amount_paid     
        ,status          = status          
        ,comments        = comments ) 

#run this just once if possible

carTrieObj = trie(carsTrie)
  
def fetch_car_booking(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    cust_id = None
    stype = get_param(request,'type','confirmed')

    def pushObjToList(mongoArray):
        arry = []
        for trans in mongoArray:
            arry.append({
                            'tran_id'          :trans.id
                            ,'booking_id'       :trans.booking_id
                            ,'trans_timestamp'  :trans.trans_timestamp
                            ,'cust_id'          :trans.cust_id
                            ,'cust_name'        :trans.cust_name
                            ,'cust_brand'       :trans.cust_brand
                            ,'cust_carname'     :trans.cust_carname
                            ,'cust_carnumber'   :trans.cust_carnumber
                            ,'cust_number'      :trans.cust_number
                            ,'cust_email'       :trans.cust_email
                            ,'cust_pickup_add'  :trans.cust_pickup_add
                            ,'cust_drop_add'    :trans.cust_drop_add
                            ,'service_items'    :trans.service_items
                            ,'price_total'      :trans.price_total
                            ,'date_booking'     :trans.date_booking
                            ,'time_booking'     :trans.time_booking
                            ,'amount_paid'      :trans.amount_paid
                            ,'status'           :trans.status
                            ,'comments'         :trans.comments})
        return arry

    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        cust_id = request.user.id

    if cust_id:
        if (stype == 'confirmed') or (stype == 'all'):
            tranObjs = Transactions.objects.filter(cust_id=cust_id).exclude(status='Cancelled').exclude(status='Complete').order_by('-booking_id')
            obj['result']['confirmed'] = pushObjToList(tranObjs)
        if (stype == 'cancelled') or (stype == 'all'):
            tranObjs = Transactions.objects.filter(cust_id=cust_id, status='Cancelled').order_by('-booking_id')
            obj['result']['cancelled'] = pushObjToList(tranObjs)
        if (stype == 'completed') or (stype == 'all'):
            tranObjs = Transactions.objects.filter(cust_id=cust_id, status='Complete').order_by('-booking_id')
            obj['result']['completed'] = pushObjToList(tranObjs)


        # for trans in tranObjs:
        #     obj['result']['confirmed'].append({
        #                     'tran_id'          :trans.id
        #                     ,'booking_id'       :trans.booking_id
        #                     ,'trans_timestamp'  :trans.trans_timestamp
        #                     ,'cust_id'          :trans.cust_id
        #                     ,'cust_name'        :trans.cust_name
        #                     ,'cust_brand'       :trans.cust_brand
        #                     ,'cust_carname'     :trans.cust_carname
        #                     ,'cust_carnumber'   :trans.cust_carnumber
        #                     ,'cust_number'      :trans.cust_number
        #                     ,'cust_email'       :trans.cust_email
        #                     ,'cust_pickup_add'  :trans.cust_pickup_add
        #                     ,'cust_drop_add'    :trans.cust_drop_add
        #                     ,'service_items'    :trans.service_items
        #                     ,'price_total'      :trans.price_total
        #                     ,'date_booking'     :trans.date_booking
        #                     ,'time_booking'     :trans.time_booking
        #                     ,'amount_paid'      :trans.amount_paid
        #                     ,'status'           :trans.status
        #                     ,'comments'         :trans.comments})
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_complete(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    cust_id = None

    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        cust_id         = request.user.id

    if cust_id:
        tranObjs = Transactions.objects.filter(cust_id=cust_id, status = 'Complete').order_by('-booking_id')
            #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
        for trans in tranObjs:
            obj['result'].append({
                            'tran_id'          :trans.id
                            ,'booking_id'       :trans.booking_id
                            ,'trans_timestamp'  :trans.trans_timestamp
                            ,'cust_id'          :trans.cust_id
                            ,'cust_name'        :trans.cust_name
                            ,'cust_brand'       :trans.cust_brand
                            ,'cust_carname'     :trans.cust_carname
                            ,'cust_carnumber'   :trans.cust_carnumber
                            ,'cust_number'      :trans.cust_number
                            ,'cust_email'       :trans.cust_email
                            ,'cust_pickup_add'  :trans.cust_pickup_add
                            ,'cust_drop_add'    :trans.cust_drop_add
                            ,'service_items'    :trans.service_items
                            ,'price_total'      :trans.price_total
                            ,'date_booking'     :trans.date_booking
                            ,'time_booking'     :trans.time_booking
                            ,'amount_paid'      :trans.amount_paid
                            ,'status'           :trans.status
                            ,'comments'         :trans.comments} )
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')



def fetch_car_cancelled(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    cust_id = None

    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        cust_id         = request.user.id

    if cust_id:
        tranObjs = Transactions.objects.filter(cust_id=cust_id, status = 'Cancelled').order_by('-booking_id')
            #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
        for trans in tranObjs:
            obj['result'].append({
                            'tran_id'          :trans.id
                            ,'booking_id'       :trans.booking_id            
                            ,'trans_timestamp'  :trans.trans_timestamp       
                            ,'cust_id'          :trans.cust_id          
                            ,'cust_name'        :trans.cust_name             
                            ,'cust_brand'       :trans.cust_brand            
                            ,'cust_carname'     :trans.cust_carname          
                            ,'cust_carnumber'   :trans.cust_carnumber        
                            ,'cust_number'      :trans.cust_number           
                            ,'cust_email'       :trans.cust_email            
                            ,'cust_pickup_add'  :trans.cust_pickup_add       
                            ,'cust_drop_add'    :trans.cust_drop_add         
                            ,'service_items'    :trans.service_items         
                            ,'price_total'      :trans.price_total           
                            ,'date_booking'     :trans.date_booking          
                            ,'time_booking'     :trans.time_booking          
                            ,'amount_paid'      :trans.amount_paid           
                            ,'status'           :trans.status                
                            ,'comments'         :trans.comments} )
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')

    
def cancel_booking(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    useremail = None
    username = None
    booking_id = None
    r_id = get_param(request, 'r_id', None)
    if (r_id == tempSecretKey) or random_req_auth(request) or (request.user and request.user.is_authenticated()):
        # cust_id         = request.user.id
        # email           = request.user.email
        tran_id         = get_param(request,'tran_id',None)

        obj['cancelled_id'] = tran_id
        tranObjs = Transactions.objects.filter(id =tran_id).exclude(status="Cancelled")
        for tran in tranObjs:
            useremail = tran.cust_email
            username  = tran.cust_name
            booking_id = tran.booking_id
            tran.status = "Cancelled"
            tran.save()
            obj['result'] = {}
            obj['result']['cancelled_id'] = tran_id
            obj['status'] = True
            obj['counter'] = 1
            obj['msg'] = "Success"
#    mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
        mviews.send_cancel_final(username,useremail,booking_id)
    return HttpResponse(json.dumps(obj), content_type='application/json')

        # useremail = tran.cust_email
        # username  = tran.cust_name
        # booking_id = tran.booking_id
        # mviews.send_cancel_final(username,useremail,booking_id)


# def fetch_all_booking(request):
#     obj = {}
#     obj['status'] = False
#     obj['result'] = []
#     cust_id = None
#     # if random_req_auth(request) or (request.user and request.user.is_authenticated()):
#     #     cust_id = request.user.id
#
#
#     tranObjs = Transactions.objects.all()
#             #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
#     for trans in tranObjs:
#         obj['result'].append({
#                             'tran_id'          :trans.id
#                             ,'booking_id'       :trans.booking_id
#                             ,'trans_timestamp'  :trans.trans_timestamp
#                             ,'cust_id'          :trans.cust_id
#                             ,'cust_name'        :trans.cust_name
#                             ,'cust_brand'       :trans.cust_brand
#                             ,'cust_carname'     :trans.cust_carname
#                             ,'cust_carnumber'   :trans.cust_carnumber
#                             ,'cust_number'      :trans.cust_number
#                             ,'cust_email'       :trans.cust_email
#                             ,'cust_pickup_add'  :trans.cust_pickup_add
#                             ,'cust_drop_add'    :trans.cust_drop_add
#                             ,'service_items'    :trans.service_items
#                             ,'price_total'      :trans.price_total
#                             ,'date_booking'     :trans.date_booking
#                             ,'time_booking'     :trans.time_booking
#                             ,'amount_paid'      :trans.amount_paid
#                             ,'status'           :trans.status
#                             ,'comments'         :trans.comments} )
#         obj['status'] = True
#         obj['counter'] = 1
#         obj['msg'] = "Success"
#         return HttpResponse(json.dumps(obj), content_type='application/json')
#     else:
#         return HttpResponse(json.dumps(obj), content_type='application/json')


   # if request.user and request.user.is_authenticated():
   #      cust_id         = request.user.id
   #      email           = request.user.email
   #      tran_id         = get_param(request,'tran_id',None)
   #      item_id         = get_param(request,'item_id',None)
   #
   #  obj['cancelled_id'] = tran_id
   #  tranObjs = Transactions.objects.filter(status = '', id =tran_id)
   #  for tran in tranObjs:
   #      # serviceObj = tran.service_items(status = True , ts =item_id)
   #      listy = tran.service_items
   #      serviceObj = (item for item in tran.service_items if 'ts' in item and item['ts'] == item_id).next()
   #      idx = tran.service_items.index(serviceObj)
   #      serviceObj['status'] = 'Cancelled'
   #      tran.service_items[idx] = serviceObj
   #      tran.save()
   #      # for service in serviceObj:
   #      #     service.status = "Cancelled"
   #      #     tran.save()
   #      #     obj['result'] = {}
   #      #     obj['result']['cancelled_id'] = tran_id
   #      #     obj['status'] = True
   #      #     obj['counter'] = 1
   #      #     obj['msg'] = "Success"
   #
   #      #mviews.send_cancel_email([email,"bookings@clickgarage.in"],tran.cust_name,tran.booking_id)booking_id

    # return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_car_list(request):
    car_bike_id = get_param(request, 'cb_id', None)
    make_id = get_param(request,'m_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []

    car = None
    make = None
    car_bike = None
    CarObjs = Car.objects.filter(car_bike = car_bike_id, make = make_id).order_by('name')
    for caravan in CarObjs:
        obj['result'].append({
                            'id':caravan.id
                            ,'name':caravan.name
                            ,'make':caravan.make
                            ,'car_bike':caravan.car_bike
                            ,'size':caravan.size
                                  } )

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

############################ New Servicing api's #################################

def fetch_car_services_new(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    import re
    regex = re.compile('^HTTP_')
    headerDict = dict((regex.sub('', header), value) for (header, value) in request.META.items() if header.startswith('HTTP_'))
    print headerDict

    if 1 or random_req_auth(request) or (request.user and request.user.is_authenticated()):
        car_id = get_param(request, 'c_id', None)
        car = None
        make = None
        if car_id:
            carObj = Car.objects.filter(id=car_id)

            if len(carObj):
                carObj = carObj[0]
                car_old = carObj.name
                car_bike = carObj.car_bike
                make = carObj.make
                car = make + " " + car_old
                if car:
                    ServiceObjs = ServicingNew.objects.filter(carname = car, brand = make).order_by('priority_service')
                    #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
                    for service in ServiceObjs:
                        obj['result'].append({
                             'id':service.id
                            ,'name':service.name
                            ,'brand':service.brand
                            ,'car_name':service.carname
                            ,'type_service' : service.type_service
                            ,'service_desc' : service.service_desc
                            ,'regular_checks':service.regular_checks

                            ,'parts_replaced':service.part_replacement
                            ,'dealers_list':service.dealer
                    #,'time_reading' : service.year
                        ,'checks_done' : service.regular_checks
                        #,'paid_free' : service.paid_free
                        ,'parts_replaced' : service.part_replacement
                        ,'part_dic':service.part_dic
                        ,'dealer_category' : service.dealer
                        ,'car_bike':car_bike
                        } )
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        obj['headers'] = headerDict
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_servicedetails_new(request):
    service_id = get_param(request, 'service_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    print '-----'
    print request.user
    if 1 or random_req_auth(request) or (request.user and request.user.is_authenticated()):

        car = None
        make = None
        odo = None
        car_2 = None
        type_service = None
        if service_id:
            serviceObj = ServicingNew.objects.filter(id=service_id)
            if len(serviceObj):
                serviceObj = serviceObj[0]
                car = serviceObj.carname
                make = serviceObj.brand
                type_service = serviceObj.type_service
                car_2 = cleanstring(car.replace(make,""))
                print car_2
            carObj = Car.objects.filter(name=car_2)

            if len(carObj):
                carObj = carObj[0]
                car_bike = carObj.car_bike
                print car_bike
                if car:
                    AuthServicedetailObj = ServiceDealerCatNew.objects.filter(carname = car, brand = make, type_service = type_service, dealer_category = 'Authorized').order_by('priority')
                    auth_prices = None
                    if len(AuthServicedetailObj):
                        service = AuthServicedetailObj[0]
                        auth_prices = {
                              'parts_price':service.price_parts,
                              'labour_price':service.price_labour,
                              'vendor':service.dealer_category
                        }

                    ServicedetailObjs = ServiceDealerCatNew.objects.filter(carname = car, brand = make, type_service = type_service).order_by('priority')
                    for service in ServicedetailObjs:
                        obj['result'].append({
                            'id':service.id
                              ,'name':service.name
                              ,'brand':service.brand
                              ,'car':service.carname
                              ,'car_bike':service.car_bike
                              ,'vendor':service.dealer_category
                              ,'parts_list':service.part_replacement
                              ,'parts_price':service.price_parts
                              ,'labour_price':service.price_labour
                              ,'wa_price':service.wheel_alignment
                              ,'wb_price':service.wheel_balancing
                              # ,'wa_wb_present':service.WA_WB_Inc
                              ,'service_desc':service.service_desc
                              ,'dealer_details':service.detail_dealers
                             ,'dry_cleaning': service.dry_cleaning
                             ,'engine_additive': service.engine_additive
                             ,'injector_cleaning': service.injector_cleaning
                             ,'rubbing_polishing': service.rubbing_polishing
                             ,'anti_rust'        : service.anti_rust
                             ,'teflon'           : service.teflon
                             ,'engine_flush'    : service.engine_flush
                             ,'ac_servicing'    : service.ac_servicing
                             ,'ac_disinfection': service.ac_disinfection
                              # ,'car_bike':car_bike
                        ,'type_service':service.type_service
                        ,'part_dic':service.part_dic
                        ,'discount':service.discount
                        ,'priority':service.priority
                        ,'prices':[
                            {
                              'parts_price':service.price_parts,
                              'labour_price':service.price_labour,
                              'vendor':service.dealer_category
                            },
                            auth_prices
                        ]
                     }
                        )


        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_additional_details(request):
    ccdAdditional = request.COOKIES.get('clgacartaddi')
    # print request.COOKIES
    # print ccdAdditional
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        user = request.user
        cart = request.user.uc_cart
        obj['result'] = cart
        obj['status'] = True
    elif ccdAdditional and len(ccdAdditional):
            try:
                ccdaObj = json.loads( urllib.unquote(ccdAdditional) )
                # for ts in ccdaObj:
                    # if ts in cartDict:
                    #     obj = cartDict[ccdaObj]
                for ts in ccdaObj:
                    print ts
                    oppy = {}
                    oppy['additional_data'] = ccdaObj[ts]
                    obj['result'][ts] = oppy
                obj['status'] = True

            except ValueError:
                obj['result'] = None
                obj['status'] = False
                #do something

    return HttpResponse(json.dumps(obj), content_type='application/json')


def fetch_all_booking(request):
    r_id = get_param(request, 'r_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    tranObjs =[]
    # cust_id = None
    # if random_req_auth(request) or (request.user and request.user.is_authenticated()):
    #     cust_id = request.user.id

    # if cust_id:

    if request.user.email in staffmails:
        tranObjs = Transactions.objects.all().order_by('-booking_id')
            #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
    for trans in tranObjs:
            obj['result'].append({
                            'tran_id'          :trans.id
                            ,'booking_id'       :trans.booking_id
                            ,'trans_timestamp'  :trans.trans_timestamp
                            ,'cust_id'          :trans.cust_id
                            ,'cust_name'        :trans.cust_name
                            ,'cust_brand'       :trans.cust_brand
                            ,'cust_carname'     :trans.cust_carname
                            ,'cust_carnumber'   :trans.cust_carnumber
                            ,'cust_number'      :trans.cust_number
                            ,'cust_email'       :trans.cust_email
                            ,'cust_pickup_add'  :trans.cust_pickup_add
                            ,'cust_drop_add'    :trans.cust_drop_add
                            ,'service_items'    :trans.service_items
                            ,'price_total'      :trans.price_total
                            ,'date_booking'     :trans.date_booking
                            ,'time_booking'     :trans.time_booking
                            ,'amount_paid'      :trans.amount_paid
                            ,'status'           :trans.status
                            ,'comments'         :trans.comments} )
            obj['status'] = True
            obj['counter'] = 1
            obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_users(request):
    r_id = get_param(request, 'r_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    tranObjs =[]
    # cust_id = None
    # if random_req_auth(request) or (request.user and request.user.is_authenticated()):
    #     cust_id = request.user.id

    # if cust_id:
    if (r_id == tempSecretKey):
        tranObjs = CGUser.objects.all()
            #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
    for trans in tranObjs:
            obj['result'].append({
                            'id'   :trans.id
                           ,'email':trans.email
                        ,'phone':trans.contact_no,
                        'uname':trans.username,
                'name':trans.first_name
                            # ,'name':trans.name

            } )
            obj['status'] = True
            obj['counter'] = 1
            obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def cancel_booking_new(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    useremail = None
    username = None
    booking_id = None
    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        # cust_id         = request.user.id
        # email           = request.user.email
        tran_id         = get_param(request,'tran_id',None)
        service_ts      = get_param(request,'ts',None)
        obj['cancelled_id'] = tran_id
        tranObjs = Transactions.objects.filter(id =tran_id)
        print len(tranObjs)
        if len(tranObjs):
            tranObj = tranObjs[0]
            useremail = tranObj.cust_email
            username  = tranObj.cust_name
            booking_id = tranObj.booking_id

            try:
                itemCancel = (item for item in tranObj.service_items if 'ts' in item and item['ts'] == service_ts).next()
                idx = tranObj.service_items.index(itemCancel)
                itemCancel['status'] = False
                print itemCancel
                print idx
                tranObj.service_items[idx] = itemCancel
                tranObj.status = "Modified"
                tranObj.save()
                obj['result'] = {}
                obj['result']['cancelled_id'] = tran_id
                obj['status'] = True
                obj['counter'] = 1
                obj['msg'] = "Success"
                mviews.send_cancel_final(username,useremail,booking_id)
            except ValueError:
                print "p"
        return HttpResponse(json.dumps(obj), content_type='application/json')

def order_complete(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    useremail = None
    username = None
    userphone = None
    booking_id = None
    tran_id   = get_param(request,'tran_id',None)
    r_id = get_param(request, 'r_id', None)
    if (r_id == tempSecretKey):
        obj['cancelled_id'] = tran_id
        tranObjs = Transactions.objects.filter(id =tran_id).exclude(status="Cancelled").exclude(status="Complete")
        for tran in tranObjs:
            useremail = tran.cust_email
            username  = tran.cust_name
            booking_id = tran.booking_id
            userphone =tran.cust_number
            tran.status = "Complete"
            tran.save()
            obj['result'] = {}
            obj['result']['complete_id'] = tran_id
            obj['status'] = True
            obj['counter'] = 1
            obj['msg'] = "Success"
#    mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
        mviews.send_order_complete(username,userphone,useremail,booking_id)
    return HttpResponse(json.dumps(obj), content_type='application/json')



# general_url = 'https://www.facebook.com/search/results/?q='
# email1 = 'drsnehyadav@gmail.com'
#
# def fetch_location(request):
#     obj = {}
#     obj['status'] = False
#     obj['result'] = {}
#     if random_req_auth(request) or (request.user and request.user.is_authenticated()):
#         location = get_const_list(email1)
#         # print email1
#         obj['result'] = location
#         obj['status'] = True
#     return HttpResponse(json.dumps(obj), content_type='application/json')
#
#
#
#
# def get_const_list(email):
#     url = general_url + email
#     req = requests.get(url)
#     doc = html.fromstring(req.text)
#     print url
#     print doc
#     print req
#     options = doc.xpath("//div[@class='_5d-5']/text()")
#     print options
#     return options

def fetch_user_cart(request):
    obj = {}
    obj['status'] = False
    obj['message'] = 'Access Denied'
    obj['result'] = []
    
    if request.user.email in ['y.shashwat@gmail.com','shashwat@clickgarage.in', 'bhuvan.batra@gmail.com', 'sanskar@clickgarage.in', 'v.rajeev92@gmail.com', 'RajeevVempuluru']:
        userObjs = CGUser.objects.all()
            #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
        for user1 in userObjs:
                obj['result'].append({
                                'id'          : user1.id,
                                'phone'       : user1.contact_no,
                                'email'       : user1.email,
                                'cart'        : user1.uc_cart
                                # ,'name':trans.name

                } )
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')

def add_coupon(request):
    obj = {}
    obj['status'] = True
    obj['result'] = {}
    today = datetime.date.today()

    cpn_cd       = get_param(request,'code',None)
    cpn_msg       = get_param(request,'message',None)

    cpn_amt       = get_param(request,'amount',None)
    cpn_cap    = get_param(request,'cap',None)
    cpn_type    = get_param(request,'type',None)
    cpn_key     = get_param(request, 'price_key', None)
    cpn_vendor    = get_param(request,'vendor',today)
    cpn_cat    = get_param(request,'service',today)
    car_bike    = get_param(request,'car_bike','Car')

    cpn_expiry    = get_param(request,'expiry',None)
    if cpn_expiry:
        try:
            cpn_expiry = eval('datetime.date('+cpn_expiry+')')
        except:
            cpn_expiry = today
    else:
        cpn_expiry = today

    cpn_init    = get_param(request,'init',None)
    if cpn_init:
        try:
            cpn_init = eval('datetime.date('+cpn_init+')')
        except:
            cpn_init = today
    else:
        cpn_init = today

    cpnObjs = Coupon.objects.filter(coupon_code=cpn_cd).exclude(valid="0")

    this_coupon = None

    if len(cpnObjs) and cpnObjs[0].is_coupon_valid() == 'expired':
        this_coupon = cpnObjs[0]

        this_coupon.message = cpn_msg
        this_coupon.date_init       = cpn_init
        this_coupon.date_expiry     = cpn_expiry
        this_coupon.value    = cpn_amt
        this_coupon.cap      = cpn_cap
        this_coupon.type      = cpn_type
        this_coupon.price_key      = cpn_key
        this_coupon.vendor          = cpn_vendor
        this_coupon.category          = cpn_cat
        this_coupon.car_bike        = car_bike

        this_coupon.save()
        obj['result'] = {
            'status'         :   True
            ,'message'      :   'Coupon Updated Successfully'
        }
    elif len(cpnObjs):
        obj['result'] = {
            'status'         :   False
            ,'message'      :   'A valid Coupon already exists'
        }
    else:
        this_coupon = Coupon(
            message = cpn_msg,
            date_init       = cpn_init,
            date_expiry     = cpn_expiry,
            coupon_code     = cpn_cd,
            price_key       = cpn_key,
            value           = cpn_amt,
            cap             = cpn_cap,
            type            = cpn_type,
            vendor          = cpn_vendor,
            category        = cpn_cat,
            car_bike        = car_bike
        )
        this_coupon.save()
        obj['result'] = {
            'status'         :   True
            ,'message'      :   'Coupon Created Successfully'
        }

    return HttpResponse(json.dumps(obj), content_type='application/json')

def apply_coupon(request):
    obj = {}
    obj['status'] = True
    obj['result'] = {}
    obj['msg'] = "Invalid Coupon"
    cpn_cd       = get_param(request,'c_cd',None)
    obj['code'] = cpn_cd
    cpnObjs = Coupon.objects.filter(coupon_code=cpn_cd).exclude(valid="0")
    for cpn in cpnObjs:
        # useremail = tran.cust_email
        # username  = tran.cust_name
        # booking_id = tran.booking_id
        # tran.status = "Cancelled"
        # tran.save()
        obj['result']= {
            'coupon_code'       :    cpn.coupon_code
            ,'date_issue'       :    cpn.date_issue
            ,'valid_till_date'  :    cpn.valid_till_date
            ,'discount'         :    cpn.discount
            ,'cashback'         :    cpn.cashback
            ,'valid'            :    cpn.valid
            ,'status'           :    True

            ,'message'          :    cpn.message
            ,'value'            :    cpn.value
            ,'cap'            :    cpn.cap
            ,'type'            :    cpn.type
            ,'vendor'            :    cpn.vendor
            ,'category'            :    cpn.category
            ,'price_key'            :    cpn.price_key
            ,'car_bike'            :    cpn.car_bike
        }
        # obj['result']['cancell = tran_id
    if len(cpnObjs):
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
    else:
        obj['result'] = {
            'status'         :   False
            ,'message'      :   'Not a coupon'
        }
#    mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
#         mviews.send_cancel_final(username,useremail,booking_id)
    return HttpResponse(json.dumps(obj), content_type='application/json')


def my_date_parser(dt_str):
    if '-' not in dt_str:
        rt = datetime.datetime.strptime(dt_str, '%d/%m/%Y %I:%M %p')
    else:
        rt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %  I:%M %p')

    return rt


def add_guest_transaction(request):
    # print 'p'
    r_id = get_param(request, 'r_id', None)
    apiFlag = (r_id == tempSecretParkwheel)
    if apiFlag or (request.user.email in staffmails):
        print "user"
        # To handle
        email          = get_param(request, 'email', None)
        name           = get_param(request, 'name', None)
        number         = get_param(request, 'number', None)
        car_reg_number = get_param(request, 'reg_no', None)
        pick_obj       = get_param(request, 'pick', None)
        drop_obj       = get_param(request, 'drop', None)
        custom_request = get_param(request, 'custom_req', None)
        sms_info = get_param(request, 'send_sms', None)
        tookan_info = get_param(request, 'send_tookan', None)
        order_list     = get_param(request, 'order_list', None)
        car_name       = get_param(request, 'car_name', None)
        android_flag   = get_param(request, 'android', None)
        coupon_data    = get_param(request, 'global_coupon', None)
        print "*******"
        print sms_info
        print "*******"

        # print coupon_data
        # car_id = get_param(request, 'car_id', None)

        # obj_pick = json.loads(pick_obj)
        pick_obj = ast.literal_eval(pick_obj)
        drop_obj = None
        #ast.literal_eval(drop_obj)
        # pick_obj = ast.literal_eval(pick_obj)
        # print pick_obj
        # pick_obj = json.loads(pick_obj)

        # print pick_obj

        # for key in pick_obj.keys():
        #     print key
        # print json.loads(drop_obj)
        # to handle - list of objects-{service_id:--,service-}
        import json
        order_list = json.loads(order_list)

        print order_list
        print pick_obj
        print drop_obj
        print car_reg_number

        # tran_len = len(Transaction.objects.all())
        booking_id = 1
        # if tran_len > 0:
        #     tran = Transaction.objects.all().aggregate(Max('booking_id'))
        #     booking_id = tran['booking_id'] + 1



        tran_len = len(Transactions.objects.all())
        if tran_len > 0:
            tran = Transactions.objects.all().aggregate(Max('booking_id'))
            booking_id = int(tran['booking_id__max'] + 1)

        html_list = []
        html_list.append('<b>Booking ID #')
        html_list.append(booking_id)
        html_list.append(            '</b><br>Name : ')
        html_list.append(name)
        html_list.append('<br> Time :')
        html_list.append(pick_obj['time'])
        html_list.append('<br> Date :')
        html_list.append(pick_obj['date'])
        # html_list.append(            '. If further assistance is needed, please contact us on 09717353148 and quote your booking confirmation number #')
        # html_list.append(            booking_id)
        # html_list.append(            '.</p>')
        # html_script = ' '.join(str(x) for x in html_list)
        html_list.append('<br>Vehicle :')
        html_list.append(car_name)
        html_list.append('<br> Registration Number : ')
        html_list.append(car_reg_number)
        # html_list.append(') ')
        # html_list.append(':</p>')


        transList = []

        for order in order_list:
            print order
            # to handle - order
            ts = order['ts']

            service = order['service']
            service = service.lower()
            service_id = order['service_id']

            listItem = {}
            listItem['service'] = service
            listItem['service_id'] = service_id
            listItem['ts'] = ts
            listItem['status'] = True
            if service == 'servicing':
                serviceDetail = ServiceDealerCat.objects.filter(id=service_id)
                serviceDetailNew = ServiceDealerCatNew.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)
                    html_list.append('<div>')
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        'odometer':serviceDetail.odometer,
                        'dealer_cat':serviceDetail.dealer_category,
                        'parts_list':serviceDetail.part_replacement,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'wa_price':serviceDetail.wheel_alignment,
                        'wb_price':serviceDetail.wheel_balancing,
                        # 'wa_wb_present':serviceDetail.WA_WB_Inc,
                        'dealer_details':serviceDetail.detail_dealers,
                        'year':serviceDetail.year,
                        'total_price':total_price,
                        'status':True,
                        'ts':ts
                    }


                    listItem['served_data'] = item
                    html_list.append('<span> regular servicing </span>')
                    html_list.append('<span> due at : ')
                    html_list.append(item['odometer'])
                    html_list.append(' / ')
                    html_list.append(item['year'])
                    html_list.append('</span>')

                    html_list.append('<span> dealer : ')
                    html_list.append(item['dealer_cat'])
                    html_list.append('</span>')

                    html_list.append('<span> price : ')
                    html_list.append(total_price)
                    html_list.append('</span>')

                    html_list.append('</div>')

                elif len(serviceDetailNew):
                    serviceDetail = serviceDetailNew[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)
                    html_list.append('<div>')
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        'type_service':serviceDetail.type_service,
                        'dealer_cat':serviceDetail.dealer_category,
                        'parts_list':serviceDetail.part_replacement,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'wa_price':serviceDetail.wheel_alignment,
                        'wb_price':serviceDetail.wheel_balancing,
                        # 'wa_wb_present':serviceDetail.WA_WB_Inc,
                        'dealer_details':serviceDetail.detail_dealers,
                        # 'year':serviceDetail.year,
                        'total_price':total_price,
                        'status':True,
                        'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Servicing </span>')
                    html_list.append('<br><span> Type : ')
                    html_list.append(item['type_service'])
                    html_list.append('</span>')

                    html_list.append('<br><span> dealer : ')
                    html_list.append(item['dealer_cat'])
                    html_list.append('</span>')


                    # tookan integration start

                    car_bike_type = serviceDetail.car_bike
                    category = "Servicing/ Repair"
                    if car_bike_type == "Car":
                        template = "Servicing_Car"
                        servicing_meta_data = [{"label": "Car_Name", "data": serviceDetail.carname},
                                           {"label": "Labour_Estimate", "data": float(serviceDetail.price_labour)},
                                           {"label": "Parts_Estimate", "data": float(serviceDetail.price_parts)}]

                    elif car_bike_type == "Bike":
                        template = "Servicing_Bike"
                        servicing_meta_data = [{"label": "Bike_Name", "data": serviceDetail.carname},
                                           {"label": "Labour_Estimate", "data": float(serviceDetail.price_labour)},
                                           {"label": "Parts_Estimate", "data": float(serviceDetail.price_parts)}]

                    if custom_request:
                        category += ' Custom : ' + custom_request


                    # tookan integration end

                    additional = None
                    if apiFlag:
                        additional = order['additional_data']
                    # elif request.user and 'uc_cart' in request.user:
                    elif request.user.uc_cart:
                        if ts in request.user.uc_cart:
                            this_order = request.user.uc_cart[ts]
                            if 'additional_data' in this_order:
                                additional = this_order['additional_data']
                    if additional:
                        addStr = '<span> Additional Features : '
                        custAddStr = ''
                        for feat, status in additional.iteritems():
                            print status
                            if status:
                                if feat == 'Custom Requests':
                                    custAddStr = '<br/><span> Custom Requests : %s </span>' %(status)
                                elif feat == 'Selected Authorized':
                                    d_name = ''
                                    d_address = ''
                                    if 'name' in status:
                                        d_name = status['name']
                                    if 'address' in status:
                                        d_address = status['address']
                                    custAddStr = '<br/><span> Authorized Dealer Selected : %s (%s) </span>' %(d_name,d_address)
                                else:
                                    addStr = '%s [%s] - ' %(addStr,feat)
                        addStr = addStr + '</span>' + custAddStr
                        html_list.append(addStr)

                    html_list.append('</div>')

            elif service == 'cleaning':
                serviceDetail = CleaningCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    html_list.append('<div>')

                    item = {
                        'id':serviceDetail.id,
                        'category':serviceDetail.category,
                        'car_cat':serviceDetail.car_cat,
                        'service':serviceDetail.service,
                        'vendor':serviceDetail.vendor,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'total_price':serviceDetail.price_total,
                        # 'total_price':total_price,
                        'description':serviceDetail.description,
                        'status':True,
                        'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Cleaning </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(item['category'])
                    html_list.append('<span> Cleaning </span>')
                    html_list.append('<br><span> Category : ')
                    html_list.append(item['category'])
                    html_list.append('</span>')

                    html_list.append('<br><span>')
                    html_list.append(item['vendor'])
                    html_list.append(' - ')
                    html_list.append(item['service'])
                    html_list.append('</span>')

                    # tookan integration start vas

                    category = "Value Added Service"
                    template = "VAS_Car"
                    servicing_meta_data = [{"label": "Car_Name", "data": car_name},
                                           {"label": "Service_Estimate", "data": float(serviceDetail.price_total)},
                                           {"label": "Service_Requested", "data": serviceDetail.service}]


                    # tookan integration end



                    # html_list.append('<span> price : ')
                    # html_list.append(total_price)
                    # html_list.append('</span>')
            elif service == 'vas':
                serviceDetail = VASCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    html_list.append('<div>')

                    item = {
                        'id':serviceDetail.id,
                        'category':serviceDetail.category,
                        'car_cat':serviceDetail.car_cat,
                        'service':serviceDetail.service,
                        'vendor':serviceDetail.vendor,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'total_price':serviceDetail.price_total,
                        # 'total_price':total_price,
                        'description':serviceDetail.description,
                        'status':True,
                        'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Vas </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(item['category'])
                    html_list.append('</span>')
                    html_list.append('<span>')
                    html_list.append(item['vendor'])
                    html_list.append(' - ')
                    html_list.append(item['service'])
                    html_list.append('</span>')

                    html_list.append('<span> price : ')
                    html_list.append(total_price)
                    html_list.append('</span>')

                    html_list.append('</div>')

            elif service == 'windshield':
                serviceDetail = WindShieldServiceDetails.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    # if len(serviceDetail.price_parts):
                    #     total_price = total_price+ float(serviceDetail.price_parts)
                    # if len(serviceDetail.price_labour):
                    #     total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    html_list.append('<div>')

                    item = {
                        'id':serviceDetail.id
                                ,'vendor'         :serviceDetail.vendor
                                ,'brand'          :serviceDetail.brand
                                ,'carname'        :serviceDetail.carname
                                ,'ws_type'        :serviceDetail.ws_type
                                ,'ws_subtype'     :serviceDetail.ws_subtype
                                ,'colour'         :serviceDetail.colour
                                ,'price_ws'       :serviceDetail.price_ws
                                ,'price_sealant'  :serviceDetail.price_sealant
                                ,'price_labour'   :serviceDetail.price_labour
                                ,'price_insurance':serviceDetail.price_insurance
                                ,'price_total'   :serviceDetail.price_total
                                ,'city'           :serviceDetail.city
                                ,'description':serviceDetail.description
                                ,'status':True
                                ,'ts':ts
                    }
                    listItem['served_data'] = item
                    html_list.append('<span> Windshield </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(item['ws_subtype'])
                    html_list.append('&nbsp;(')
                    html_list.append(item['ws_type'])
                    html_list.append('&nbsp;)')
                    html_list.append('</span>')

                    html_list.append('<span>')
                    html_list.append(item['vendor'])
                    html_list.append(' - ')
                    html_list.append(item['colour'])
                    html_list.append('</span>')

                    html_list.append('<span> price : ')
                    html_list.append(item['price_total'])
                    html_list.append('</span>')

                    html_list.append('</div>')
            elif service == 'repair':

                if len(service_id) and (service_id in repair_map):
                    html_list.append('<div>')
                    html_list.append('<span> Repairs </span>')
                    html_list.append('<span> Category : ')
                    html_list.append(repair_map[service_id]['name'])
                    html_list.append('</span>')

                    additional = None

                    if apiFlag:
                        additional = order['additional_data']
                    elif request.user and 'uc_cart' in request.user:
                        if ts in request.user.uc_cart:
                            this_order = request.user.uc_cart[ts]
                            if 'additional_data' in this_order:
                                additional = this_order['additional_data']
                    if additional:
                        addStr = '<span> Repair Queries : '
                        custAddStr = ''
                        for feat, status in additional.iteritems():
                            if status:
                                if feat == 'Custom Requests':
                                    custAddStr = '<br/><span> Custom Requests : %s </span>' %(status)
                                elif feat == 'Damage Type':
                                    custAddStr = '<br/><span> Damage Type : %s </span>' %(status)
                                # elif feat == 'Selected Authorized':
                                #     d_name = ''
                                #     d_address = ''
                                #     if 'name' in status:
                                #         d_name = status['name']
                                #     if 'address' in status:
                                #         d_address = status['address']
                                #     custAddStr = '<br/><span> Authorized Dealer Selected : %s (%s) </span>' %(d_name,d_address)
                                else:
                                    addStr = '%s [%s] - ' %(addStr,feat)
                        addStr = addStr + '</span>' + custAddStr
                        html_list.append(addStr)

                    html_list.append('</div>')

            # if not android_flag:
            #     ac_vi.updateCart(request.user, ts+'*', 'delete', '', None)
            transList.append(listItem)


        #written by vikas for demo
        # print type(pick_obj['street'])
        # pip install dateutil
        # from dateutil import parser as dt_parser
        # date_string = '2007/10/31 0:30pm'
        # dt_parser.parse(date_string)

        if 'street' in pick_obj:
            html_list.append('<div> <span>Pickup Address : </span><span>')
            html_list.append(pick_obj['street'])
        if 'landmark' in pick_obj:
            html_list.append('</span><span> Landmark : ')
            html_list.append(pick_obj['landmark'])
        if 'city' in pick_obj:
            html_list.append('</span><span> City : ')
            html_list.append(pick_obj['city'])
        if 'pincode' in pick_obj:
            html_list.append('</span><span> Pincode : ')
            html_list.append(pick_obj['pincode'])
        html_list.append('</span></div>')

        if coupon_data and len(coupon_data):
            coupon_json = json.loads(coupon_data)
            if isinstance(coupon_json, dict):
                html_list.append('<div><span> Coupons. : ')
                for coupon in coupon_json.keys():
                    html_list.append(coupon)
                    html_list.append(' [')
                    html_list.append(coupon_json[coupon])
                    html_list.append('] ')
                html_list.append('</span></div>')

        html_list.append('<div><span> Contact No. : ')
        html_list.append(str(number))
        html_list.append('</span></div>')

        if drop_obj:
            if 'street' in drop_obj:
                html_list.append('<div> <span>Drop Address : </span><span>')
                html_list.append(drop_obj['street'])
            if 'landmark' in drop_obj:
                html_list.append('</span><span> Landmark : ')
                html_list.append(drop_obj['landmark'])
            if 'city' in drop_obj:
                html_list.append('</span><span> City : ')
                html_list.append(drop_obj['city'])
            if 'pincode' in drop_obj:
                html_list.append('</span><span> Pincode : ')
                html_list.append(drop_obj['pincode'])
            html_list.append('</span></div>')

        # create_guest_user(name,email);


        tt = Transactions(
            booking_id      = booking_id,
            trans_timestamp = time.time(),
            cust_id         = create_guest_user(name,email).id,
            cust_name       = name,
            cust_brand      = '',
            cust_carname    = car_name,
            cust_number     = number,
            cust_carnumber  = car_reg_number,
            cust_email      = email,

            cust_pickup_add = pick_obj,
            cust_drop_add   = drop_obj,

            service_items   = transList,

            price_total     = '',

            date_booking    = pick_obj['date'],
            time_booking    = pick_obj['time'],
            amount_paid     = '',
            status          = '',
            comments        = ''
        )
        tt.save()
        html_script = ' '.join(str(x) for x in html_list)
        # mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
        mviews.send_booking_final_guest(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script,sms_info)

        obj = {}
        obj['status'] = True
        obj['result'] = pick_obj

        print pick_obj
        print '*'*100
        print type(pick_obj)
        print '*'*100
        # print pick_obj.__dict__
        # Tookan Integration Start




        if tookan_info == "Yes":
            from dateutil import parser as dt_parser
            customer_address = ', '.join([pick_obj.get('street',''),pick_obj.get('landmark',''),pick_obj.get('city','')])
            start_time = pick_obj.get('date')+' '+pick_obj.get('time').split(' - ')[0]
            print 'st0', start_time

            start_time = my_date_parser(start_time)

            print 'st',start_time.month,start_time.year,start_time.day
            start_time = start_time.strftime('%m/%d/%Y %I:%M %p')
            end_time = pick_obj.get('date') + ' ' + pick_obj.get('time').split(' - ')[1]
            print 'et0', end_time
            end_time = my_date_parser(end_time)
            print 'et', end_time.month,end_time.year,end_time.day
            end_time = end_time.strftime('%m/%d/%Y %I:%M %p')
            print start_time
            print end_time
            # a = {"label": "Servicing_Labour", "data": "100"}
            values = {
                "customer_email": email,
                "order_id": str(booking_id),
                "customer_username": name,
                "customer_phone": number,
                "customer_address": customer_address,
                "latitude": "",
                "longitude": "",
                "job_description": category,
                "job_pickup_datetime": start_time,
                "job_delivery_datetime": end_time,
                "has_pickup": "0",
                "has_delivery": "0",
                "layout_type": "1",
                "tracking_link": 1,
                "timezone": "-330",
                "team_id":"12376",
                "custom_field_template": template,
                "meta_data": servicing_meta_data,
                "api_key": "a18332760b2847468d7b569f88ff0fce345c32a0580b095657c81890251fc0a0",
                "team_id": "255",
                "auto_assignment": "0",
                "fleet_id": "636",
                "ref_images": ["https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/8b0df50f-a54b-4a7b-9ef6-c31d66aff1f1.jpg"],
                "notify": 1,
                # "tags": "tag1,tag2",
                "geofence": 0
            }

            print values

            headers = {
                'Content-type': 'application/json'
            }

            # import requests
            url = 'https://api.tookanapp.com/v2/create_task'
            # import json
            req = requests.post(url, data=json.dumps(values), headers=headers, verify= False, timeout = 10)
            # req = Request(url , data=json.dumps(values), headers=headers)
            # obj['took'] = urlopen(req).read()

            obj['took'] = req.json() if req.status_code == 200 else req.content


        # Tookan Integration End



        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:

        print "no user"
        obj = {}
        obj['status'] = False
        if request.user and request.user.is_authenticated():
            obj['result'] = {
                'username':request.user.username,
                'id':request.user.id,
                'contact':request.user.email,
                'email':request.user.contact_no
            }
        return HttpResponse(json.dumps(obj), content_type='application/json')

        # redirect('/loginPage/')

def create_guest_user(name,email='',number=None):
    if number:
        # if not name:
        #     name = number
        users = CGUser.objects.filter(contact_no=number)
        if len(users):
            return users[0]
        else:
            # create_user(name,email)
            user_new = CGUser(username=number,email=email,contact_no=number)
            # users2 = CGUser.objects.filter(email=email)
            # user2 = users2[0]
            # user2.active = False
            # user2.user_type = 'Guest'
            if name:
                name = name.split(' ')
                user_new.first_name = name[0]
                if len(name) > 1:
                    user_new.last_name = name[1]
            user_new.save()
            return user_new

    elif email:
        email = email.lower()
        if not name:
            name = email
        users = CGUser.objects.filter(email=email)
        if len(users):
            return users[0]
        else:
            # create_user(name,email,"")
            # users2 = CGUser.objects.filter(email=email)
            user_new = CGUser(username=name,email=email)
            # user2 = users2[0]
            # user2.active = False
            # user2.user_type = 'Guest'
            # user2.save()
            user_new.save()
            return user_new
    # def create_user(username, email, password):
    # user = User(username=username, email=email)
    # user.set_password(password)
    # user.save()
    # return user

def send_contact(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    # obj['msg'] = "Invalid Coupon"
    name       = get_param(request,'name',None)
    phone      = get_param(request,'phone',None)
    message      = get_param(request,'message',None)

    # obj['code'] = cpn_cd
    # cpnObjs = Coupon.objects.filter(coupon_code=cpn_cd).exclude(valid="0")
    # for cpn in cpnObjs:
    #     # useremail = tran.cust_email
    #     # username  = tran.cust_name
    #     # booking_id = tran.booking_id
    #     # tran.status = "Cancelled"
        # tran.save()
        # obj['result']= {
        #     'coupon_code'       :    cpn.coupon_code
        #     ,'date_issue'       :    cpn.date_issue
        #     ,'valid_till_date'  :    cpn.valid_till_date
        #     ,'discount'         :    cpn.discount
        #     ,'cashback'         :    cpn.cashback
        #     ,'message'          :    cpn.message
        #     ,'valid'            :    cpn.valid
        #     ,'status'           :    True
        # }
        # obj['result']['cancell = tran_id
    # if len(cpnObjs):
    mviews.send_contact_mail(name,phone,message)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    # else:
    #     obj['result'] = {
    #         'status'         :   False
    #         ,'message'      :   'Not a coupon'
    #     }
#    mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
#         mviews.send_cancel_final(username,useremail,booking_id)
    return HttpResponse(json.dumps(obj), content_type='application/json')


def send_otp(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}

    # phone = phone1
    phn = get_param(request,'phone',None)
    otp = random.randint(100000, 999999)
    otpdatetime = datetime.datetime.now()
    message = "Your ClickGarage one time password is " + str(otp) + ". Please enter the same to complete your mobile verification."
    message = message.replace(" ","+")
    newFlag = False
    username = None
    # print message
    findOtp     = Otp.objects.filter(mobile=phn)
    if len(findOtp ):
        findOtp = findOtp[0]
        obj['result']['username'] = findOtp.username
        findOtp.otp      = otp
        findOtp.updated  = otpdatetime
        findOtp.save()

    else:
        newFlag = True
        cc = Otp(
            mobile = phn,
            otp = otp,
            created = otpdatetime,
            updated = otpdatetime)
        cc.save()

    mviews.send_otp(phn,message)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    obj['result']['new_user'] = newFlag
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_all_otp(request):
    obj = {}
    result = []
    allOtp = Otp.objects.all()
    for otp in allOtp:
        result.append({
            'mobile':otp.mobile,
            'otp':otp.otp
        })

    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def checkOTP(onetp, mobile, name):
    check = False
    msg = ''
    curr_time = datetime.datetime.now()
    curr_ts = calendar.timegm(curr_time.timetuple())
    findOtp     = Otp.objects.filter(mobile=mobile)
    mviews.send_signup_mail(name,mobile,"NA")
    if len(findOtp) and findOtp[0].otp:
        findOtp = findOtp[0]
        otp_ts = calendar.timegm(findOtp.updated.timetuple())
        if (curr_ts - otp_ts) > 3600:
            msg = 'expired otp'
            findOtp.otp = ''
            findOtp.updated = curr_time
            findOtp.save()
        elif onetp == findOtp.otp:
            msg = 'success'
            check = True
            findOtp.otp = ''
            if name:
                findOtp.username = name
            findOtp.updated = curr_time
            findOtp.save()
        else:
            msg = 'wrong otp'
    else:
        msg = 'no active otp'

    return {'msg': msg, 'status': check}

def create_otp_user(request):
    # obj = {}
    # obj['status'] = False
    # obj['result'] = {}

    # phone = phone1
    name = get_param(request,'name',None)
    phn = get_param(request,'phone',None)
    onetp = get_param(request,'otp',None)

    obj = checkOTP(onetp,phn,name)
    if obj['status']:
        user = create_guest_user(name,'',phn)
        if not request.user or request.user.is_anonymous():
            # logout(request)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        obj['result'] = {}
        obj['result']['userid'] = request.user.id
        if request.user.first_name and len(request.user.first_name):
            obj['result']['username'] = request.user.first_name
        else:
            obj['result']['username'] = request.user.username
        obj['result']['email'] = request.user.email
        obj['result']['auth'] = True
    else:
        obj['status'] = True
        obj['result'] = {}
        obj['result']['auth'] = False
        obj['result']['msg'] = obj['msg']

    # findOtp     = Otp.objects.filter(mobile=phn)
    # if (onetp==findOtp[0].otp):
    #     obj['status'] = True
    #     obj['counter'] = 1
    #     obj['msg'] = "Success"
    #     user = create_guest_user(name,'',phn)
    #     if not request.user or request.user.is_anonymous():
    #         # logout(request)
    #         login(request, user)
    #     obj['result']= user.id

    return HttpResponse(json.dumps(obj), content_type='application/json')

def service_selected(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    service            = get_param(request,'service',None)
    id_selection      = get_param(request,'id',None)
    result = []

    if (service=="servicing"):
        ServicedetailObjs = ServiceDealerCatNew.objects.filter(id=id_selection)
        for service in ServicedetailObjs:
                        obj['result'].append({
                            'id':service.id
                              ,'name':service.name
                              ,'brand':service.brand
                              ,'car':service.carname
                              ,'car_bike':service.car_bike
                              ,'vendor':service.dealer_category
                              ,'parts_list':service.part_replacement
                              ,'parts_price':service.price_parts
                              ,'labour_price':service.price_labour
                              ,'wa_price':service.wheel_alignment
                              ,'wb_price':service.wheel_balancing
                              # ,'wa_wb_present':service.WA_WB_Inc
                              ,'dealer_details':service.detail_dealers
                              # ,'car_bike':car_bike
                        ,'type_service':service.type_service
                        ,'part_dic':service.part_dic
                        ,'labour_price':service.price_labour
                        ,'discosunt':service.discount
                        ,'priority':service.priority
                     } )
    if (service=="cleaning"):
        CleanCatObjs=CleaningCategoryServices.objects.filter(id=id_selection)
        for service in CleanCatObjs:
                obj['result'].append({
                        'id':service.id
                        ,'vendor':service.vendor
                        ,'category':service.category
                        ,'car_cat':service.car_cat
                        ,'type_service':service.service
                        ,'price_labour':service.price_labour
                        ,'price_parts':service.price_parts
                        ,'total_price':service.price_total
                        ,'description':service.description
                        ,'discount':service.discount
                        ,'rating':service.rating
                        ,'reviews':service.reviews
                        ,'priority':service.priority
                      } )
    if (service=="vas"):
        VasCatObjs=VASCategoryServices.objects.filter(id=id_selection)
        for service in VasCatObjs:
                obj['result'].append({
                        'id':service.id
                        ,'vendor':service.vendor
                        ,'category':service.category
                        ,'car_cat':service.car_cat
                        ,'type_service':service.service
                        ,'price_labour':service.price_labour
                        ,'price_parts':service.price_parts
                        ,'total_price':service.price_total
                        ,'description':service.description
                        ,'doorstep':service.doorstep
                        ,'discount':service.discount
                        ,'rating':service.rating
                        ,'reviews':service.reviews
                        ,'car_bike': service.car_bike
                        ,'priority':service.priority
                      } )
    if (service=="windshield"):
        wsTypeObjs=WindShieldServiceDetails.objects.filter(id=id_selection)
        # wsTypeObjs = WindShieldServiceDetails.objects.filter(city=city,vendor = vendor, ws_type = ws_type, carname = carname, brand=brand)
        for service in wsTypeObjs:
            obj['result'].append({'id':service.id
                                    ,'vendor':service.vendor
                                    ,'brand':service.brand
                                    ,'carname':service.carname
                                    ,'colour':service.colour
                                    ,'type_service':service.ws_type
                                    ,'ws_subtype':service.ws_subtype
                                    ,'price_ws':service.price_ws
                                    ,'price_sealant':service.price_sealant
                                    ,'price_labour':service.price_labour
                                    ,'price_insurance':service.price_insurance
                                    ,'total_price'    :service.price_total
                                    ,'city'           :service.city
                                    ,'description':service.description
                                    ,'rating':service.rating
                                    ,'reviews':service.reviews
                              } )



    # CleaningCategoryServices.objects.all().delete()
    # VASCategoryServices.objects.all().delete()
    # WindShieldServiceDetails.objects.all().delete()


    # obj['result'] = result
    obj['status'] = True
    # obj['counter'] = 1
    obj['msg'] = "Success"
    # else:
    #     obj['result'] = {
    #         'status'         :   False
    #         ,'message'      :   'Not a coupon'
    #     }
#    mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
#         mviews.send_cancel_final(username,useremail,booking_id)
    return HttpResponse(json.dumps(obj), content_type='application/json')

# Drivers APIs
# def signUpDriver(request):
#     from api.drivers import signUpDriver
#     return signUpDriver(request)
#
# def updateBookingStatus(request):
#     from api.drivers import updateBookingStatus
#     return updateBookingStatus(request)
#
# def getDriverBookings(request):
#     from api.drivers import getDriverBookings
#     return getDriverBookings(request)


# <------------------------ Website Revamp ------------------------>

google_map_api_key = "AIzaSyBFxHslgLn1N0XVrRnONqZTJWFyorZd5PQ"
import operator
def get_type_make(request):
    vehicle_type = get_param(request, 'vehicle_type', None)
    # make_id = get_param(request,'make_id',None)
    # model_id = get_param(request,'model_id',None)
    obj = {}

    obj['status'] = False
    obj['result'] = []

    # vehicle = None
    # make = None
    # car_bike = None
    VehObjs = Vehicle.objects.filter(car_bike = vehicle_type).order_by('make')
    for veh in VehObjs:
        obj['result'].append({
                            # 'id' :            veh.id
                            'make':           veh.make
                            # 'model' :         veh.model
                            # 'year' :          veh.year
                            # 'fuel_type' :     veh.fuel_type
                            # 'full_veh_name':  veh.full_veh_name
                            # 'aspect_ratio' :  veh.aspect_ratio
                            # 'size' :          veh.size
                            # 'car_bike' :      veh.car_bike
                            # 'engine_oil' :    veh.engine_oil
                            # 'active' :        veh.active
                                  })

    obj['result'] = {v['make']:v for v in obj['result']}.values()
    obj['result'] = sorted(obj['result'], key=operator.itemgetter('make'))
    # =y
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')




def get_make_model(request):
    vehicle_type = get_param(request, 'vehicle_type', None)
    make_id = get_param(request,'make_id',None)
    # model_id = get_param(request,'model_id',None)
    obj = {}

    obj['status'] = False
    obj['result'] = []

    # vehicle = None
    # make = None
    # car_bike = None
    VehObjs = Vehicle.objects.filter(car_bike = vehicle_type, make = make_id).order_by('model')
    for veh in VehObjs:
        obj['result'].append({
                            # 'id' :            veh.id
                            'make':           veh.make,
                            'model' :         veh.model
                            # 'year' :          veh.year
                            # 'fuel_type' :     veh.fuel_type
                            # 'full_veh_name':  veh.full_veh_name
                            # 'aspect_ratio' :  veh.aspect_ratio
                            # 'size' :          veh.size
                            # 'car_bike' :      veh.car_bike
                            # 'engine_oil' :    veh.engine_oil
                            # 'active' :        veh.active
                                  } )

    obj['result'] = {v['model']:v for v in obj['result']}.values()
    obj['result'] = sorted(obj['result'], key=operator.itemgetter('make','model'))
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def get_jobs_vehicle(request):
    make_id = get_param(request,'make_id',None)
    model_id = get_param(request,'model_id',None)
    fuel_id = get_param(request,'fuel_id',None)
    service_type = get_param(request, 'service_type', None)

    obj = {}

    obj['status'] = False
    obj['result'] = []

    jobObjs = Services.objects.filter(make = make_id, model = model_id, fuel_type = fuel_id, service_cat = service_type).order_by('priority')
    for job in jobObjs:
        obj['result'].append({
                            "id" :            job.id
            ,"make"	: job.make
            ,"model"    : job.model
            ,"year"    : job.year
            ,"fuel_type"    : job.fuel_type
            , "full_veh_name"    : job.full_veh_name
            , "car_bike"    : job.car_bike
            , "city"    : job.city
            , "service_cat"    : job.service_cat
            , "service_desc"    : job.service_desc
            , "job_name"    : job.job_name
            , "doorstep"    : job.doorstep
            , "job_summary"    : job.job_summary
            , "job_desc"    : job.job_desc
            , "job_features"    : job.job_features
            , "job_symptoms"    : job.job_symptoms
            , "job_dealer"    : job.dealer
            , "default_comp"    : job.default_components
            , "optional_comp"    : job.optional_components
            , "total_price"    : job.total_price
            , "total_price_comp"    : job.total_price_comp
            , "time"    : job.time
            , "priority"    : job.priority
        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def add_job_cart(request):
    # service_ids = get_param(request,'service_names',None)
    cookieCartData = request.COOKIES.get('cgcart')
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    obj['result']['cart_details'] = []
    cg_price = 0
    comp_price = 0
    if cookieCartData:
        list_ids = cookieCartData.split(',')
        jobObjs = Services.objects.filter(id__in=list_ids)
        for job in jobObjs:
            obj['result']['cart_details'].append({
                 "id" :            job.id
                ,"make"	: job.make
                ,"model"    : job.model
                ,"year"    : job.year
                ,"fuel_type"    : job.fuel_type
                , "full_veh_name"    : job.full_veh_name
                , "car_bike"    : job.car_bike
                , "city"    : job.city
                , "service_cat"    : job.service_cat
                , "service_desc"    : job.service_desc
                , "job_name"    : job.job_name
                , "doorstep"    : job.doorstep
                , "job_summary"    : job.job_summary
                , "job_desc"    : job.job_desc
                , "job_features"    : job.job_features
                , "job_symptoms"    : job.job_symptoms
                , "job_dealer"    : job.dealer
                , "default_comp"    : job.default_components
                , "optional_comp"    : job.optional_components
                , "total_price"    : job.total_price
                , "total_price_comp"    : job.total_price_comp
                , "time"    : job.time
                , "priority"    : job.priority
            }
            )
            cg_price = float(job.total_price) + cg_price
            comp_price = float(job.total_price_comp) + comp_price

    if comp_price == 0:
        discount = 0
    else:
        discount = "NA"


    obj['result']['cart_summary'] = [{
        "cg_amount": cg_price
        , "comp_amount": comp_price
        ,"discount": discount
        ,"diff_amount": (comp_price-cg_price)
    }]
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')






















def get_location(request):
    location_id = get_param(request, 'location_id', None)
    location_delhi="28.6466773,76.813073"
    radius_m = "100000"
    obj = {}
    obj['status'] = False
    obj['result'] = []
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="+location_id+"&types=geocode&language=en&location="+ location_delhi +"&radius="+radius_m+"&key="+ google_map_api_key
    req = requests.get(url)
    obj['result'] = req.json()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')


def post_lead(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}

    # phone = phone1
    firstname = get_param(request, 'firstname', None)
    lastname = get_param(request, 'lastname', None)
    car_bike = get_param(request, 'car_bike', None)
    make = get_param(request, 'make', None)
    model = get_param(request, 'model', None)
    fuel_type = get_param(request, 'fuel_type', None)
    service_category = get_param(request, 'service_category', None)
    additional = get_param(request, 'additional', None)
    address = get_param(request, 'address', None)
    locality = get_param(request, 'locality', None)
    date_requested = get_param(request, 'date_requested', None)
    time_requested = get_param(request, 'time_requested', None)
    number = get_param(request, 'number', None)
    email = get_param(request, 'email', None)
    source = get_param(request, 'source', None)
    time_stamp = get_param(request, 'time_stamp', None)

    cc = Leads(firstname       = firstname       ,
                lastname        = lastname        ,
                car_bike        = car_bike        ,
                make            = make            ,
                model           = model           ,
                fuel_type       = fuel_type       ,
                service_category= service_category,
                additional_request        = additional         ,
                address         = address         ,
                locality        = locality        ,
                date_requested  = date_requested  ,
                time_requested  = time_requested  ,
                number          = number          ,
                email           = email           ,
                source          = source          ,
                time_stamp      = time_stamp      )
    cc.save()

    mviews.send_lead(firstname,lastname,car_bike, number,email, make, model, fuel_type, additional, service_category,locality,address,date_requested,time_requested)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def post_message(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}

    # phone = phone1
    firstname = get_param(request, 'firstname', None)
    lastname = get_param(request, 'lastname', None)
    number = get_param(request, 'number', None)
    email = get_param(request, 'email', None)
    time_stamp = get_param(request, 'time_stamp', None)
    message = get_param(request,'message',None)
    cc = Messages(firstname = firstname,
                lastname  = lastname,
                number    = number,
                message   = message,
                email     = email,
                time_stamp      = time_stamp)
    cc.save()

    mviews.send_message(firstname,lastname, number,email, message)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')


