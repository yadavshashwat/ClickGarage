from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
import datetime, time

from django.db.models import Max

import operator
import json
import ast
import re
from django.views.decorators.csrf import csrf_exempt

from models import *
from dataEntry.runentry import carMakers, cleanstring
from activity import views as ac_vi
from mailing import views as mviews

from activity.models import Transactions

tempSecretKey = 'dmFydW5ndWxhdGlsaWtlc2dhbG91dGlrZWJhYg=='

#login views

def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
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
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user

def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def sign_up_in(request):
    post = request.POST
    if not user_exists(post['email']):
        user = create_user(username=post['email'], email=post['email'], password=post['password'])
    	return auth_and_login(request)
    else:
    	return redirect("/login/")

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
        result.append({'name':car.name, 'make':car.make, 'aspect_ratio':car.aspect_ratio,'size':car.size,'car_bike':car.car_bike,'id':car.id})

    obj['result'] = result
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')




def fetch_car(request, HTTPFlag=True):
    car_id = get_param(request, 'c_id', None)
    print car_id
    obj = {}
    obj['status'] = False
    if car_id:
        carObj = Car.objects.filter(id=car_id)
        if len(carObj):
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
                              ,'wa_wb_present':service.WA_WB_Inc
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
    allServices = Servicing.objects.order_by('odometer')
    for service in allServices:
        result.append({'id':service.id,
                        'name' : service.name  
                        ,'brand' : service.brand     
                        ,'car_name' : service.carname                   
                        ,'odometer_reading' : service.odometer               
                        ,'time_reading' : service.year                   
                        ,'checks_done' : service.regular_checks                    
                        ,'paid_free' : service.paid_free              
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
    allDealerCat = ServiceDealerCat.objects.order_by('odometer','dealer_category')

    for service in allDealerCat:

        result.append({ 'id':service.id
                        ,'name':service.name                
                        ,'brand_name':service.brand               
                        ,'car_name':service.carname             
                        ,'odometer':service.odometer
                        ,'year':service.year           

                        ,'dealer_category':service.dealer_category     
                        ,'parts_replaced':service.part_replacement    
                        ,'parts_price':service.price_parts         
                        ,'labour_price':service.price_labour        
                        ,'wheel_alignment_price':service.wheel_alignment     
                        ,'wheel_balancing_price':service.wheel_balancing     
                        ,'WA_WB?':service.WA_WB_Inc           
                        ,'dealer_details':service.detail_dealers
                        ,'paid_free?':service.paid_free      
                        ,'regular_checks':service.regular_checks       
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

    if catg_id:
        cleanObj = CleaningServiceCat.objects.filter(id=catg_id)
        
        if len(cleanObj):
            cleanObj = cleanObj[0]
            vendor = cleanObj.vendor
            category = cleanObj.category


    if vendor:
        if category:
            if size:
             CleanCatObjs = CleaningCategoryServices.objects.filter(vendor = vendor, category = category,car_cat = size)
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
                        ,'rating':service.rating          
                        ,'reviews':service.reviews                        
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
            ,'service_description':service.description    
            ,'rating':service.rating         
            ,'reviews':service.reviews        } )
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
             VASCatObjs = VASCategoryServices.objects.filter(vendor = vendor, category = category,car_cat = size)
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
                        ,'doorstep':service.doorstep     
                        ,'rating':service.rating          
                        ,'reviews':service.reviews                        
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
                                        , 'brand  ' :service.brand
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
    car = None
    make = None
    odo = None

  
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
                                    ,'vendor         ':service.vendor           
                                    ,'brand          ':service.brand            
                                    ,'carname        ':service.carname          
                                    ,'ws_type        ':service.ws_type          
                                    ,'ws_subtype     ':service.ws_subtype       
                                    ,'price_ws       ':service.price_ws         
                                    ,'price_sealant  ':service.price_sealant    
                                    ,'price_labour   ':service.price_labour     
                                    ,'price_insurance':service.price_insurance 
                                    ,'price_total'    :service.price_total
                                    ,'city'           :service.city
                                    ,'description    ':service.description      
                                    ,'rating         ':service.rating           
                                    ,'reviews        ':service.reviews                           
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
            , 'brand  ' :service.brand
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

def addItemToCart(request):
    cookie_data = get_param(request, 'cookie',None)
    car_id = get_param(request, 'car_id',None)
    remove = get_param(request, 'delete',False)
    obj = {}
    obj['status'] = False
    obj['result'] =[]

    print request
    if request.user.is_authenticated():
        if cookie_data:
            if remove:
                resp = ac_vi.updateCart(request.user, cookie_data, 'delete', car_id)
            else:
                resp = ac_vi.updateCart(request.user, cookie_data, 'add', car_id)


    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"

    return HttpResponse(json.dumps(obj), content_type='application/json')

def getUserDetails(request):
    obj = {}
    obj['status'] = False
    obj['result'] ={}

    print request.user
    if request.user.is_authenticated():
        res = {}
        res['userid'] = request.user.id
        res['u_cart'] = request.user.unchecked_cart
        res['uc_cart'] = request.user.uc_cart
        res['saved_addresses'] = request.user.saved_address
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
                print size
        if catg_id:
            cleanObj = CleaningCatName.objects.filter(id=catg_id)

            if len(cleanObj):
                cleanObj = cleanObj[0]
                category = cleanObj.category
                print category


        if category:
            if size:
                CleanCatObjs = CleaningCategoryServices.objects.filter(category = category,car_cat = size, car_bike = car_bike)
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
                            ,'rating':service.rating
                            ,'reviews':service.reviews
                            ,'car_bike': service.car_bike
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
            CleanCatObjs = VASCategoryServices.objects.filter(category = category,car_cat = size, car_bike = car_bike)
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
                        ,'rating':service.rating          
                        ,'reviews':service.reviews   
                        ,'car_bike': service.car_bike                  
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
def place_order(request):
    print 'p'
    if (request.user and request.user.is_authenticated()) or random_req_auth(request):
        email = request.user.email
        name = get_param(request, 'name', None)
        number = get_param(request, 'number', None)
        car_reg_number = get_param(request, 'reg_no', None)
        pick_obj = get_param(request, 'pick', None)
        drop_obj = get_param(request, 'drop', None)
        order_list = get_param(request, 'order_list', None)
        car_name = get_param(request, 'car_name', None)
        android_flag = get_param(request, 'android', None)
        # car_id = get_param(request, 'car_id', None)

        # obj_pick = json.loads(pick_obj)
        pick_obj = ast.literal_eval(pick_obj)
        drop_obj = ast.literal_eval(drop_obj)
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
        print drop_obj

        tran_len = len(Transaction.objects.all())
        booking_id = 1
        if tran_len > 0:
            tran = Transaction.objects.all().aggregate(Max('booking_id'))
            booking_id = tran['booking_id'] + 1



        tran_len = len(Transactions.objects.all())
        if tran_len > 0:
            tran = Transactions.objects.all().aggregate(Max('booking_id'))
            booking_id = int(tran['booking_id__max'] + 1)

        html_list = []
        html_list.append('<b>Booking ID #')
        html_list.append(    booking_id)
        html_list.append(            '</b><br><p>Hi ')
        html_list.append(name)
        html_list.append(',<br> Your ClickGarage booking has been confirmed. Pick up time chosen by you is ')
        html_list.append(            pick_obj['time'])
        html_list.append(            ' on ')
        html_list.append(            pick_obj['date'])
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
            service = order['service']
            service_id = order['service_id']

            listItem = {}
            listItem['service'] = service
            listItem['service_id'] = service_id
            listItem['ts'] = ts
            listItem['status'] = True
            if service == 'servicing':
                serviceDetail = ServiceDealerCat.objects.filter(id=service_id)
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
                        'wa_wb_present':serviceDetail.WA_WB_Inc,
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
            if not android_flag:
                ac_vi.updateCart(request.user, ts+'*', 'delete', '')
            transList.append(listItem)


        html_list.append('<div> <span>Pickup Address : </span><span>')
        html_list.append(pick_obj['street'])
        html_list.append('</span><span> Landmark : ')
        html_list.append(pick_obj['landmark'])
        html_list.append('</span><span> City : ')
        html_list.append(pick_obj['city'])
        html_list.append('</span><span> Pincode : ')
        html_list.append(pick_obj['pincode'])
        html_list.append('</span></div>')

        html_list.append('<div><span> Contact No. : ')
        html_list.append(str(number))
        html_list.append('</span></div>')

        html_list.append('<div> <span>Drop Address : </span><span>')
        html_list.append(drop_obj['street'])
        html_list.append('</span><span> Landmark : ')
        html_list.append(drop_obj['landmark'])
        html_list.append('</span><span> City : ')
        html_list.append(drop_obj['city'])
        html_list.append('</span><span> Pincode : ')
        html_list.append(drop_obj['pincode'])
        html_list.append('</span></div>')


        tt = Transactions(
            booking_id      = booking_id,
            trans_timestamp = time.time(),
            cust_id         = request.user.id,
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
        mviews.send_booking_final(name,email,number,pick_obj['time'],pick_obj['date'],str(booking_id),html_script)
        obj = {}
        obj['status'] = True
        obj['result'] = pick_obj
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

    tran_len = len(Transaction.objects.all())
    if tran_len > 0:
        tran = Transaction.objects.all().aggregate(Max('booking_id'))
        booking_id = tran['booking_id'] + 1
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
    obj['result'] = []
    cust_id = None
    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        cust_id = request.user.id

    if cust_id:
        tranObjs = Transactions.objects.filter(cust_id=cust_id, status = '').order_by('-booking_id')
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
    if random_req_auth(request) or (request.user and request.user.is_authenticated()):
        cust_id         = request.user.id
        email           = request.user.email
        tran_id         = get_param(request,'tran_id',None)

    obj['cancelled_id'] = tran_id
    tranObjs = Transactions.objects.filter(status = '', id =tran_id)
    for tran in tranObjs:
        tran.status = "Cancelled"
        tran.save()
        obj['result'] = {}
        obj['result']['cancelled_id'] = tran_id
        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

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
    CarObjs = Car.objects.filter(car_bike = car_bike_id, make = make_id)
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
                make = carObj.make
                car = make + " " + car_old
                if car:
                    ServiceObjs = ServicingNew.objects.filter(carname = car, brand = make)
                    #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
                    for service in ServiceObjs:
                        obj['result'].append({
                            'id':service.id
                            ,'name':service.name
                            ,'brand':service.brand
                            ,'car_name':service.carname
                            ,'type_service':service.type_service
                            # ,'year':service.year
                            ,'regular_checks':service.regular_checks
                            # ,'paid_free':service.paid_free
                            ,'parts_replaced':service.part_replacement
                            ,'dealers_list':service.dealer} )



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
                    ServicedetailObjs = ServiceDealerCatNew.objects.filter(carname = car, brand = make, type_service = type_service).order_by('priority')
                    for service in ServicedetailObjs:
                        obj['result'].append({
                            'id':service.id
                              ,'name':service.name
                              ,'brand':service.brand
                              ,'car':service.carname
                              ,'type_service':service.type_service
                              ,'vendor':service.dealer_category
                              ,'parts_list':service.part_replacement
                              ,'parts_price':service.price_parts
                              ,'labour_price':service.price_labour
                              ,'wa_price':service.wheel_alignment
                              ,'wb_price':service.wheel_balancing
                              ,'wa_wb_present':service.WA_WB_Inc
                              ,'dealer_details':service.detail_dealers
                              ,'discount':service.discount
                              ,'priority':service.priority
                              ,'car_bike':car_bike}
                        )


        obj['status'] = True
        obj['counter'] = 1
        obj['msg'] = "Success"
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return HttpResponse(json.dumps(obj), content_type='application/json')


