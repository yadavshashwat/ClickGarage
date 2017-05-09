production = 1

from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.db import models
import datetime, time, calendar
# from datetime import datetime
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
# from bson import json_util
from models import *
from dataEntry.runentry import carMakers, cleanstring
from activity import views as ac_vi
from mailing import views as mviews
from api import tasks as tasks
# from wkhtmltopdf import WKHtmlToPdf
from django.db.models import Q
import math
import os
import socket
from activity.models import Transactions, CGUser, CGUserNew
# from lxml import html
import csv

PRODUCTION = False

if os.getcwd()=='/home/ubuntu/beta/suigen':
    PRODUCTION = True


tempSecretKey = 'dmFydW5ndWxhdGlsaWtlc2dhbG91dGlrZWJhYg=='
tempSecretParkwheel = 'dGhpcyBrZXkgaXMgZm9yIFBhcmt3aGVlbHM='
superadmin = ["9717353148"]

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


def fetch_all_booking(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    cust_id = None
    # if random_req_auth(request) or (request.user and request.user.is_authenticated()):
    #     cust_id = request.user.id


    tranObjs = Transactions.objects.all()
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
#
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
    if request.user.is_staff:
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
    otp = random.randint(1000, 9999)
    otpdatetime = datetime.datetime.now()
    message = "Your ClickGarage one time password is " + str(otp) + ". Please enter the same to complete your mobile verification."
    # message = message.replace(" ","+")
    newFlag = False
    username = None
    # print message
    findOtp     = Otp.objects.filter(mobile=phn)
    if len(findOtp):
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

def get_make_model_old(request):
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
            'id' :            veh.id,
            'make':           veh.make,
            'model' :         veh.model,
            # 'year' :          veh.year
            'fuel_type' :     veh.fuel_type,
            'full_veh_name' : veh.model + " ("+ veh.fuel_type+")"
            # 'full_veh_name':  veh.full_veh_name
            # 'aspect_ratio' :  veh.aspect_ratio
            # 'size' :          veh.size
            # 'car_bike' :      veh.car_bike
            # 'engine_oil' :    veh.engine_oil
            # 'active' :        veh.active
        } )

    # obj['result'] = {v['model']:v for v in obj['result']}.values()
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
    doorstep = get_param(request,'doorstep',None)
    sub_cat = get_param(request,'sub_cat',None)


    obj = {}
    obj['status'] = False
    obj['result'] = []

    jobObjs = Services.objects.filter(make=make_id, model=model_id, fuel_type=fuel_id).order_by('priority')

    if service_type != None:
        jobObjs = jobObjs.filter(make = make_id, model = model_id, fuel_type = fuel_id, service_cat = service_type).order_by('priority')

    if sub_cat != None:
        jobObjs = jobObjs.filter(job_sub_cat = sub_cat)

    if doorstep != None:
        jobObjs = jobObjs.filter(doorstep=doorstep)

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
            # , "service_desc"    : job.service_desc
            , "job_sub_cat": job.job_sub_cat
            , "job_name"    : job.job_name
            , "doorstep"    : job.doorstep
            , "job_summary"    : job.job_summary
            , "job_desc"    : job.job_desc
            , "job_features"    : job.job_features
            , "job_symptoms"    : job.job_symptoms
            , "job_vendor"    : job.vendor
            , "default_comp"    : job.default_components
            , "optional_comp"    : job.optional_components
            , "total_price"    : job.total_price
            , "total_part": job.total_part
            , "total_labour": job.total_labour
            , "total_discount": job.total_discount
            , "price_active": job.price_active
            , "total_price_comp"    : job.total_price_comp
            , "time"    : job.time
            , "priority"    : job.priority
        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def add_job_cart(request):
    service_ids = get_param(request,'service_names',None)
    cookieCartData = request.COOKIES.get('cgcart')
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    obj['result']['cart_details'] = []
    cg_price = 0
    cg_part  = 0
    cg_labour = 0
    cg_discount = 0
    comp_price = 0
    cg_price_doorstep = 0
    cg_price_workshop = 0
    car_bike = ""
    jobs = 0
    list_ids = []
    if service_ids !=None:
        list_ids = (json.loads(service_ids))
    elif cookieCartData:
        list_ids = cookieCartData.split(',')

    jobObjs = Services.objects.filter(id__in=list_ids)
    for job in jobObjs:
        jobs = jobs +1
        obj['result']['cart_details'].append({
            "id" :   job.id
            ,"make"	: job.make
            ,"model"    : job.model
            ,"year"    : job.year
            ,"fuel_type"    : job.fuel_type
            , "full_veh_name"    : job.full_veh_name
            , "car_bike"    : job.car_bike
            , "city"    : job.city
            , "service_cat"    : job.service_cat
            # , "service_desc"    : job.service_desc
            , "job_name"    : job.job_name
            , "price_active": job.price_active
            , "doorstep"    : job.doorstep
            , "job_summary"    : job.job_summary
            , "job_desc"    : job.job_desc
            , "job_features"    : job.job_features
            , "job_symptoms"    : job.job_symptoms
            , "job_vendor"    : job.vendor
            , "default_comp"    : job.default_components
            , "optional_comp"    : job.optional_components
            , "total_price"    : job.total_price
            , "total_labour": job.total_labour
            , "total_discount": job.total_discount
            , "total_part": job.total_part
            , "total_price_comp" : job.total_price_comp
            , "time"    : job.time
            , "priority"    : job.priority
        }
        )

        cg_price = float(job.total_price) + cg_price
        car_bike = job.car_bike
        if job.doorstep =="1":
            cg_price_doorstep = float(job.total_price) + cg_price_doorstep
        else:
            cg_price_workshop = float(job.total_price) + cg_price_workshop

        if job.total_part != None:
            cg_part = float(job.total_part) + cg_part
        if job.total_labour != None:
            cg_labour = float(job.total_labour) + cg_labour
        if job.total_discount != None:
            cg_discount = float(job.total_discount) + cg_discount
        comp_price = float(job.total_price_comp) + comp_price

    if comp_price == 0:
        discount = 0
    else:
        discount = (comp_price-cg_price)/comp_price

    obj['result']['cart_summary'] = [{
        "car_bike":car_bike
        ,"cg_amount": cg_price
        ,"cg_amount_doorstep":cg_price_doorstep
        , "cg_amount_workshop": cg_price_workshop
        , "comp_amount": comp_price
        ,"discount": discount
        ,"diff_amount": (comp_price-cg_price)
        , "total_jobs": jobs
        ,"total_labour_cg" :cg_labour
        ,"total_discount_cg":cg_discount
        , "total_part_cg": cg_part
    }]
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def get_location2(request):
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

def get_location(request):
    location_id = get_param(request, 'location_id', None)
    location_delhi="28.6466773,76.813073"
    radius_m = "100000"
    obj = {}
    obj['status'] = False
    obj['result'] = []
    url = "https://maps.googleapis.com/maps/api/place/queryautocomplete/json?key="+ google_map_api_key+"&input="+location_id+"&location="+ location_delhi +"&radius="+radius_m

    # url = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="+location_id+"&types=geocode&language=en&location="+ location_delhi +"&radius="+radius_m+"&key="+ google_map_api_key
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

    # cc = Leads(firstname       = firstname       ,
    #             lastname        = lastname        ,
    #             car_bike        = car_bike        ,
    #             make            = make            ,
    #             model           = model           ,
    #             fuel_type       = fuel_type       ,
    #             service_category= service_category,
    #             additional_request        = additional         ,
    #             address         = address         ,
    #             locality        = locality        ,
    #             date_requested  = date_requested  ,
    #             time_requested  = time_requested  ,
    #             number          = number          ,
    #             email           = email           ,
    #             source          = source          ,
    #             time_stamp      = time_stamp      )
    # cc.save()

    mviews.send_lead(firstname,lastname,car_bike, number,email, make, model, fuel_type, additional, service_category,locality,address,date_requested,time_requested)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def post_message(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}

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

def send_otp_new(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    phn = get_param(request,'phone',None)
    otp = random.randint(1000, 9999)
    otpdatetime = datetime.datetime.now()
    message = "Your ClickGarage one time password is " + str(otp) + ". Please enter the same to complete your mobile verification."
    message = message.replace(" ","+")

    newFlag = False
    username = None
    findOtp     = Otp.objects.filter(mobile=phn)
    if len(findOtp):
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

def checkOTP_new(onetp, mobile):
    check = False
    msg = ''
    curr_time = datetime.datetime.now()
    curr_ts = calendar.timegm(curr_time.timetuple())
    findOtp     = Otp.objects.filter(mobile=mobile)
    if len(findOtp) and findOtp[0].otp:
        findOtp = findOtp[0]
        otp_ts = calendar.timegm(findOtp.updated.timetuple())
        if (curr_ts - otp_ts) > 3600:
            msg = 'Expired OTP'
            # findOtp.otp = ''
            findOtp.updated = curr_time
            findOtp.save()
        elif onetp == findOtp.otp:
            msg = 'Success'
            check = True
            # findOtp.otp = ''
            # if name:
            #     findOtp.username = name
            findOtp.updated = curr_time
            findOtp.save()
        else:
            msg = 'Wrong OTP'
    else:
        msg = 'No active OTP'

    return {'msg': msg, 'status': check}






def create_check_user(name,number):
    if number:
        users = CGUserNew.objects.filter(contact_no=number)
        if len(users):
            return users[0]
        else:
            user_new = CGUserNew(username=number,contact_no=number)
            if name:
                name = name.split(' ')
                user_new.first_name = name[0]
                if len(name) > 1:
                    lname = ""
                    for i in range(1, len(name)):
                        if i == 1 :
                            lname = name[i]
                        else:
                            lname = lname + " " + name[i]
                    user_new.last_name = lname
            user_new.save()
            return user_new

def create_check_user_modified(name,number,owner):
    if number:
        users = CGUserNew.objects.filter(contact_no=number)
        if len(users):
            if owner == "ClickGarage":
                users[0].clickgarage_flag = True
            else:
                if owner not in users[0].owner_user:
                    users[0].owner_user.append(owner)
                users[0].save()
            return users[0]
        else:
            user_new = CGUserNew(username=number,contact_no=number)
            if name:
                name = name.split(' ')
                user_new.first_name = name[0]
                if len(name) > 1:
                    lname = ""
                    for i in range(1, len(name)):
                        if i == 1 :
                            lname = name[i]
                        else:
                            lname = lname + " " + name[i]
                    user_new.last_name = lname
            if owner == "ClickGarage":
                user_new.clickgarage_flag = True
            else:
                user_new.clickgarage_flag = False
                if owner not in user_new.owner_user:
                    user_new.owner_user.append(owner)
            user_new.save()
            return user_new
# def place_lead(request):
#     if request.user.is_authenticated():
#         name        = get_param(request, 'name', None)
#         number      = get_param(request, 'number', None)
#         email       = get_param(request, 'number', None)
#         reg_number  = get_param(request, 'reg_no', None)
#         address     = get_param(request, 'add', None)
#         locality    = get_param(request, 'locality', None)
#         city        = get_param(request, 'city', None)
#         order_list  = get_param(request, 'order_list', None)
#         make        = get_param(request, 'make', None)
#         veh_type    = get_param(request, 'veh_type', None)
#         model       = get_param(request, 'model', None)
#         fuel        = get_param(request, 'fuel', None)
#         date        = get_param(request, 'date', None)
#         time        = get_param(request, 'time', None)
#         comment     = get_param(request, 'comment', None)
#         is_paid     = get_param(request, 'is_paid', None)
#         paid_amt    = get_param(request, 'paid_amt', None)
#         coupon      = get_param(request, 'coupon', None)
#         price_total      = get_param(request, 'price_total', None)
#         status = "Lead Generated"
#         lead_id = 100000
#         tran_len = len(Leads.objects.all())
#         if tran_len > 0:
#             tran = Transactions.objects.all().aggregate(Max('booking_id'))
#             lead_id = int(tran['lead_id__max'] + 1)
#
#         tt = Leads(lead_id              = lead_id                ,
#                             lead_timestamp       = time.time()          ,
#                             cust_id              = request.user.id      ,
#                             cust_name            = name            ,
#                             cust_make            = make            ,
#                             cust_model           = model           ,
#                             cust_vehicle_type    = veh_type,
#                             cust_fuel_varient    = fuel    ,
#                             cust_regnumber       = reg_number       ,
#                             cust_number          = number          ,
#                             cust_email           = email           ,
#                             cust_address         = address         ,
#                             cust_locality        = locality        ,
#                             cust_city            = city            ,
#                             service_items        = order_list        ,
#                             price_total          = price_total          ,
#                             date_booking         = date                ,
#                             follow_up_date       = date         ,
#                             time_booking         = time         ,
#                             is_paid              = is_paid            ,
#                             coupon               =coupon,
#                             amount_paid          =  paid_amt          ,
#                             status               = status             ,
#                             comments             = comment             )
#         tt.save()

# def place_lead(user_id,name,number,email,reg_number,address,locality,city,order_list,make,veh_type,model,fuel,date,time_str,comment,is_paid,paid_amt,coupon,price_total ):
#         status = "Lead Generated"
#         lead_id = 1
#         tran_len = len(Leads.objects.all())
#         if tran_len:
#             tran = Leads.objects.all().aggregate(Max('lead_id'))
#             lead_id = int(tran['lead_id__max'] + 1)
#
#         tt = Leads(lead_id                       = lead_id                ,
#                             lead_timestamp       = time.time()          ,
#                             cust_id              = user_id     ,
#                             cust_name            = name            ,
#                             cust_make            = make            ,
#                             cust_model           = model           ,
#                             cust_vehicle_type    = veh_type,
#                             cust_fuel_varient    = fuel    ,
#                             cust_regnumber       = reg_number       ,
#                             cust_number          = number          ,
#                             cust_email           = email           ,
#                             cust_address         = address         ,
#                             cust_locality        = locality        ,
#                             cust_city            = city            ,
#                             service_items        = order_list        ,
#                             price_total          = price_total          ,
#                             date_booking         = date                ,
#                             follow_up_date       = date         ,
#                             time_booking         = time_str         ,
#                             is_paid              = is_paid            ,
#                             coupon               =coupon,
#                             amount_paid          =  paid_amt          ,
#                             status               = status             ,
#                             comments             = comment             )
#         tt.save()
#         return {'Status': "Order Placed",'lead_id':str(tt.id)}

# booking_flag = models.BooleanField()
# booking_id = models.IntegerField()
# booking_timestamp = models.CharField(max_length=200)
# cust_id = models.CharField(max_length=200)
# cust_name = models.CharField(max_length=200)
# cust_make = models.CharField(max_length=200)
# cust_model = models.CharField(max_length=200)
# cust_vehicle_type = models.CharField(max_length=200)
# cust_fuel_varient = models.CharField(max_length=200)
# cust_regnumber = models.CharField(max_length=200, null=True)
# cust_number = models.CharField(max_length=200)
# cust_email = models.CharField(max_length=200)
# cust_address = models.CharField(max_length=200)
# cust_locality = models.CharField(max_length=200)
# cust_city = models.CharField(max_length=200)
# service_items = ListField(DictField())
# price_total = models.CharField(max_length=200)
# date_booking = models.CharField(max_length=200)
# time_booking = models.CharField(max_length=200)
# is_paid = models.BooleanField()
# customer_comment = models.CharField(max_length=500)
# amount_paid = models.CharField(max_length=200)
# coupon = models.CharField(max_length=200, null=True)
# status = models.CharField(max_length=200)
# comments = models.CharField(max_length=300)
# source = models.CharField(max_length=200)
# done_by = models.CharField(max_length=200)

# print newformat


def place_booking(user_id, name, number, email, reg_number, address, locality, city, order_list, make, veh_type, model,
                  fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon, price_total,source, booking_flag, int_summary,send_sms = "1",booking_type="User",booking_user_name=None,booking_user_number=None, owner="ClickGarage", follow_up_date_book = "",follow_up_time_book = "",odometer=""):

    print email

    name = cleanstring(name).title()
    address = cleanstring(address).title()
    locality = cleanstring(locality).title()
    city = cleanstring(city).title()
    reg_number = cleanstring(reg_number).upper()
    # WMS Modification Start
    if owner == "ClickGarage":
        clickgarage_flag = True
        agent = ""

    else:
        clickgarage_flag = False
        agent = owner
    # WMS Modification End

    if booking_user_name == None:
        booking_user_name = name
    if booking_user_number == None:
        booking_user_number = number
    booking_user_name = cleanstring(booking_user_name).title()

    if booking_flag:
        if owner == "ClickGarage":
            status = "Confirmed"
        else:
            status = "Assigned"
        user = CGUserNew.objects.filter(id=user_id)[0]
        address2 = {'address':address, 'locality':locality, 'city':city}
        if address2 not in user.user_saved_address:
            user.user_saved_address.append(address2)
        vehicle = {'type':veh_type,'make':make,'model':model,'fuel':fuel,"reg_num":reg_number}
        if vehicle not in user.user_veh_list:
            user.user_veh_list.append(vehicle)
        if email not in user.email_list:
            user.email_list.append(email)
        user.email = email
        user.save()
        if follow_up_date_book == "":
            follow_up_date = time.strftime("%Y-%m-%d")
        else:
            follow_up_date = follow_up_date_book
        if follow_up_time_book == "":
            follow_up_time = datetime.time(9,30,0,0)
        else:
            follow_up_time = datetime.time(9, 30, 0, 0)


    else:
        status = "Lead"
        if follow_up_date_book == "":
            follow_up_date = time.strftime("%Y-%m-%d")
        else:
            follow_up_date = follow_up_date_book

        if follow_up_time_book == "":
            follow_up_time = datetime.time(9,30,0,0)
        else:
            follow_up_time = follow_up_time_book

    # import time.strftime("%d/%m/%Y"))
    # update estimate history
    new_estimate_timestamp = time.time()
    estimate_by_id = user_id
    estimate_by_number = number
    estimate_by_name = name
    estimate_history = [{"timestamp": new_estimate_timestamp, "change_by_userid": estimate_by_id,
                         "change_by_number": estimate_by_number, "change_by_name": estimate_by_name,
                         'work_estimate': order_list}]

    # update user

    booking_id = 100000
    tran_len = len(Bookings.objects.all())
    if tran_len:
        tran = Bookings.objects.all().aggregate(Max('booking_id'))
        booking_id = int(tran['booking_id__max'] + 1)

    tt= Bookings(booking_flag           = booking_flag  ,
                 booking_id             =booking_id      ,
                 booking_timestamp      =time.time()     ,
                 cust_id                =user_id         ,
                 cust_name              =name            ,
                 cust_make              =make            ,
                 cust_model             =model           ,
                 cust_vehicle_type      =veh_type        ,
                 cust_fuel_varient      =fuel            ,
                 cust_regnumber         =reg_number      ,
                 cust_number            =number           ,
                 cust_email             =email            ,
                 cust_address           =address          ,
                 cust_locality          =locality         ,
                 cust_city              =city             ,
                 service_items          =order_list       ,
                 price_total            =price_total      ,
                 date_booking           =date              ,
                 time_booking           =time_str          ,
                 is_paid                =is_paid           ,
                 amount_paid            =paid_amt          ,
                 coupon                 =coupon            ,
                 status                 =status            ,
                 jobssummary  = jobsummary_list,
                 # comments               =comment           ,
                 source                 =source           ,
                 agent                  =    agent             ,
                 booking_user_type      =   booking_type,
                 booking_user_name      = booking_user_name,
                 booking_user_number    =  booking_user_number,
                 date_delivery = date,
                 # lead_follow_up_date = follow_up_date,
                 estimate_history    =estimate_history,
                 clickgarage_flag = clickgarage_flag,
                 booking_owner = owner,
                 follow_up_date = follow_up_date,
                 follow_up_time = follow_up_time,
                 odometer = odometer)
    tt.save()

    send_sms_bool = True
    if clickgarage_flag:
        if send_sms == "1":
            send_sms_bool = True
        else:
            send_sms_bool = False
    else:
        user1 = CGUserNew.objects.filter(id=agent)
        sms_credits = user1.agent_sms_credits
        credits_per_message = 1
        num_sms = 1
        if num_sms <= sms_credits:
            send_sms_bool = True
            num_sms_left = sms_credits - 1
            user1.agent_sms_credits = num_sms_left
            user1.save()
        else:
            send_sms_bool = False


    if send_sms_bool:
        mviews.send_booking_confirm(email=email,name=name,booking_id=booking_id,number=number, service_list= int_summary, car_bike=veh_type)
    if clickgarage_flag:
        mviews.send_booking(firstname=name,lastname ="", number=number,email=email, car_bike=veh_type, make=make, model=model, fuel_type=fuel,locality=locality,address=address,date_requested=date,time_requested=time_str)
    return {'Status': "Order Placed", 'booking_id': str(tt.booking_id),'price_total':str(tt.price_total),'Summary':str(tt.comments), 'id':str(tt.id)}
#
# def send_otp_booking(request):
#     name = get_param(request, 'name', None)
#     number = get_param(request, 'number', None)
#     email = get_param(request, 'email', None)
#     reg_number = get_param(request, 'reg_number', None)
#     address = get_param(request, 'address', None)
#     locality = get_param(request, 'locality', None)
#     city = get_param(request, 'city', None)
#     order_list = get_param(request, 'order_list', None)
#     if order_list:
#         order_list = json.loads(order_list)
#     else:
#         order_list = []
#     make = get_param(request, 'make', None)
#     veh_type = get_param(request, 'veh_type', None)
#     model = get_param(request, 'model', None)
#     fuel = get_param(request, 'fuel', None)
#     date = get_param(request, 'date', None)
#     time_str = get_param(request, 'time', None)
#     comment = get_param(request, 'comment', None)
#     is_paid = get_param(request, 'is_paid', None)
#     paid_amt = get_param(request, 'paid_amt', None)
#     coupon = get_param(request, 'coupon', None)
#     price_total = get_param(request, 'price_total', None)
#     onetp = get_param(request,'otp',None)
#     source = get_param(request,'source',None)
#     booking_flag = False
#     oldformat = date
#     datetimeobject = datetime.datetime.strptime(oldformat, '%d-%m-%Y')
#     newformat = datetimeobject.strftime('%Y-%m-%d')
#     date =newformat
#
#     booking = ''
#     obj = checkOTP_new(onetp, number)
#     if obj['status']:
#         user = create_check_user(name,number)
#         if not request.user or request.user.is_anonymous():
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             login(request, user)
#         booking = place_booking(str(user.id), name, number, email, reg_number, address, locality, city, order_list, make,
#                                 veh_type, model, fuel, date, time_str, comment, is_paid, paid_amt, coupon, price_total,source,booking_flag)
#         obj['result'] = {}
#         obj['result']['userid'] = request.user.id
#         obj['result']['booking'] = booking
#         if request.user.first_name and len(request.user.first_name):
#             obj['result']['username'] = request.user.first_name
#         else:
#             obj['result']['username'] = request.user.username
#         obj['result']['auth'] = True
#     else:
#         obj['status'] = True
#         obj['result'] = {}
#         obj['result']['auth'] = False
#         obj['result']['msg'] = obj['msg']
#     return HttpResponse(json.dumps(obj), content_type='application/json')

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires)

def verify_otp_password_cookie(request):
    obj = {}
    obj['status'] = False
    number = get_param(request, 'number', None)
    password = get_param(request,'pass',None)
    onetp = get_param(request,'otp',None)
    objtp = checkOTP_new(onetp, number)
    message = ''
    obj['status'] = False
    obj['result'] = {}
    login_flag = False
    cookieUserData = request.COOKIES.get('c_user_id')
    if cookieUserData:
        user = CGUserNew.objects.get(id=cookieUserData)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        login_flag = True
        obj['result']['userid'] = user.id
        obj['result']['username'] = user.username
        obj['result']['agent_sms_credits'] = user.agent_sms_credits
        obj['result']['auth'] = True
        obj['result']['email_list'] = user.email_list
        obj['result']['email_primary'] = user.email
        obj['result']['phone'] = user.contact_no
        obj['result']['first_name'] = user.first_name
        obj['result']['last_name'] = user.last_name
        obj['result']['agent'] = user.is_agent
        obj['result']['user'] = user.is_user
        obj['result']['admin'] = user.is_admin
        obj['result']['staff'] = user.is_staff
        obj['result']['b2b'] = user.is_b2b
        obj['result']['user_address_list'] = user.user_saved_address
        obj['result']['user_vehicles'] = user.user_veh_list
        obj['result']['user_state'] = user.user_state
        obj['result']['agent_cin'] = user.agent_cin
        obj['result']['agent_stax'] = user.agent_stax
        obj['result']['agent_vat'] = user.agent_vat
        obj['result']['clickgarage_flag'] = user.clickgarage_flag
        obj['result']['owner_user'] = user.owner_user
        obj['result']['date_joined'] = str(user.date_joined)
        obj['result']['user_address'] = user.user_address
        obj['result']['user_locality'] = user.user_locality
        obj['result']['user_city'] = user.user_city
        if user.user_state != "":
            taxes = get_tax(user.user_state)
            if len(taxes['result']):
                obj['result']['vat_parts'] = taxes['result'][0]['vat_parts']
                obj['result']['vat_consumables'] = taxes['result'][0]['vat_consumables']
                obj['result']['vat_lube'] = taxes['result'][0]['vat_lube']
                obj['result']['service_tax'] = taxes['result'][0]['service_tax']

        message = "Success"
    else:
        try:
            user = CGUserNew.objects.get(username=number)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            if user.check_password(password):
                login(request, user)
                login_flag = True
                obj['result']['userid'] = user.id
                obj['result']['username'] = user.username
                obj['result']['auth'] = True
                obj['result']['agent_sms_credits'] = user.agent_sms_credits
                obj['result']['email_list'] = user.email_list
                obj['result']['email_primary'] = user.email
                obj['result']['phone'] = user.contact_no
                obj['result']['first_name'] = user.first_name
                obj['result']['last_name'] = user.last_name
                obj['result']['agent'] = user.is_agent
                obj['result']['user'] = user.is_user
                obj['result']['admin'] = user.is_admin
                obj['result']['staff'] = user.is_staff
                obj['result']['b2b'] = user.is_b2b
                obj['result']['user_address_list'] = user.user_saved_address
                obj['result']['user_vehicles'] = user.user_veh_list
                obj['result']['user_state'] = user.user_state
                obj['result']['agent_cin'] = user.agent_cin
                obj['result']['agent_stax'] = user.agent_stax
                obj['result']['agent_vat'] = user.agent_vat
                obj['result']['clickgarage_flag'] = user.clickgarage_flag
                obj['result']['owner_user'] = user.owner_user
                obj['result']['date_joined'] = str(user.date_joined)
                obj['result']['user_address'] = user.user_address
                obj['result']['user_locality'] = user.user_locality
                obj['result']['user_city'] = user.user_city
                if user.user_state != "":
                    taxes = get_tax(user.user_state)
                    if len(taxes['result']):
                        obj['result']['vat_parts'] = taxes['result'][0]['vat_parts']
                        obj['result']['vat_consumables'] = taxes['result'][0]['vat_consumables']
                        obj['result']['vat_lube'] = taxes['result'][0]['vat_lube']
                        obj['result']['service_tax'] = taxes['result'][0]['service_tax']

                message = "Success"
            elif objtp['status']:
                login(request, user)
                login_flag = True
                obj['result']['userid'] = user.id
                obj['result']['username'] = user.username
                obj['result']['auth'] = True
                obj['result']['agent_sms_credits'] = user.agent_sms_credits
                obj['result']['email_list'] = user.email_list
                obj['result']['email_primary'] = user.email
                obj['result']['phone'] = user.contact_no
                obj['result']['first_name'] = user.first_name
                obj['result']['last_name'] = user.last_name
                obj['result']['agent'] = user.is_agent
                obj['result']['user'] = user.is_user
                obj['result']['admin'] = user.is_admin
                obj['result']['staff'] = user.is_staff
                obj['result']['b2b'] = user.is_b2b
                obj['result']['user_address_list'] = user.user_saved_address
                obj['result']['user_vehicles'] = user.user_veh_list
                obj['result']['user_state'] = user.user_state
                obj['result']['agent_cin'] = user.agent_cin
                obj['result']['agent_stax'] = user.agent_stax
                obj['result']['agent_vat'] = user.agent_vat
                obj['result']['clickgarage_flag'] = user.clickgarage_flag
                obj['result']['owner_user'] = user.owner_user
                obj['result']['date_joined'] = str(user.date_joined)
                obj['result']['user_address'] = user.user_address
                obj['result']['user_locality'] = user.user_locality
                obj['result']['user_city'] = user.user_city

                message = "Success"
            else:
                obj['result']['auth'] = False
                message = "Login Failed!"
        except CGUserNew.DoesNotExist:
            user = None
            message = "User Doesn't exist"
            obj['result']['auth'] = False
    obj['result']['msg'] = message
    obj['status'] = True
    admin_status = None

    # print request.user.username
    # print admin_status

    if login_flag:
        if request.user.username in superadmin:
            admin_status = True
        else:
            admin_status = request.user.is_admin
        obj['result']['auth_rights'] = {'admin': admin_status, 'b2b': request.user.is_b2b,
                                        'agent': request.user.is_agent,
                                        'staff': request.user.is_staff}
    else:
        obj['result']['auth_rights'] = {'admin': False, 'b2b': False,
                                        'agent': False,
                                        'staff': False}

    response = HttpResponse(json.dumps(obj), content_type='application/json')
    # try:
    # print (user.is_authenticated())
    if obj['result']['auth']:
        set_cookie(response,"c_user_id", user.id)
        set_cookie(response, "c_user_first_name", user.first_name)
        set_cookie(response, "c_user_last_name", user.last_name)
        set_cookie(response, "c_user_number", user.contact_no)
        try:
            set_cookie(response, "c_user_email", user.email)
            set_cookie(response, "c_user_address", user.user_saved_address[0]['address'])
            set_cookie(response, "c_user_locality", user.user_saved_address[0]['locality'])
            set_cookie(response, "c_user_city", user.user_saved_address[0]['city'])
        except:
            None
    return response



def set_password_otp(request):
    obj = {}
    obj['status'] = False
    number = get_param(request, 'number', None)
    # name = get_param(request, 'name', None)
    pass2 = get_param(request,'pass',None)
    onetp = get_param(request,'otp',None)
    objtp = checkOTP_new(onetp, number)
    message = ''
    obj['status'] = False
    obj['result'] = {}
    try:
        user = CGUserNew.objects.get(username=number)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        if objtp['status']:
            obj['result']['userid'] = user.id
            obj['result']['username'] = user.username
            user.set_password(pass2)
            user.save()
            login(request, user)
            obj['result']['auth'] = True
            obj['result']['pass'] = pass2
            message = "Success"
        else:
            obj['result']['auth'] = False
            message = objtp['msg']
    except CGUserNew.DoesNotExist:
        user = None
        message = "User Doesn't exist"
        obj['result']['auth'] = False
    obj['result']['msg'] = message
    obj['status'] = True
    response = HttpResponse(json.dumps(obj), content_type='application/json')
    # try:
    if obj['result']['auth']:
        set_cookie(response,"c_user_id", user.id)
        set_cookie(response, "c_user_first_name", user.first_name)
        set_cookie(response, "c_user_last_name", user.last_name)
        set_cookie(response, "c_user_number", user.contact_no)
        try:
            set_cookie(response, "c_user_email", user.email)
            set_cookie(response, "c_user_address", user.user_saved_address[0]['address'])
            set_cookie(response, "c_user_locality", user.user_saved_address[0]['locality'])
            set_cookie(response, "c_user_city", user.user_saved_address[0]['city'])
        except:
            None
    return response

def sign_up_otp(request):
    obj = {}
    obj['status'] = False
    number = get_param(request, 'number', None)
    name = get_param(request, 'name', None)
    password = get_param(request,'pass',None)
    onetp = get_param(request,'otp',None)
    objtp = checkOTP_new(onetp, number)
    message = ''
    obj['status'] = False
    obj['result'] = {}
    # try:
    if objtp['status']:
        user = create_check_user(name, number)
        user.set_password(password)
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        obj['result']['userid'] = user.id
        obj['result']['username'] = user.username
        obj['result']['auth'] = True
        message = "Success"
    else:
        obj['result']['auth'] = False
        message = objtp['msg']
    obj['result']['msg'] = message
    obj['status'] = True
    response = HttpResponse(json.dumps(obj), content_type='application/json')

    if obj['result']['auth']:
        set_cookie(response,"c_user_id", user.id)
        set_cookie(response, "c_user_first_name", user.first_name)
        set_cookie(response, "c_user_last_name", user.last_name)
        set_cookie(response, "c_user_number", user.contact_no)
        try:
            set_cookie(response, "c_user_email", user.email)
            set_cookie(response, "c_user_address", user.user_saved_address[0]['address'])
            set_cookie(response, "c_user_locality", user.user_saved_address[0]['locality'])
            set_cookie(response, "c_user_city", user.user_saved_address[0]['city'])
        except:
            None
    return response

def logout_view(request):
    # path = get_param(request, 'path', None)
    logout(request)
    # return redirect(path)

# Exotel calling start
sid = "clickgarage1"
token = "bca1fb4bbe89339878eb1e08aee88f30aed8a39f"
callerid = "01139585428"
# calltype='trans'
calltype='promo'

from pprint import pprint
def connect_customer_to_agent_exo(agent_no, customer_no, timelimit=None, timeout=None):
    return requests.post('https://twilix.exotel.in/v1/Accounts/{sid}/Calls/connect.json'.format(sid=sid),
                         auth=(sid, token),
                         data= {
                             'From': agent_no,
                             'To': customer_no,
                             'CallerId': callerid,
                             'TimeLimit': timelimit,
                             'TimeOut': timeout,
                             'CallType': calltype
                         })

def call_customer(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    agent_no = request.user.contact_no
    cust_no  = get_param(request, 'cust_no', None)
    exocall = connect_customer_to_agent_exo(agent_no= agent_no,customer_no= cust_no)
    print agent_no
    print cust_no
    print exocall.status_code
    pprint(exocall.json())
    # obj['result']['exotel'] = r.json()
    # obj['result']['status'] = exocall.status_code
    obj['status'] = True
    response = HttpResponse(json.dumps(obj), content_type='application/json')
    return response

# if __name__ == '__main__':
#     r = connect_customer_to_agent(
#         sid, token,
#         agent_no="<First-phone-number-to-call (Your agent's number)>",
#         customer_no="<Second-phone-number-to-call (Your customer's number)>",
#         callerid="<Your-Exotel-virtual-number>",
#         timelimit="<time-in-seconds>",  # This is optional
#         timeout="<time-in-seconds>",  # This is also optional
#         calltype="trans"  # Can be "trans" for transactional and "promo" for promotional content
#         )
#     print r.status_code
#     pprint(r.json())

# Exotel calling end


def analyse_bookings(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    date = get_param(request, 'date', None)
    car_bike = get_param(request,'car_bike',None)
    monthyear = get_param(request, 'monthyear', None)
    is_agent = request.user.is_agent
    is_staff = request.user.is_staff
    is_admin = request.user.is_admin
    is_b2b = request.user.is_b2b
    if request.user.is_admin or request.user.is_staff:
        tranObjs = Bookings.objects.filter(clickgarage_flag = True).order_by('-booking_id')
        custObjs = CGUserNew.objects.filter(clickgarage_flag = True)
    elif request.user.is_b2b:
        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('-booking_id')
        custObjs = CGUserNew.objects.filter(owner_user=request.user.id)
    elif request.user.is_agent:
        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('-booking_id')
        custObjs = CGUserNew.objects.filter(owner_user=request.user.id)
    else:
        tranObjs = None
        custObjs = None

    if car_bike == None and monthyear == None and date == None:
        expenseObjs = Expenses.objects.filter()
    else:
        expenseObjs = None


    if car_bike != None and car_bike != "":
        tranObjs = tranObjs.filter(cust_vehicle_type=car_bike)

    if date != None and date != "":
        year = date[6:10]
        month = date[3:5]
        day = date[0:2]
        tranObjs = tranObjs.filter(date_booking=datetime.date(int(year), int(month), int(day)))
        custObjs = custObjs.filter(date_joined =datetime.date(int(year), int(month), int(day)) )
    if monthyear != None and monthyear != "":
        year = monthyear[0:4]
        month = monthyear[4:6]
        # print year
        # print month
        if month in ['01','03','05','07','08','10','12']:
            day = 31
        elif (month == "02" and (int(year) % 4) == 0):
            day = 29
        elif month == "02":
            day = 28
        else:
            day = 30
        start_date = datetime.date(int(year), int(month), 1)
        end_date = datetime.date(int(year), int(month), day)
        tranObjs = tranObjs.filter(date_booking__range=(start_date, end_date))
        custObjs = custObjs.filter(date_joined__range=(start_date, end_date))
    num_users = 0

    num_lead_lead = 0
    vol_lead_lead = 0
    num_warm_lead = 0
    vol_warm_lead = 0
    num_cold_lead = 0
    vol_cold_lead = 0

    num_confirmed_booking = 0
    vol_confirmed_booking = 0
    num_assigned_booking = 0
    vol_assigned_booking = 0
    num_reachedworkshop_booking = 0
    vol_reachedworkshop_booking = 0
    num_estimateshared_booking = 0
    vol_estimateshared_booking = 0
    num_engineerleft_booking = 0
    vol_engineerleft_booking = 0

    num_cancelled_lead = 0
    vol_cancelled_lead = 0
    num_cancelled_booking = 0
    vol_cancelled_booking = 0
    num_escalation_booking = 0
    num_jobcompleted_booking = 0
    num_feedbacktaken_booking = 0

    num_completed = 0
    vol_googleadwords_completed = 0
    num_googleadwords_completed = 0
    vol_repeatcustomer_completed = 0
    num_repeatcustomer_completed = 0
    vol_employeereferral_completed = 0
    num_employeereferral_completed = 0
    vol_externalreferral_completed = 0
    num_externalreferral_completed = 0
    vol_justdial_completed = 0
    num_justdial_completed = 0
    vol_pamphlet_completed = 0
    num_pamphlet_completed = 0
    vol_autoadvertisement_completed = 0
    num_autoadvertisement_completed = 0
    vol_on_groundmarketing_completed = 0
    num_on_groundmarketing_completed = 0
    vol_sulekha_completed = 0
    num_sulekha_completed = 0
    vol_database_coldcalling_completed = 0
    num_database_coldcalling_completed = 0
    vol_chat_completed = 0
    num_chat_completed = 0
    vol_b2b_completed = 0
    num_b2b_completed = 0
    vol_partner_droom_completed = 0
    num_partner_droom_completed = 0
    vol_partner_wishup_completed = 0
    num_partner_wishup_completed = 0
    vol_partner_housejoy_completed = 0
    num_partner_housejoy_completed = 0
    vol_walkin_completed = 0
    num_walkin_completed = 0
    vol_partner_mrright_completed = 0
    num_partner_mrright_completed = 0
    vol_websearch_completed = 0
    num_websearch_completed = 0
    vol_unknown_completed = 0
    num_unknown_completed = 0
    vol_societycamps_completed = 0
    num_societycamps_completed = 0
    vol_checkupcamps_completed = 0
    num_checkupcamps_completed = 0
    vol_signuplead_completed = 0
    num_signuplead_completed = 0
    vol_facebookad_completed = 0
    num_facebookad_completed = 0
    vol_mahindraauthorized_completed = 0
    num_mahindraauthorized_completed = 0
    vol_exotel_completed = 0
    num_exotel_completed = 0
    vol_other_completed = 0
    num_other_completed = 0
    vol_total_lead = 0
    num_total_lead = 0
    vol_googleadwords_lead = 0
    num_googleadwords_lead = 0
    vol_repeatcustomer_lead = 0
    num_repeatcustomer_lead = 0
    vol_employeereferral_lead = 0
    num_employeereferral_lead = 0
    vol_externalreferral_lead = 0
    num_externalreferral_lead = 0
    vol_justdial_lead = 0
    num_justdial_lead = 0
    vol_pamphlet_lead = 0
    num_pamphlet_lead = 0
    vol_autoadvertisement_lead = 0
    num_autoadvertisement_lead = 0
    vol_on_groundmarketing_lead = 0
    num_on_groundmarketing_lead = 0
    vol_sulekha_lead = 0
    num_sulekha_lead = 0
    vol_database_coldcalling_lead = 0
    num_database_coldcalling_lead = 0
    vol_chat_lead = 0
    num_chat_lead = 0
    vol_b2b_lead = 0
    num_b2b_lead = 0
    vol_partner_droom_lead = 0
    num_partner_droom_lead = 0
    vol_partner_wishup_lead = 0
    num_partner_wishup_lead = 0
    vol_partner_housejoy_lead = 0
    num_partner_housejoy_lead = 0
    vol_walkin_lead = 0
    num_walkin_lead = 0
    vol_partner_mrright_lead = 0
    num_partner_mrright_lead = 0
    vol_websearch_lead = 0
    num_websearch_lead = 0
    vol_unknown_lead = 0
    num_unknown_lead = 0
    vol_societycamps_lead = 0
    num_societycamps_lead = 0
    vol_checkupcamps_lead = 0
    num_checkupcamps_lead = 0
    vol_signuplead_lead = 0
    num_signuplead_lead = 0
    vol_facebookad_lead = 0
    num_facebookad_lead = 0
    vol_mahindraauthorized_lead = 0
    num_mahindraauthorized_lead = 0
    vol_exotel_lead = 0
    num_exotel_lead = 0
    vol_other_lead = 0
    num_other_lead = 0
    vol_completed = 0
    vol_part_completed = 0
    vol_labour_completed = 0
    vol_consumable_completed = 0
    vol_lube_completed = 0
    nps_completed = 0
    vol_b2b_total_completed = 0
    num_b2b_total_completed = 0
    vol_b2c_total_completed = 0
    num_b2c_total_completed = 0
    vol_b2b_total_lead = 0
    num_b2b_total_lead = 0
    vol_b2c_total_lead = 0
    num_b2c_total_lead = 0
    Promoters = 0
    Detractors = 0
    Passives = 0
    vol_total_expense = 0
    vol_googleadwords_expense = 0
    vol_repeatcustomer_expense = 0
    vol_employeereferral_expense = 0
    vol_externalreferral_expense = 0
    vol_justdial_expense = 0
    vol_pamphlet_expense = 0
    vol_autoadvertisement_expense = 0
    vol_on_groundmarketing_expense = 0
    vol_sulekha_expense = 0
    vol_database_coldcalling_expense = 0
    vol_chat_expense = 0
    vol_b2b_expense = 0
    vol_partner_droom_expense = 0
    vol_partner_wishup_expense = 0
    vol_partner_housejoy_expense = 0
    vol_walkin_expense = 0
    vol_partner_mrright_expense = 0
    vol_websearch_expense = 0
    vol_unknown_expense = 0
    vol_societycamps_expense = 0
    vol_checkupcamps_expense = 0
    vol_signuplead_expense = 0
    vol_facebookad_expense = 0
    vol_mahindraauthorized_expense = 0
    vol_exotel_expense = 0
    vol_other_expense = 0

    if len(custObjs):
        print len(custObjs)
        for cust in custObjs:
            num_users = num_users + 1

    if expenseObjs != None:
        for expense in expenseObjs:
            if expense.category == "Marketing":
                if expense.sub_category == "Google Adwords":
                    vol_googleadwords_expense = vol_googleadwords_expense + float(expense.amount)
                elif expense.sub_category == "Repeat Customer":
                    vol_repeatcustomer_expense = vol_repeatcustomer_expense + float(expense.amount)
                elif expense.sub_category == "Employee Referral":
                    vol_employeereferral_expense = vol_employeereferral_expense + float(expense.amount)
                elif expense.sub_category == "External Referral":
                    vol_externalreferral_expense = vol_externalreferral_expense + float(expense.amount)
                elif expense.sub_category == "JustDial":
                    vol_justdial_expense = vol_justdial_expense + float(expense.amount)
                elif expense.sub_category == "Pamphlet":
                    vol_pamphlet_expense = vol_pamphlet_expense + float(expense.amount)
                elif expense.sub_category == "Auto Advertisement":
                    vol_autoadvertisement_expense = vol_autoadvertisement_expense + float(expense.amount)
                elif expense.sub_category == "On-Ground Marketing":
                    vol_on_groundmarketing_expense = vol_on_groundmarketing_expense + float(expense.amount)
                elif expense.sub_category == "Sulekha":
                    vol_sulekha_expense = vol_sulekha_expense + float(expense.amount)
                elif expense.sub_category == "Database - Cold Calling":
                    vol_database_coldcalling_expense = vol_database_coldcalling_expense + float(expense.amount)
                elif expense.sub_category == "Chat":
                    vol_chat_expense = vol_chat_expense + float(expense.amount)
                elif expense.sub_category == "B2B":
                    vol_b2b_expense = vol_b2b_expense + float(expense.amount)
                elif expense.sub_category == "Partner - Droom":
                    vol_partner_droom_expense = vol_partner_droom_expense + float(expense.amount)
                elif expense.sub_category == "Partner - Wishup":
                    vol_partner_wishup_expense = vol_partner_wishup_expense + float(expense.amount)
                elif expense.sub_category == "Partner - Housejoy":
                    vol_partner_housejoy_expense = vol_partner_housejoy_expense + float(expense.amount)
                elif expense.sub_category == "Walk in ":
                    vol_walkin_expense = vol_walkin_expense + float(expense.amount)
                elif expense.sub_category == "Partner - Mr Right":
                    vol_partner_mrright_expense = vol_partner_mrright_expense + float(expense.amount)
                elif expense.sub_category == "Web Search":
                    vol_websearch_expense = vol_websearch_expense + float(expense.amount)
                elif expense.sub_category == "Unknown":
                    vol_unknown_expense = vol_unknown_expense + float(expense.amount)
                elif expense.sub_category == "Society camps":
                    vol_societycamps_expense = vol_societycamps_expense + float(expense.amount)
                elif expense.sub_category == "Check up camps":
                    vol_checkupcamps_expense = vol_checkupcamps_expense + float(expense.amount)
                elif expense.sub_category == "Sign up lead":
                    vol_signuplead_expense = vol_signuplead_expense + float(expense.amount)
                elif expense.sub_category == "Facebook Ad":
                    vol_facebookad_expense = vol_facebookad_expense + float(expense.amount)
                elif expense.sub_category == "Mahindra Authorized":
                    vol_mahindraauthorized_expense = vol_mahindraauthorized_expense + float(expense.amount)
                elif expense.sub_category == "Exotel":
                    vol_exotel_expense = vol_exotel_expense + float(expense.amount)
                else:
                    vol_other_expense = vol_other_expense + float(expense.amount)


    if len(tranObjs):
        for trans in tranObjs:
            # if trans.clickgarage_flag == True:
            if trans.status == "Lead":
                num_lead_lead               = num_lead_lead + 1
                for item in trans.service_items:
                    vol_lead_lead           = vol_lead_lead + float(item['price'])

            elif trans.status == "Warm":
                num_warm_lead               = num_warm_lead + 1
                for item in trans.service_items:
                    vol_warm_lead         = vol_warm_lead + float(item['price'])

            elif trans.status == "Cold":
                num_cold_lead = num_cold_lead + 1
                for item in trans.service_items:
                    vol_cold_lead = vol_cold_lead + float(item['price'])


            elif trans.status == "Confirmed":
                num_confirmed_booking = num_confirmed_booking + 1
                for item in trans.service_items:
                    vol_confirmed_booking = vol_confirmed_booking + float(item['price'])


            elif trans.status == "Assigned":
                num_assigned_booking = num_assigned_booking + 1
                for item in trans.service_items:
                    vol_assigned_booking = vol_assigned_booking + float(item['price'])


            elif trans.status == "Reached Workshop":
                num_reachedworkshop_booking = num_reachedworkshop_booking + 1
                for item in trans.service_items:
                    vol_reachedworkshop_booking = vol_reachedworkshop_booking + float(item['price'])


            elif trans.status == "Estimate Shared":
                num_estimateshared_booking = num_estimateshared_booking + 1
                for item in trans.service_items:
                    vol_estimateshared_booking = vol_estimateshared_booking + float(item['price'])

            elif trans.status == "Engineer Left":
                num_engineerleft_booking = num_engineerleft_booking + 1
                for item in trans.service_items:
                    vol_engineerleft_booking = vol_engineerleft_booking + float(item['price'])

            elif trans.status == "Cancelled":
                if trans.booking_flag == False:
                    num_cancelled_lead = num_cancelled_lead + 1
                    for item in trans.service_items:
                        vol_cancelled_lead = vol_cancelled_lead + float(item['price'])
                else:
                    num_cancelled_booking = num_cancelled_booking + 1
                    for item in trans.service_items:
                        vol_cancelled_booking = vol_cancelled_booking + float(item['price'])

            elif trans.status == "Escalation":
                num_escalation_booking = num_escalation_booking + 1

            elif trans.status == "Job Completed" or trans.status == "Feedback Taken":
                if trans.status == "Job Completed":
                    num_jobcompleted_booking = num_jobcompleted_booking + 1
                elif trans.status == "Feedback Taken":
                    num_feedbacktaken_booking = num_feedbacktaken_booking + 1

                num_completed = num_completed + 1
                if trans.source == "Google Adwords":
                    vol_googleadwords_completed = vol_googleadwords_completed + float(trans.price_total)
                    num_googleadwords_completed = num_googleadwords_completed + 1
                elif trans.source == "Repeat Customer":
                    vol_repeatcustomer_completed = vol_repeatcustomer_completed + float(trans.price_total)
                    num_repeatcustomer_completed = num_repeatcustomer_completed + 1
                elif trans.source == "Employee Referral":
                    vol_employeereferral_completed = vol_employeereferral_completed + float(trans.price_total)
                    num_employeereferral_completed = num_employeereferral_completed + 1
                elif trans.source == "External Referral":
                    vol_externalreferral_completed = vol_externalreferral_completed + float(trans.price_total)
                    num_externalreferral_completed = num_externalreferral_completed + 1
                elif trans.source == "JustDial":
                    vol_justdial_completed = vol_justdial_completed + float(trans.price_total)
                    num_justdial_completed = num_justdial_completed + 1
                elif trans.source == "Pamphlet":
                    vol_pamphlet_completed = vol_pamphlet_completed + float(trans.price_total)
                    num_pamphlet_completed = num_pamphlet_completed + 1
                elif trans.source == "Auto Advertisement":
                    vol_autoadvertisement_completed = vol_autoadvertisement_completed + float(trans.price_total)
                    num_autoadvertisement_completed = num_autoadvertisement_completed + 1
                elif trans.source == "On-Ground Marketing":
                    vol_on_groundmarketing_completed = vol_on_groundmarketing_completed + float(trans.price_total)
                    num_on_groundmarketing_completed = num_on_groundmarketing_completed + 1
                elif trans.source == "Sulekha":
                    vol_sulekha_completed = vol_sulekha_completed + float(trans.price_total)
                    num_sulekha_completed = num_sulekha_completed + 1
                elif trans.source == "Database - Cold Calling":
                    vol_database_coldcalling_completed = vol_database_coldcalling_completed + float(trans.price_total)
                    num_database_coldcalling_completed = num_database_coldcalling_completed + 1
                elif trans.source == "Chat":
                    vol_chat_completed = vol_chat_completed + float(trans.price_total)
                    num_chat_completed = num_chat_completed + 1
                elif trans.source == "B2B":
                    vol_b2b_completed = vol_b2b_completed + float(trans.price_total)
                    num_b2b_completed = num_b2b_completed + 1
                elif trans.source == "Partner - Droom":
                    vol_partner_droom_completed = vol_partner_droom_completed + float(trans.price_total)
                    num_partner_droom_completed = num_partner_droom_completed + 1
                elif trans.source == "Partner - Wishup":
                    vol_partner_wishup_completed = vol_partner_wishup_completed + float(trans.price_total)
                    num_partner_wishup_completed = num_partner_wishup_completed + 1
                elif trans.source == "Partner - Housejoy":
                    vol_partner_housejoy_completed = vol_partner_housejoy_completed + float(trans.price_total)
                    num_partner_housejoy_completed = num_partner_housejoy_completed + 1
                elif trans.source == "Walk in ":
                    vol_walkin_completed = vol_walkin_completed + float(trans.price_total)
                    num_walkin_completed = num_walkin_completed + 1
                elif trans.source == "Partner - Mr Right":
                    vol_partner_mrright_completed = vol_partner_mrright_completed + float(trans.price_total)
                    num_partner_mrright_completed = num_partner_mrright_completed + 1
                elif trans.source == "Web Search":
                    vol_websearch_completed = vol_websearch_completed + float(trans.price_total)
                    num_websearch_completed = num_websearch_completed + 1
                elif trans.source == "Unknown":
                    vol_unknown_completed = vol_unknown_completed + float(trans.price_total)
                    num_unknown_completed = num_unknown_completed + 1
                elif trans.source == "Society camps":
                    vol_societycamps_completed = vol_societycamps_completed + float(trans.price_total)
                    num_societycamps_completed = num_societycamps_completed + 1
                elif trans.source == "Check up camps":
                    vol_checkupcamps_completed = vol_checkupcamps_completed + float(trans.price_total)
                    num_checkupcamps_completed = num_checkupcamps_completed + 1
                elif trans.source == "Sign up lead":
                    vol_signuplead_completed = vol_signuplead_completed + float(trans.price_total)
                    num_signuplead_completed = num_signuplead_completed + 1
                elif trans.source == "Facebook Ad":
                    vol_facebookad_completed = vol_facebookad_completed + float(trans.price_total)
                    num_facebookad_completed = num_facebookad_completed + 1
                elif trans.source == "Mahindra Authorized":
                    vol_mahindraauthorized_completed = vol_mahindraauthorized_completed + float(trans.price_total)
                    num_mahindraauthorized_completed = num_mahindraauthorized_completed + 1
                elif trans.source == "Exotel":
                    vol_exotel_completed = vol_exotel_completed + float(trans.price_total)
                    num_exotel_completed = num_exotel_completed + 1
                else:
                    vol_other_completed = vol_other_completed + float(trans.price_total)
                    num_other_completed = num_other_completed + 1

                for item in trans.service_items:
                    vol_completed = vol_completed + float(item['price'])
                    try:
                        if item['type'] == "Part":
                            vol_part_completed = vol_part_completed + float(item['price'])
                        elif item['type'] == "Labour":
                            vol_labour_completed = vol_labour_completed + float(item['price'])
                        elif item['type'] == "Consumable":
                            vol_consumable_completed = vol_consumable_completed + float(item['price'])
                        elif item['type'] == "Lube":
                            vol_lube_completed = vol_lube_completed + float(item['price'])
                    except:
                        vol_labour_completed = vol_labour_completed + float(item['price'])

                if trans.booking_user_type == "B2B" or trans.source == "B2B":
                    vol_b2b_total_completed = vol_b2b_total_completed + float(trans.price_total)
                    num_b2b_total_completed = num_b2b_total_completed + 1

                else:
                    vol_b2c_total_completed = vol_b2c_total_completed + float(trans.price_total)
                    num_b2c_total_completed = num_b2c_total_completed + 1


            vol_total_lead = vol_total_lead + float(trans.price_total)
            num_total_lead = num_total_lead + 1

            if trans.booking_user_type == "B2B" or trans.source == "B2B":
                vol_b2b_total_lead = vol_b2b_total_lead + float(trans.price_total)
                num_b2b_total_lead = num_b2b_total_lead + 1

            else:
                vol_b2c_total_lead = vol_b2c_total_lead + float(trans.price_total)
                num_b2c_total_lead = num_b2c_total_lead + 1

            if trans.source == "Google Adwords":
                vol_googleadwords_lead = vol_googleadwords_lead + float(trans.price_total)
                num_googleadwords_lead = num_googleadwords_lead + 1
            elif trans.source == "Repeat Customer":
                vol_repeatcustomer_lead = vol_repeatcustomer_lead + float(trans.price_total)
                num_repeatcustomer_lead = num_repeatcustomer_lead + 1
            elif trans.source == "Employee Referral":
                vol_employeereferral_lead = vol_employeereferral_lead + float(trans.price_total)
                num_employeereferral_lead = num_employeereferral_lead + 1
            elif trans.source == "External Referral":
                vol_externalreferral_lead = vol_externalreferral_lead + float(trans.price_total)
                num_externalreferral_lead = num_externalreferral_lead + 1
            elif trans.source == "JustDial":
                vol_justdial_lead = vol_justdial_lead + float(trans.price_total)
                num_justdial_lead = num_justdial_lead + 1
            elif trans.source == "Pamphlet":
                vol_pamphlet_lead = vol_pamphlet_lead + float(trans.price_total)
                num_pamphlet_lead = num_pamphlet_lead + 1
            elif trans.source == "Auto Advertisement":
                vol_autoadvertisement_lead = vol_autoadvertisement_lead + float(trans.price_total)
                num_autoadvertisement_lead = num_autoadvertisement_lead + 1
            elif trans.source == "On-Ground Marketing":
                vol_on_groundmarketing_lead = vol_on_groundmarketing_lead + float(trans.price_total)
                num_on_groundmarketing_lead = num_on_groundmarketing_lead + 1
            elif trans.source == "Sulekha":
                vol_sulekha_lead = vol_sulekha_lead + float(trans.price_total)
                num_sulekha_lead = num_sulekha_lead + 1
            elif trans.source == "Database - Cold Calling":
                vol_database_coldcalling_lead = vol_database_coldcalling_lead + float(trans.price_total)
                num_database_coldcalling_lead = num_database_coldcalling_lead + 1
            elif trans.source == "Chat":
                vol_chat_lead = vol_chat_lead + float(trans.price_total)
                num_chat_lead = num_chat_lead + 1
            elif trans.source == "B2B":
                vol_b2b_lead = vol_b2b_lead + float(trans.price_total)
                num_b2b_lead = num_b2b_lead + 1
            elif trans.source == "Partner - Droom":
                vol_partner_droom_lead = vol_partner_droom_lead + float(trans.price_total)
                num_partner_droom_lead = num_partner_droom_lead + 1
            elif trans.source == "Partner - Wishup":
                vol_partner_wishup_lead = vol_partner_wishup_lead + float(trans.price_total)
                num_partner_wishup_lead = num_partner_wishup_lead + 1
            elif trans.source == "Partner - Housejoy":
                vol_partner_housejoy_lead = vol_partner_housejoy_lead + float(trans.price_total)
                num_partner_housejoy_lead = num_partner_housejoy_lead + 1
            elif trans.source == "Walk in ":
                vol_walkin_lead = vol_walkin_lead + float(trans.price_total)
                num_walkin_lead = num_walkin_lead + 1
            elif trans.source == "Partner - Mr Right":
                vol_partner_mrright_lead = vol_partner_mrright_lead + float(trans.price_total)
                num_partner_mrright_lead = num_partner_mrright_lead + 1
            elif trans.source == "Web Search":
                vol_websearch_lead = vol_websearch_lead + float(trans.price_total)
                num_websearch_lead = num_websearch_lead + 1
            elif trans.source == "Unknown":
                vol_unknown_lead = vol_unknown_lead + float(trans.price_total)
                num_unknown_lead = num_unknown_lead + 1
            elif trans.source == "Society camps":
                vol_societycamps_lead = vol_societycamps_lead + float(trans.price_total)
                num_societycamps_lead = num_societycamps_lead + 1
            elif trans.source == "Check up camps":
                vol_checkupcamps_lead = vol_checkupcamps_lead + float(trans.price_total)
                num_checkupcamps_lead = num_checkupcamps_lead + 1
            elif trans.source == "Sign up lead":
                vol_signuplead_lead = vol_signuplead_lead + float(trans.price_total)
                num_signuplead_lead = num_signuplead_lead + 1
            elif trans.source == "Facebook Ad":
                vol_facebookad_lead = vol_facebookad_lead + float(trans.price_total)
                num_facebookad_lead = num_facebookad_lead + 1
            elif trans.source == "Mahindra Authorized":
                vol_mahindraauthorized_lead = vol_mahindraauthorized_lead + float(trans.price_total)
                num_mahindraauthorized_lead = num_mahindraauthorized_lead + 1
            elif trans.source == "Exotel":
                vol_exotel_lead = vol_exotel_lead + float(trans.price_total)
                num_exotel_lead = num_exotel_lead + 1
            else:
                vol_other_lead = vol_other_lead + float(trans.price_total)
                num_other_lead = num_other_lead + 1



                if trans.feedback_2:
                    feed = Feedback.objects.filter(booking_data_id=trans.id)[0]
                    time_stamp = feed.time_stamp
                    pick_on_time = feed.pick_on_time
                    delivery_on_time = feed.delivery_on_time
                    courteous = feed.courteous
                    washing = feed.washing
                    quality_of_service = feed.quality_of_service
                    experience = feed.experience
                    additional = feed.additional
                    recommend_factor = feed.recommend_factor
                else:
                    time_stamp = "NA"
                    pick_on_time = "NA"
                    delivery_on_time = "NA"
                    courteous = "NA"
                    washing = "NA"
                    quality_of_service = "NA"
                    experience = "NA"
                    additional = "NA"
                    recommend_factor = "NA"

                if recommend_factor in ["1","2","3","4","5","6"]:
                    print "Detractors"
                    Detractors = Detractors + 1
                elif recommend_factor in ["7","8"]:
                    print "Passives"
                    Passives = Passives + 1
                elif recommend_factor in ["9","10"]:
                    print "Promoters"
                    Promoters = Promoters + 1

                try:
                    nps_completed = math.ceil((Promoters - Detractors)/(Promoters + Detractors + Passives) * 100)
                except:
                    nps_completed = "NA"


    obj['status'] = True
    obj['counter'] = 1
    obj['result'] = {

        'num_lead_lead':   num_lead_lead ,
        'vol_lead_lead':   vol_lead_lead ,
        'num_warm_lead':   num_warm_lead ,
        'vol_warm_lead':   vol_warm_lead ,
        'num_cold_lead':   num_cold_lead ,
        'vol_cold_lead':   vol_cold_lead ,
        'num_confirmed_booking':   num_confirmed_booking ,
        'vol_confirmed_booking':   vol_confirmed_booking ,
        'num_assigned_booking':   num_assigned_booking ,
        'vol_assigned_booking':   vol_assigned_booking ,
        'num_reachedworkshop_booking':   num_reachedworkshop_booking ,
        'vol_reachedworkshop_booking':   vol_reachedworkshop_booking ,
        'num_estimateshared_booking':   num_estimateshared_booking ,
        'vol_estimateshared_booking':   vol_estimateshared_booking ,
        'num_engineerleft_booking':   num_engineerleft_booking ,
        'vol_engineerleft_booking':   vol_engineerleft_booking ,
        'num_cancelled_lead':   num_cancelled_lead ,
        'vol_cancelled_lead':   vol_cancelled_lead ,
        'num_cancelled_booking':   num_cancelled_booking ,
        'vol_cancelled_booking':   vol_cancelled_booking ,
        'num_escalation_booking':   num_escalation_booking ,
        'num_jobcompleted_booking':   num_jobcompleted_booking ,
        'num_feedbacktaken_booking':   num_feedbacktaken_booking ,
        'num_completed': num_completed,
        'vol_googleadwords_completed': vol_googleadwords_completed,
        'num_googleadwords_completed': num_googleadwords_completed,
        'vol_repeatcustomer_completed': vol_repeatcustomer_completed,
        'num_repeatcustomer_completed': num_repeatcustomer_completed,
        'vol_employeereferral_completed': vol_employeereferral_completed,
        'num_employeereferral_completed': num_employeereferral_completed,
        'vol_externalreferral_completed': vol_externalreferral_completed,
        'num_externalreferral_completed': num_externalreferral_completed,
        'vol_justdial_completed': vol_justdial_completed,
        'num_justdial_completed': num_justdial_completed,
        'vol_pamphlet_completed': vol_pamphlet_completed,
        'num_pamphlet_completed': num_pamphlet_completed,
        'vol_autoadvertisement_completed': vol_autoadvertisement_completed,
        'num_autoadvertisement_completed': num_autoadvertisement_completed,
        'vol_ongroundmarketing_completed': vol_on_groundmarketing_completed,
        'num_ongroundmarketing_completed': num_on_groundmarketing_completed,
        'vol_sulekha_completed': vol_sulekha_completed,
        'num_sulekha_completed': num_sulekha_completed,
        'vol_databasecoldcalling_completed': vol_database_coldcalling_completed,
        'num_databasecoldcalling_completed': num_database_coldcalling_completed,
        'vol_chat_completed': vol_chat_completed,
        'num_chat_completed': num_chat_completed,
        'vol_b2b_completed': vol_b2b_completed,
        'num_b2b_completed': num_b2b_completed,
        'vol_partnerdroom_completed': vol_partner_droom_completed,
        'num_partnerdroom_completed': num_partner_droom_completed,
        'vol_partnerwishup_completed': vol_partner_wishup_completed,
        'num_partnerwishup_completed': num_partner_wishup_completed,
        'vol_partnerhousejoy_completed': vol_partner_housejoy_completed,
        'num_partnerhousejoy_completed': num_partner_housejoy_completed,
        'vol_walkin_completed': vol_walkin_completed,
        'num_walkin_completed': num_walkin_completed,
        'vol_partnermrright_completed': vol_partner_mrright_completed,
        'num_partnermrright_completed': num_partner_mrright_completed,
        'vol_websearch_completed': vol_websearch_completed,
        'num_websearch_completed': num_websearch_completed,
        'vol_unknown_completed': vol_unknown_completed,
        'num_unknown_completed': num_unknown_completed,
        'vol_societycamps_completed': vol_societycamps_completed,
        'num_societycamps_completed': num_societycamps_completed,
        'vol_checkupcamps_completed': vol_checkupcamps_completed,
        'num_checkupcamps_completed': num_checkupcamps_completed,
        'vol_signuplead_completed': vol_signuplead_completed,
        'num_signuplead_completed': num_signuplead_completed,
        'vol_facebookad_completed': vol_facebookad_completed,
        'num_facebookad_completed': num_facebookad_completed,
        'vol_mahindraauthorized_completed': vol_mahindraauthorized_completed,
        'num_mahindraauthorized_completed': num_mahindraauthorized_completed,
        'vol_exotel_completed': vol_exotel_completed,
        'num_exotel_completed': num_exotel_completed,
        'vol_other_completed': vol_other_completed,
        'num_other_completed': num_other_completed,
        'vol_completed': vol_completed,
        'vol_part_completed': vol_part_completed,
        'vol_labour_completed': vol_labour_completed,
        'vol_consumable_completed': vol_consumable_completed,
        'vol_lube_completed': vol_lube_completed,
        'nps':nps_completed,
        'num_users':num_users,
        'monthyear':monthyear,
        'vol_total_lead': vol_total_lead,
        'num_total_lead': num_total_lead,
        'vol_googleadwords_lead': vol_googleadwords_lead,
        'num_googleadwords_lead': num_googleadwords_lead,
        'vol_repeatcustomer_lead': vol_repeatcustomer_lead,
        'num_repeatcustomer_lead': num_repeatcustomer_lead,
        'vol_employeereferral_lead': vol_employeereferral_lead,
        'num_employeereferral_lead': num_employeereferral_lead,
        'vol_externalreferral_lead': vol_externalreferral_lead,
        'num_externalreferral_lead': num_externalreferral_lead,
        'vol_justdial_lead': vol_justdial_lead,
        'num_justdial_lead': num_justdial_lead,
        'vol_pamphlet_lead': vol_pamphlet_lead,
        'num_pamphlet_lead': num_pamphlet_lead,
        'vol_autoadvertisement_lead': vol_autoadvertisement_lead,
        'num_autoadvertisement_lead': num_autoadvertisement_lead,
        'vol_ongroundmarketing_lead': vol_on_groundmarketing_lead,
        'num_ongroundmarketing_lead': num_on_groundmarketing_lead,
        'vol_sulekha_lead': vol_sulekha_lead,
        'num_sulekha_lead': num_sulekha_lead,
        'vol_databasecoldcalling_lead': vol_database_coldcalling_lead,
        'num_databasecoldcalling_lead': num_database_coldcalling_lead,
        'vol_chat_lead': vol_chat_lead,
        'num_chat_lead': num_chat_lead,
        'vol_b2b_lead': vol_b2b_lead,
        'num_b2b_lead': num_b2b_lead,
        'vol_partnerdroom_lead': vol_partner_droom_lead,
        'num_partnerdroom_lead': num_partner_droom_lead,
        'vol_partnerwishup_lead': vol_partner_wishup_lead,
        'num_partnerwishup_lead': num_partner_wishup_lead,
        'vol_partnerhousejoy_lead': vol_partner_housejoy_lead,
        'num_partnerhousejoy_lead': num_partner_housejoy_lead,
        'vol_walkin_lead': vol_walkin_lead,
        'num_walkin_lead': num_walkin_lead,
        'vol_partnermrright_lead': vol_partner_mrright_lead,
        'num_partnermrright_lead': num_partner_mrright_lead,
        'vol_websearch_lead': vol_websearch_lead,
        'num_websearch_lead': num_websearch_lead,
        'vol_unknown_lead': vol_unknown_lead,
        'num_unknown_lead': num_unknown_lead,
        'vol_societycamps_lead': vol_societycamps_lead,
        'num_societycamps_lead': num_societycamps_lead,
        'vol_checkupcamps_lead': vol_checkupcamps_lead,
        'num_checkupcamps_lead': num_checkupcamps_lead,
        'vol_signuplead_lead': vol_signuplead_lead,
        'num_signuplead_lead': num_signuplead_lead,
        'vol_facebookad_lead': vol_facebookad_lead,
        'num_facebookad_lead': num_facebookad_lead,
        'vol_mahindraauthorized_lead': vol_mahindraauthorized_lead,
        'num_mahindraauthorized_lead': num_mahindraauthorized_lead,
        'vol_exotel_lead': vol_exotel_lead,
        'num_exotel_lead': num_exotel_lead,
        'vol_other_lead': vol_other_lead,
        'num_other_lead': num_other_lead,
        'vol_b2b_total_completed':vol_b2b_total_completed,
        'num_b2b_total_completed': num_b2b_total_completed,
        'vol_b2c_total_completed': vol_b2c_total_completed,
        'num_b2c_total_completed': num_b2c_total_completed,
        'vol_b2b_total_lead': vol_b2b_total_lead,
        'num_b2b_total_lead': num_b2b_total_lead,
        'vol_b2c_total_lead': vol_b2c_total_lead,
        'num_b2c_total_lead': num_b2c_total_lead,
        'vol_total_expense': vol_total_expense,
        'vol_googleadwords_expense': vol_googleadwords_expense,
        'vol_repeatcustomer_expense': vol_repeatcustomer_expense,
        'vol_employeereferral_expense': vol_employeereferral_expense,
        'vol_externalreferral_expense': vol_externalreferral_expense,
        'vol_justdial_expense': vol_justdial_expense,
        'vol_pamphlet_expense': vol_pamphlet_expense,
        'vol_autoadvertisement_expense': vol_autoadvertisement_expense,
        'vol_ongroundmarketing_expense': vol_on_groundmarketing_expense,
        'vol_sulekha_expense': vol_sulekha_expense,
        'vol_databasecoldcalling_expense': vol_database_coldcalling_expense,
        'vol_chat_expense': vol_chat_expense,
        'vol_b2b_expense': vol_b2b_expense,
        'vol_partnerdroom_expense': vol_partner_droom_expense,
        'vol_partnerwishup_expense': vol_partner_wishup_expense,
        'vol_partnerhousejoy_expense': vol_partner_housejoy_expense,
        'vol_walkin_expense': vol_walkin_expense,
        'vol_partnermrright_expense': vol_partner_mrright_expense,
        'vol_websearch_expense': vol_websearch_expense,
        'vol_unknown_expense': vol_unknown_expense,
        'vol_societycamps_expense': vol_societycamps_expense,
        'vol_checkupcamps_expense': vol_checkupcamps_expense,
        'vol_signuplead_expense': vol_signuplead_expense,
        'vol_facebookad_expense': vol_facebookad_expense,
        'vol_mahindraauthorized_expense': vol_mahindraauthorized_expense,
        'vol_exotel_expense': vol_exotel_expense,
        'vol_other_expense': vol_other_expense,
        'req_user_agent': is_agent,
        'req_user_staff': is_staff,
        'req_user_b2b': is_b2b,
        'req_user_admin': is_admin

    }
    obj['msg'] = "Success"

    return HttpResponse(json.dumps(obj), content_type='application/json')

def send_feedback(request):
    booking_data_id = get_param(request, 'booking_data_id', None)
    pick_on_time = get_param(request, 'pick_on_time', None)
    delivery_on_time = get_param(request, 'delivery_on_time', None)
    courteous = get_param(request, 'courteous', None)
    washing = get_param(request, 'washing', None)
    quality_of_service = get_param(request, 'quality_of_service', None)
    experience = get_param(request, 'experience', None)
    additional = get_param(request, 'additional', None)
    recommend_factor = get_param(request, 'recommend_factor', None)
    feedback_type   = get_param(request,'feedback_type',None)

    obj = {}
    obj['status'] = False
    obj['result'] = []

    # if pick_on_time == "1":
    #     pick_on_time = "Yes"
    # elif pick_on_time == "0":
    #     pick_on_time = "No"
    # else:
    #     pick_on_time = "Unanswered"
    #
    # if delivery_on_time == "1":
    #     delivery_on_time = "Yes"
    # elif delivery_on_time == "0":
    #     delivery_on_time = "No"
    # else:
    #     delivery_on_time = "Unanswered"
    #
    # if courteous == "1":
    #     courteous ="Yes"
    # elif courteous == "0":
    #     courteous = "No"
    # else:
    #     courteous = "Unanswered"

    findFeed = Feedback.objects.filter(booking_data_id = booking_data_id)
    booking = Bookings.objects.filter(id = booking_data_id)[0]
    if len(findFeed):
        findFeed = findFeed[0]
        findFeed.clickgarage_flag       = booking.clickgarage_flag
        if pick_on_time != None:
            findFeed.pick_on_time        = pick_on_time
        if delivery_on_time != None:
            findFeed.delivery_on_time   = delivery_on_time
        if courteous != None:
            findFeed.courteous          = courteous
        if washing != None:
            findFeed.washing            = washing
        if quality_of_service != None:
            findFeed.quality_of_service = quality_of_service
        if experience != None:
            findFeed.experience         = experience
        if additional != None:
            findFeed.additional         = additional
        if recommend_factor != None:
            findFeed.recommend_factor   = recommend_factor
        findFeed.time_stamp             = time.time()
        findFeed.save()
        # print findService.job_name

    else:
        Feed = Feedback(
            clickgarage_flag    = booking.clickgarage_flag,
            booking_data_id     = booking_data_id,
            time_stamp          = time.time(),
            pick_on_time        = pick_on_time,
            delivery_on_time    = delivery_on_time,
            courteous           = courteous,
            washing             = washing,
            quality_of_service  = quality_of_service,
            experience          = experience,
            additional          = additional,
            recommend_factor    = recommend_factor)
        Feed.save()

    if feedback_type == "1":
        booking.feedback_1 = True
    elif feedback_type == "2":
        booking.feedback_2 = True
    booking.save()
    obj['status'] = True
    return HttpResponse(json.dumps(obj), content_type='application/json')

def get_all_feedback(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking_data_id = get_param(request, 'booking_data_id', None)
    if booking_data_id == None :
        feedObjs = Feedback.objects.all()
    else:
        feedObjs = Feedback.objects.filter(booking_data_id=booking_data_id)
    for feed in feedObjs:
        obj['result'].append({
            'clickgarage_flag':feed.clickgarage_flag               ,
            'booking_data_id': feed.booking_data_id,
            'time_stamp': feed.time_stamp,
            'pick_on_time': feed.pick_on_time,
            'delivery_on_time': feed.delivery_on_time,
            'courteous': feed.courteous,
            'washing': feed.washing,
            'quality_of_service': feed.quality_of_service,
            'experience': feed.experience,
            'additional': feed.additional,
            'recommend_factor': feed.recommend_factor,
        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')



def view_all_bookings(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking_id = get_param(request, 'b_id', None)
    lead_booking = get_param(request, 'lead_booking', None)
    sort = get_param(request, 'sort', None)
    date = get_param(request,'date', None)
    date_end = get_param(request,'date_end',None)
    del_date = get_param(request, 'del_date', None)
    status = get_param(request,'status',None)
    name = get_param(request, 'name', None)
    reg_number = get_param(request,'reg',None)
    veh_type = get_param(request,'veh_type',None)
    data_id = get_param(request,'data_id',None)
    state = get_param(request,'state',None)
    source_id = get_param(request, 'source_id', None)
    phone_num = get_param(request, 'phone_num', None)
    agent_id = get_param(request, 'agent_id', None)
    cg_book = get_param(request, 'cg_book', None)
    complete_flag = get_param(request, 'complete_flag', None)
    page_num = get_param(request, 'page_num', None)
    getcsv = get_param(request, 'getcsv', "False")
    getcsv2 = get_param(request, 'getcsv2', "False")

    if request.user.is_admin or request.user.is_staff:
        if lead_booking == "Lead":
            lead_correct()


    if data_id == "" or data_id == None:
        if request.user.is_admin:
            if (booking_id == None or booking_id ==""):
                # print "no id"
                if sort != None and sort != "":
                    if sort == "Booking ID":
                        # print "booking sort"
                        tranObjs = Bookings.objects.all().order_by('-booking_id')
                    elif sort == "Name":
                        # print "name sort"
                        tranObjs = Bookings.objects.all().order_by('cust_name')
                    elif sort == "Status":
                        # print "status sort"
                        tranObjs = Bookings.objects.all().order_by('status')
                    elif sort == "Generation Date":
                        # print "status sort"
                        tranObjs = Bookings.objects.all().order_by('booking_timestamp')
                    elif sort == "Follow Time":
                        # print "status sort"
                        tranObjs = Bookings.objects.all().order_by('follow_up_time')
                    elif sort == "Source":
                        # print "status sort"
                        tranObjs = Bookings.objects.all().order_by('source')
                    elif sort == "Date":
                        # print "status sort"
                        if lead_booking == "Lead":
                            tranObjs = Bookings.objects.all().order_by('follow_up_date')
                        else:
                            tranObjs = Bookings.objects.all().order_by('date_booking')
                    else:
                        # print "other sort"
                        tranObjs = Bookings.objects.all().order_by('-booking_id')
                else:
                    # print "no sort"
                    tranObjs = Bookings.objects.all().order_by('-booking_id')
            else:
                # print "booking id filter"
                tranObjs = Bookings.objects.filter(booking_id=booking_id)

        elif request.user.is_staff:
            if (booking_id == None or booking_id ==""):
                # print "no id"
                if sort != None and sort != "":
                    if sort == "Booking ID":
                        # print "booking sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('-booking_id')
                    elif sort == "Name":
                        # print "name sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('cust_name')
                    elif sort == "Status":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('status')
                    elif sort == "Generation Date":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('booking_timestamp')
                    elif sort == "Follow Time":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('follow_up_time')
                    elif sort == "Source":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('source')
                    elif sort == "Date":
                        # print "status sort"
                        if lead_booking == "Lead":
                            tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('follow_up_date')
                        else:
                            tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('date_booking')
                    else:
                        # print "other sort"
                        tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('-booking_id')
                else:
                    # print "no sort"
                    tranObjs = Bookings.objects.filter(clickgarage_flag=True).order_by('-booking_id')
            else:
                # print "booking id filter"
                tranObjs = Bookings.objects.filter(booking_id=booking_id, clickgarage_flag=True)
        elif request.user.is_b2b:
            if booking_id == None or booking_id == "":
                # print "no id"
                if sort != None and sort != "":
                    if sort == "Booking ID":
                        # print "booking sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('-booking_id')
                    elif sort == "Name":
                        # print "name sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('cust_name')
                    elif sort == "Status":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('status')
                    elif sort == "Generation Date":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('booking_timestamp')
                    elif sort == "Follow Time":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('follow_up_time')
                    elif sort == "Source":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('source')
                    elif sort == "Date":
                        # print "status sort"
                        if lead_booking == "Lead":
                            tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('follow_up_date')
                        else:
                            tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('date_booking')
                    else:
                        # print "other sort"
                        tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('-booking_id')
                else:
                    # print "no sort"
                    tranObjs = Bookings.objects.filter(cust_id=request.user.id).order_by('-booking_id')
            else:
                # print "booking id filter"
                tranObjs = Bookings.objects.filter(booking_id=booking_id, cust_id=request.user.id)

        elif request.user.is_agent:
            if booking_id == None or booking_id == "":
                # print "no id"
                if sort != None and sort != "":
                    if sort == "Booking ID":
                        # print "booking sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('-booking_id')
                    elif sort == "Name":
                        # print "name sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('cust_name')
                    elif sort == "Status":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('status')
                    elif sort == "Generation Date":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('booking_timestamp')
                    elif sort == "Follow Time":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('follow_up_time')
                    elif sort == "Source":
                        # print "status sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('source')
                    elif sort == "Date":
                        # print "status sort"
                        if lead_booking == "Lead":
                            tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('follow_up_date')
                        else:
                            tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('date_booking')
                    else:
                        # print "other sort"
                        tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('-booking_id')
                else:
                    # print "no sort"
                    tranObjs = Bookings.objects.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id)).order_by('-booking_id')
            else:
                # print "booking id filter"
                tranObjs = Bookings.objects.filter(booking_id=booking_id)
                tranObjs = tranObjs.filter(Q(booking_owner=request.user.id) | Q(agent=request.user.id))
        else:
            tranObjs=None

        if lead_booking =="Lead":
            # print "Lead"
            tranObjs = tranObjs.filter(booking_flag = False)
        elif lead_booking =="Booking":
            # print "Booking"
            tranObjs = tranObjs.filter(booking_flag = True)
        else:
            # print "Other All"
            tranObjs = tranObjs

        if status != None and status !="":
            # print "filter status"
            tranObjs = tranObjs.filter(status=status)

        if name != None and name != "":
            # print "filter name"
            tranObjs = tranObjs.filter(cust_name=name)

        if source_id != None and source_id != "":
            tranObjs = tranObjs.filter(source=source_id)

        if phone_num != None and phone_num != "":
            tranObjs = tranObjs.filter(cust_number=phone_num)

        if reg_number != None and reg_number != "":
            # print "filter reg number"
            tranObjs = tranObjs.filter(cust_regnumber=reg_number)

        if agent_id != None and agent_id != "":
            # print "filter reg number"
            tranObjs = tranObjs.filter(agent=agent_id)

        if cg_book != None and cg_book != "":
            if cg_book == "True":
                tranObjs = tranObjs.filter(clickgarage_flag=True)

        if complete_flag != None and complete_flag != "":
            if complete_flag == "True":
                tranObjs = tranObjs.filter(job_completion_flag=True)

        if data_id != None and data_id != "":
            tranObjs = tranObjs.filter(id=data_id)


        if date != None and date != "":
            # print "date filter"
            year = date[6:10]
            month = date[3:5]
            day = date[0:2]
            # print year
            # print month

            start_date = datetime.date(int(year), int(month), int(day))

            if date_end != "" and date_end != None:
                end_date = datetime.date(int(date_end[6:10]), int(date_end[3:5]), int(date_end[0:2]))
            else:
                end_date = start_date

            # print day
            if lead_booking == "Lead":
                # tranObjs = tranObjs.filter(follow_up_date=datetime.date(int(year), int(month), int(day)))
                tranObjs = tranObjs.filter(follow_up_date__range=(start_date, end_date))
            else:
                # tranObjs = tranObjs.filter(date_booking=datetime.date(int(year), int(month), int(day)))
                tranObjs = tranObjs.filter(date_booking__range=(start_date, end_date))

        if del_date != None and del_date != "":
            # print "date filter"
            year_del = del_date[6:10]
            month_del = del_date[3:5]
            day_del = del_date[0:2]
            print year_del
            print month_del
            print day_del
            start_date_del = datetime.date(int(year_del), int(month_del), int(day_del))

            if date_end != "" and date_end != None:
                end_date_del = datetime.date(int(date_end[6:10]), int(date_end[3:5]), int(date_end[0:2]))
            else:
                end_date_del = start_date_del

            # tranObjs = tranObjs.filter(date_delivery=datetime.date(int(year_del), int(month_del), int(day_del)))
            tranObjs = tranObjs.filter(date_delivery__range=(start_date_del, end_date_del))

        if veh_type != None and veh_type != "" :
            # print "veh type"
            tranObjs = tranObjs.filter(cust_vehicle_type=veh_type)

        status_next = ""

        is_agent = request.user.is_agent
        is_staff = request.user.is_staff
        is_admin = request.user.is_admin
        is_b2b = request.user.is_b2b
    else:
        tranObjs = Bookings.objects.filter(id=data_id)
        if request.user.is_authenticated():
            is_agent = request.user.is_agent
            is_staff = request.user.is_staff
            is_admin = request.user.is_admin
            is_b2b = request.user.is_b2b
        else:
            is_agent = False
            is_staff = False
            is_admin = False
            is_b2b = False

    if getcsv == "True" or getcsv2 == "True":
        tranObjs = tranObjs
    else:
        if page_num != None and page_num != "":
            # offset = page_num * 30
            page_num = int(page_num) + 1
            # tranObjs = tranObjs.skip(offset).limit(30)
            tranObjs = Paginator(tranObjs, 15)
            try:
                tranObjs = tranObjs.page(page_num)
            except:
                None
    datarow = []
    datarow.append(['booking_flag',
                    'booking_id',
                    'booking_timestamp',
                    'cust_id',
                    'cust_name',
                    'cust_make',
                    'cust_model',
                    'cust_vehicle_type',
                    'cust_fuel_varient',
                    'cust_regnumber',
                    'cust_number',
                    'cust_email',
                    'cust_address',
                    'cust_locality',
                    'cust_city',
                    'settlement_cat',
                    'price',
                    'unit_price',
                    'type',
                    'quantity',
                    'name',
                    'price_total',
                    'price_labour',
                    'price_part',
                    'price_discount',
                    'date_booking',
                    'time_booking',
                    'date_delivery',
                    'is_paid',
                    'amount_paid',
                    'coupon',
                    'status',
                    'comments',
                    'source',
                    'agent',
                    'customer_notes',
                    'booking_user_type',
                    'booking_user_name',
                    'booking_user_number',
                    'clickgarage_flag',
                    'booking_owner',
                    'odometer',
                    'escalation_flag',
                    'bill_id',
                    'bill_generation_flag',
                    'feedback_1',
                    'feedback_2',
                    'follow_up_date',
                    'follow_up_time'])
    datarow2 = []
    datarow2.append(['agent_name',
                     'booking_id',
                    'cust_name',
                    'cust_make',
                    'cust_model',
                    'cust_vehicle_type',
                    'cust_fuel_varient',
                    'cust_regnumber',
                    'date_booking',
                    'payment_cg',
                     'payment_cg-uc',
                     'payment_cg-hj',
                     'credit_amount',
                     'price_total',
                    'price_labour',
                    'price_part',
                    'price_lube',
                    'price_vas',
                    'price_denting',
                    'price_discount',
                    'price_consumable',
                    'price_labour_pre_tax',
                    'price_part_pre_tax',
                    'price_lube_pre_tax',
                    'price_vas_pre_tax',
                    'price_denting_pre_tax',
                    'price_discount_pre_tax',
                    'price_consumable_pre_tax',
                    'commission_labour',
                    'commission_part',
                    'commission_lube',
                    'commission_vas',
                    'commission_denting',
                    'commission_discount',
                    'commission_consumable',
                    'commission_total',
                    'settlement_flag'
                     ])
    for trans in tranObjs:
        oldformat_b = str(trans.date_booking)
        datetimeobject = datetime.datetime.strptime(oldformat_b, '%Y-%m-%d')
        newformat_b = datetimeobject.strftime('%d-%m-%Y')

        if trans.date_delivery is None:
            oldformat_d = str(trans.date_booking)
        else:
            oldformat_d = str(trans.date_delivery)

        datetimeobject = datetime.datetime.strptime(oldformat_d, '%Y-%m-%d')
        newformat_d = datetimeobject.strftime('%d-%m-%Y')

        if trans.follow_up_date:
            oldformat_f = str(trans.follow_up_date)
            datetimeobject = datetime.datetime.strptime(oldformat_f, '%Y-%m-%d')
            newformat_f = datetimeobject.strftime('%d-%m-%Y')
        else:
            newformat_f = "NA"
        if trans.status == "":
            status_next = "Confirmed"
        if trans.status == "Follow Up":
            status_next = "Confirmed"
        if trans.status == "Cold":
            status_next = "Estimate Required"
        if trans.status == "Estimate Required":
            status_next = "Warm"
        if trans.status == "Warm":
            status_next = "Confirmed"

        # if trans.status == "Follow Up":
        #     status_next = "Confirmed"
        if trans.status == "Lead" 			    :
            status_next = "Confirmed"
        if trans.status =="Confirmed"			:
            status_next = "Assigned"
        if trans.status =="Assigned"			:
            status_next = "Engineer Left"
        if trans.status =="Engineer Left"			:
            status_next = "Reached Workshop"
        if trans.status =="Reached Workshop" 	:
            status_next = "Estimate Shared"
        if trans.status =="Estimate Shared" 	:
            status_next = "Job Completed"
        if trans.status =="Job Completed"		:
            status_next = "Feedback Taken"
        if trans.status =="Feedback Taken" 	:
            status_next = "Cancelled"
        if trans.status =="Cancelled" 			:
            status_next = "Escalation"
        if trans.status== "Escalation" 		:
            status_next = "Job Completed"

        if trans.agent != "":
            agent = fetch_user(trans.agent)
            agent_name = agent['result'][0]['first_name']
            full_agent_name = agent['result'][0]['first_name'] +' ' + agent['result'][0]['last_name']
            agent_num = agent['result'][0]['phone']
            agent_details = agent_name +" - "+agent_num
            agent_address = agent['result'][0]['user_address']
            agent_locality = agent['result'][0]['user_locality']
            agent_city = agent['result'][0]['user_city']
            agent_vat = agent['result'][0]['agent_vat']
            agent_cin = agent['result'][0]['agent_cin']
            agent_stax = agent['result'][0]['agent_stax']
            agent_state = agent['result'][0]['user_state']
            if state == None or state == "" or trans.booking_owner != "ClickGarage":
                if agent_state:
                    taxes = get_tax(agent_state)
                    vat_part = taxes['result'][0]['vat_parts']
                    vat_consumable = taxes['result'][0]['vat_consumables']
                    vat_lube = taxes['result'][0]['vat_lube']
                    if agent_stax:
                        service_tax = taxes['result'][0]['service_tax']
                    else:
                        service_tax = 0
                else:
                    vat_part = 0
                    vat_consumable = 0
                    vat_lube = 0
                    service_tax = 0
            elif state == "NA":
                vat_part = 0
                vat_consumable = 0
                vat_lube = 0
                service_tax = 0
            else:
                taxes = get_tax(state)
                vat_part = taxes['result'][0]['vat_parts']
                vat_consumable = taxes['result'][0]['vat_consumables']
                vat_lube = taxes['result'][0]['vat_lube']
                service_tax = taxes['result'][0]['service_tax']
        else:
            agent_name = "NA"
            full_agent_name = "NA"
            agent_num = "NA"
            agent_address = "NA"
            agent_locality = "NA"
            agent_city = "NA"
            agent_vat = "NA"
            agent_cin = "NA"
            agent_stax = "NA"
            agent_details = "Not Assigned"
            agent_state = "NA"
            if state == None or state == "":
                vat_part = 0
                vat_consumable = 0
                vat_lube = 0
                service_tax = 0
            elif state == "NA":
                vat_part = 0
                vat_consumable = 0
                vat_lube = 0
                service_tax = 0
            else:
                taxes = get_tax(state)
                vat_part = taxes['result'][0]['vat_parts']
                vat_consumable = taxes['result'][0]['vat_consumables']
                vat_lube = taxes['result'][0]['vat_lube']
                service_tax = taxes['result'][0]['service_tax']



        if trans.bill_id != "":
            bill = Bills.objects.filter(id = trans.bill_id)[0]
            components = bill.components
            payment_mode = bill.payment_mode
            date_created = str(bill.date_created)
            invoice_number = bill.invoice_number
            bill_notes = bill.notes
            bill_state = bill.state
            bill_vat_part_percent = bill.vat_part_percent
            bill_vat_lube_percent = bill.vat_lube_percent
            bill_vat_consumable_percent = bill.vat_consumable_percent
            bill_service_tax_percent = bill.service_tax_percent
            bill_agent_name = bill.agent_name
            bill_agent_address = bill.agent_address
            bill_file_name = bill.file_name
            # bill_agent_locality =  bill.agent_locality
            # bill_agent_city = bill.agent_city
            bill_agent_vat_no = bill.agent_vat_no
            bill_agent_cin = bill.agent_cin
            bill_agent_stax = bill.agent_stax
            bill_cust_name = bill.cust_name
            bill_cust_address = bill.cust_address
            bill_cust_locality = bill.cust_locality
            bill_cust_city = bill.cust_city
            bill_reg_number  =  bill.reg_number
            bill_vehicle = bill.vehicle
            # bill_model = bill.model
            bill_type  = bill.bill_type
            bill_owner = bill.owner
        else:
            components = ""
            payment_mode = ""
            date_created = ""
            invoice_number = ""
            bill_notes = ""
            bill_state = ""
            bill_vat_part_percent = ""
            bill_vat_lube_percent = ""
            bill_vat_consumable_percent = ""
            bill_service_tax_percent = ""
            bill_agent_name = ""
            bill_agent_address = ""
            # bill_agent_locality = ""
            # bill_agent_city = ""
            bill_agent_vat_no = ""
            bill_agent_cin = ""
            bill_agent_stax = ""
            bill_cust_name = ""
            bill_cust_address = ""
            bill_cust_locality = ""
            bill_cust_city = ""
            bill_reg_number = ""
            bill_vehicle = ""
            # bill_model = ""
            bill_type = ""
            bill_owner = ""
            bill_file_name = ""

        if trans.feedback_2:
            print "1"
            feed                = Feedback.objects.filter(booking_data_id = trans.id)[0]
            time_stamp          = feed.time_stamp
            pick_on_time        = feed.pick_on_time
            delivery_on_time    = feed.delivery_on_time
            courteous           = feed.courteous
            washing             = feed.washing
            quality_of_service  = feed.quality_of_service
            experience          = feed.experience
            additional          = feed.additional
            recommend_factor    = feed.recommend_factor
        else:
            # print "2"
            time_stamp = "NA"
            pick_on_time = "NA"
            delivery_on_time = "NA"
            courteous = "NA"
            washing = "NA"
            quality_of_service = "NA"
            experience = "NA"
            additional = "NA"
            recommend_factor = "NA"

        if getcsv2 == "True":
            commission = trans.commission
            if socket.gethostname().startswith('ip-'):
                if PRODUCTION:
                    filename = '/home/ubuntu/beta/suigen/csvfiles/allbookings_commission.csv'
                else:
                    filename = '/home/ubuntu/testing/suigen/csvfiles/allbookings_commission.csv'
            else:
                filename = '/home/shashwat/Desktop/codebase/ClickGarage/csvfiles/allbookings_commission.csv'

            file = open(filename, 'w')
            part_price = 0
            part_price_pretax = 0
            part_comm = 0
            labour_price= 0
            labour_price_pretax = 0
            labour_comm = 0
            vas_price = 0
            vas_price_pretax = 0
            vas_comm = 0
            consumable_price = 0
            consumable_price_pretax = 0
            consumable_comm = 0
            denting_price = 0
            denting_price_pretax = 0
            denting_comm = 0
            lube_price = 0
            lube_price_pretax = 0
            lube_comm = 0
            discount_price = 0
            discount_price_pretax = 0
            discount_comm = 0

            for comm in commission:
                # print trans.booking_id
                if comm['type']=="Part":
                    part_price = comm['purchase_price']
                    part_price_pretax = comm['purchase_price_pre_tax']
                    part_comm = comm['clickgarage_share']

                if comm['type'] == "Labour":
                    labour_price = comm['purchase_price']
                    labour_price_pretax = comm['purchase_price_pre_tax']
                    labour_comm = comm['clickgarage_share']

                if comm['type'] == "VAS":
                    vas_price = comm['purchase_price']
                    vas_price_pretax = comm['purchase_price_pre_tax']
                    vas_comm = comm['clickgarage_share']

                if comm['type'] == "Consumable":
                    consumable_price = comm['purchase_price']
                    consumable_price_pretax = comm['purchase_price_pre_tax']
                    consumable_comm = comm['clickgarage_share']

                if comm['type'] == "Denting":
                    denting_price = comm['purchase_price']
                    denting_price_pretax = comm['purchase_price_pre_tax']
                    denting_comm = comm['clickgarage_share']

                if comm['type'] == "Lube":
                    lube_price = comm['purchase_price']
                    lube_price_pretax = comm['purchase_price_pre_tax']
                    lube_comm = comm['clickgarage_share']

                if comm['type'] == "Discount":
                    discount_price = comm['purchase_price']
                    discount_price_pretax = comm['purchase_price_pre_tax']
                    discount_comm = comm['clickgarage_share']
            payment_cg = 0
            payment_uc = 0
            payment_hj = 0
            payment_credit = 0
            for paymentdic in trans.payment_booking:
                if len(paymentdic):
                    if paymentdic['collected_by'] == "ClickGarage":
                        payment_cg = payment_cg + float(paymentdic['amount'])
                    if paymentdic['collected_by'] == "ClickGarage UC":
                        payment_uc = payment_uc + float(paymentdic['amount'])
                    if paymentdic['collected_by'] == "ClickGarage HJ":
                        payment_hj = payment_hj + float(paymentdic['amount'])
                    if paymentdic['collected_by'] == "ClickGarage Credit":
                        payment_credit = payment_credit + float(paymentdic['amount'])

            datarow2.append([str(full_agent_name),
                             str(trans.booking_id),
                             str(trans.cust_name),
                             str(trans.cust_make),
                             str(trans.cust_model),
                             str(trans.cust_vehicle_type),
                             str(trans.cust_fuel_varient),
                             str(trans.cust_regnumber),
                             str(trans.date_booking),
                             str(payment_cg),
                             str(payment_uc),
                             str(payment_hj),
                             str(payment_credit),
                             str(trans.price_total),
                             str(labour_price),
                             str(part_price),
                             str(lube_price),
                             str(vas_price),
                             str(denting_price),
                             str(discount_price),
                             str(consumable_price),
                             str(labour_price_pretax),
                             str(part_price_pretax),
                             str(lube_price_pretax),
                             str(vas_price_pretax),
                             str(denting_price_pretax),
                             str(discount_price_pretax),
                             str(consumable_price_pretax),
                             str(labour_comm),
                             str(part_comm),
                             str(lube_comm),
                             str(vas_comm),
                             str(denting_comm),
                             str(discount_comm),
                             str(consumable_comm),
                             str(trans.commission_total),
                             str(trans.settlement_flag),
                             ])

        if getcsv == "True":
            items = trans.service_items
            if socket.gethostname().startswith('ip-'):
                if PRODUCTION:
                    filename = '/home/ubuntu/beta/suigen/csvfiles/allbookings.csv'
                else:
                    filename = '/home/ubuntu/testing/suigen/csvfiles/allbookings.csv'
            else:
                filename = '/home/shashwat/Desktop/codebase/ClickGarage/csvfiles/allbookings.csv'

            file = open(filename, 'w')
            comment = ''
            for job in trans.jobssummary:
                comment = comment +'$' + job['Job'] + ' (' + str(job['Price']) + ')'

            comment = comment.encode('utf-8')
            for item in items:
                # print trans.booking_id
                try:
                    settlement_cat = item['settlement_cat']
                except:
                    settlement_cat = "NA"

                try:
                    type_part = item['type']
                except:
                    type_part = "NA"

                try:
                    item_unit_price = item['unit_price']
                except:
                    item_unit_price = "NA"

                try:
                    item_quantity = item['quantity']
                except:
                    item_quantity = "NA"

                try:
                    name = item['name']
                except:
                    try:
                        name = item['job_name']
                    except:
                        name = "NA"

                # print name

                datarow.append([str(trans.booking_flag),
                                str(trans.booking_id),
                                str(trans.booking_timestamp),
                                str(trans.cust_id),
                                str(trans.cust_name),
                                str(trans.cust_make),
                                str(trans.cust_model),
                                str(trans.cust_vehicle_type),
                                str(trans.cust_fuel_varient),
                                str(trans.cust_regnumber),
                                str(trans.cust_number),
                                str(trans.cust_email),
                                str(trans.cust_address),
                                str(trans.cust_locality),
                                str(trans.cust_city),
                                str(settlement_cat),
                                str(item['price']),
                                str(item_unit_price),
                                str(type_part),
                                str(item_quantity),
                                str(name),
                                str(trans.price_total),
                                str(trans.price_labour),
                                str(trans.price_part),
                                str(trans.price_discount),
                                str(trans.date_booking),
                                str(trans.time_booking),
                                str(trans.date_delivery),
                                str(trans.is_paid),
                                str(trans.amount_paid),
                                str(trans.coupon),
                                str(trans.status),
                                str(comment),
                                str(trans.source),
                                str(full_agent_name),
                                str(trans.customer_notes),
                                str(trans.booking_user_type),
                                str(trans.booking_user_name),
                                str(trans.booking_user_number),
                                str(trans.clickgarage_flag),
                                str(trans.booking_owner),
                                str(trans.odometer),
                                str(trans.escalation_flag),
                                str(trans.bill_id),
                                str(trans.bill_generation_flag),
                                str(trans.feedback_1),
                                str(trans.feedback_2),
                                str(trans.follow_up_date),
                                str(trans.follow_up_time)])



        obj['result'].append({
            'id'                : trans.id              ,
            'booking_flag'      : trans.booking_flag    ,
            'booking_id'        : trans.booking_id      ,
            'booking_timestamp' : trans.booking_timestamp,
            'time_generated'    : time.strftime('%I:%M %p',time.localtime(float(trans.booking_timestamp)+19800)),
            'date_generated'    : time.strftime('%d-%m-%Y',time.localtime(float(trans.booking_timestamp)+19800)),
            'cust_id'           : trans.cust_id,
            'cust_name'         : trans.cust_name,
            'cust_make'         : trans.cust_make,
            'cust_model'        : trans.cust_model,
            'cust_vehicle_type' : trans.cust_vehicle_type,
            'cust_fuel_varient' : trans.cust_fuel_varient,
            'cust_regnumber'    : trans.cust_regnumber,
            'cust_number'       : trans.cust_number,
            'cust_email'        : trans.cust_email,
            'cust_address'      : trans.cust_address,
            'cust_locality'     : trans.cust_locality,
            'cust_city'         : trans.cust_city,
            'service_items'     : trans.service_items,
            'part_total'        : trans.price_part,
            'labour_total'      : trans.price_labour,
            'discount_total'    : trans.price_discount,
            'price_total'       : trans.price_total,
            'date_booking'      : newformat_b,
            # 'follow_up_date': newformat_f,
            'time_booking'      : trans.time_booking,
            'is_paid'           : trans.is_paid,
            'amount_paid'       : trans.amount_paid,
            'coupon'            : trans.coupon,
            'status'            : trans.status,
            'escalation_flag'   : trans.escalation_flag,
            'comments'          : trans.comments,
            'source'            : trans.source,
            'agent'             : trans.agent,
            'agent_name'        :full_agent_name,
            'agent_address'     : agent_address,
            'agent_locality'    : agent_locality,
            'agent_city'        :agent_city,
            'agent_state'       : agent_state,
            'vat_part'          : vat_part,
            'vat_consumable'    : vat_consumable,
            'vat_lube'          : vat_lube,
            'service_tax'           : service_tax,
            'agent_vat'             : agent_vat,
            'agent_cin'             :agent_cin,
            'agent_stax'            : agent_stax,
            # 'estimate_history'      : trans.estimate_history,
            'estimate_history_len': len(trans.estimate_history),
            'agent_details'         : agent_details,
            'status_next'           :status_next,
            'customer_notes'        :trans.customer_notes,
            'booking_user_type'     : trans.booking_user_type,
            'delivery_date'         :newformat_d,
            'job_summary': trans.jobssummary ,
            'req_user_agent'        : is_agent,
            'req_user_staff'        : is_staff,
            'req_user_b2b'          : is_b2b,
            'req_user_admin'        : is_admin,
            'booking_user_name'     : trans.booking_user_name,
            'booking_user_number'   : trans.booking_user_number,
            'bill_id'               : trans.bill_id,
            'bill_generation_flag'  : trans.bill_generation_flag,
            'payment_status'        : trans.payment_status,
            'odometer'              : trans.odometer,
            'clickgarage_flag'      : trans.clickgarage_flag,
            'booking_owner'         : trans.booking_owner,
            'bill_components'       : components,
            'bill_payment_mode'     : payment_mode,
            'bill_date_created'     : date_created,
            'invoice_number'        : invoice_number,
            'bill_notes'            :bill_notes,
            'bill_state'            : bill_state,
            'bill_vat_part_percent' : bill_vat_part_percent,
            'bill_vat_lube_percent' : bill_vat_lube_percent,
            'bill_vat_consumable_percent' : bill_vat_consumable_percent,
            'bill_service_tax_percent' : bill_service_tax_percent,
            'bill_agent_name' : bill_agent_name,
            'bill_agent_address' : bill_agent_address,
            'bill_file_name':bill_file_name,
            # 'bill_agent_locality' : bill_agent_locality,
            # 'bill_agent_city' : bill_agent_city,
            'bill_agent_vat_no' : bill_agent_vat_no,
            'bill_agent_cin' : bill_agent_cin,
            'bill_agent_stax' : bill_agent_stax,
            'bill_cust_name' : bill_cust_name,
            'bill_cust_address' : bill_cust_address,
            'bill_cust_locality': bill_cust_locality,
            'bill_cust_city': bill_cust_city,
            'bill_reg_number': bill_reg_number,
            'bill_vehicle': bill_vehicle,
            'bill_owner':bill_owner,
            # 'bill_model': bill_model,
            'bill_type':bill_type,
            'time_stamp' : time_stamp,
            'pick_on_time': pick_on_time,
            'delivery_on_time': delivery_on_time,
            'courteous': courteous,
            'washing': washing,
            'quality_of_service': quality_of_service,
            'experience': experience,
            'additional': additional,
            'recommend_factor': recommend_factor,
            'follow_up_date': newformat_f,
            'follow_up_time': str(trans.follow_up_time.strftime('%I:%M %p')),
            'follow_up_status':trans.follow_up_status,
            'total_commission':trans.commission_total,
            'commission_items': trans.commission,
            'settlement_flag': trans.settlement_flag,
            'frozen_flag': trans.frozen_flag,
            'job_completion_flag': trans.job_completion_flag,
            'payment_booking': trans.payment_booking,
            'purchase_price_total': trans.purchase_price_total,
            'lead_delay_count': trans.delay_count

        })
    if getcsv == "True":
        # obj['datacheck'] = datarow
        with file:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="allbookings.csv"'
            writer = csv.writer(response)
            writer.writerows(datarow)
            file.close()
            return response

    if getcsv2 == "True":
        # obj['datacheck'] = datarow
        with file:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="allbookings_commission.csv"'
            writer = csv.writer(response)
            writer.writerows(datarow2)
            file.close()
            return response

            # writer = csv.writer(file)
            # f = open(filename, 'r')
            # downloadfilename = 'bookingsdata.csv'
            # content = f.read()
            # response_file = HttpResponse(content, mimetype='text/csv')
            # response_file['Content-Disposition'] = 'attachement; filename=' + downloadfilename
            # return response_file

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_user(user_id):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    tranObjs = CGUserNew.objects.filter(id=user_id)
    for trans in tranObjs:
        obj['result'].append({
            'id'   :trans.id
            ,'email':trans.email_list
            ,'email_primary':trans.email
            ,'phone':trans.contact_no
            ,'uname':trans.username
            ,'first_name':trans.first_name
            ,'last_name':trans.last_name
            ,'agent': trans.is_agent
            , 'user': trans.is_user
            , 'admin': trans.is_admin
            , 'staff': trans.is_staff
            , 'b2b': trans.is_b2b
            , 'user_address_list': trans.user_saved_address
            , 'user_vehicles': trans.user_veh_list
            , 'user_state':trans.user_state
            , 'agent_cin': trans.agent_cin
            , 'agent_vat': trans.agent_vat
            , 'agent_stax': trans.agent_stax
            ,  'user_address':trans.user_address
            , 'user_locality': trans.user_locality
            , 'user_city': trans.user_city

        })
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return obj


def fetch_all_users(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    type = get_param(request, 'type', None)
    userid = get_param(request,'u_id',None)

    # WMS Modification Start
    tranObjs = None

    if request.user.is_staff or request.user.is_admin:
        tranObjs = CGUserNew.objects.all()

    if request.user.is_agent:
        tranObjs = CGUserNew.objects.filter(owner_user=request.user.id)

    # WMS Modification End
    if userid != None:
        tranObjs = tranObjs.filter(id=userid)

    if type != None:
        if type == "agent":
            tranObjs = tranObjs.filter(is_agent=True)
        elif type == "b2b":
            tranObjs = tranObjs.filter(is_b2b=True)
        elif type == "user":
            tranObjs = tranObjs.filter(is_user=True)
        elif type == "admin":
            tranObjs = tranObjs.filter(is_admin=True)
        elif type == "staff":
            tranObjs = tranObjs.filter(is_admin=True)
            # else:
            #     tranObjs = CGUserNew.objects.all()
    if request.user.is_authenticated():
        is_agent = request.user.is_agent
        is_staff = request.user.is_staff
        is_admin = request.user.is_admin
        is_b2b = request.user.is_b2b
    else:
        is_agent = False
        is_staff = False
        is_admin = False
        is_b2b = False

    for trans in tranObjs:
        obj['result'].append({
            'id'   :trans.id
            ,'email_list':trans.email_list
            ,'email_primary': trans.email
            ,'phone':trans.contact_no
            ,'uname':trans.username
            ,'first_name':trans.first_name
            ,'last_name':trans.last_name
            ,'agent': trans.is_agent
            , 'user': trans.is_user
            , 'admin': trans.is_admin
            ,'staff': trans.is_staff
            ,'b2b': trans.is_b2b
            , 'user_address_list': trans.user_saved_address
            , 'user_vehicles': trans.user_veh_list
            , 'user_state': trans.user_state
            , 'agent_cin': trans.agent_cin
            , 'agent_stax': trans.agent_stax
            , 'agent_vat': trans.agent_vat
            ,'clickgarage_flag' : trans.clickgarage_flag
            # ,'email_list' : trans.email_list
            , 'owner_user': trans.owner_user
            , 'date_joined': str(trans.date_joined)
            , 'user_address': trans.user_address
            , 'user_locality':trans.user_locality
            , 'user_city':trans.user_city
            ,'req_user_agent': is_agent
            ,'req_user_staff': is_staff
            ,'req_user_b2b': is_b2b
            ,'req_user_admin': is_admin
            , 'agent_sms_credits': trans.agent_sms_credits

            , 'agent_part_share': trans.agent_part_share
            , 'agent_lube_share': trans.agent_lube_share
            , 'agent_consumable_share': trans.agent_consumable_share
            , 'agent_labour_share': trans.agent_labour_share
            , 'agent_vas_share': trans.agent_vas_share
            , 'agent_denting_share': trans.agent_denting_share
            # , 'user_state':trans.user_state
        })
    obj['status'] = True
    obj['counter'] = 1
    # if request.user.is_anonymous:
    #     obj['auth_rights'] = {'admin': False, 'b2b': False,
    #                                     'agent': False,
    #                                     'staff': False}
    # else:
    #     obj['auth_rights'] = {'admin': request.user.is_admin, 'b2b': request.user.is_b2b,
    #                                     'agent': request.user.is_agent,
    #                                     'staff': request.user.is_staff}
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def update_user(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    user_id = get_param(request, 'user_id', None)
    user_name = get_param(request, 'user_name',None)
    # user_lname = get_param(request, 'user_lname',None)
    user_num = get_param(request, 'user_num',None)
    user_email = get_param(request, 'user_email',None)
    user_add = get_param(request, 'user_add',None)
    user_loc = get_param(request, 'user_loc',None)
    user_city = get_param(request, 'user_city',None)
    user_state = get_param(request, 'user_state', None)
    agent = get_param(request, 'agent_st', None)
    b2b = get_param(request, 'b2b_st', None)
    admin = get_param(request, 'admin_st', None)
    staff = get_param(request, 'staff_st', None)
    agent_vat = get_param(request, 'agent_vat', None)
    agent_stax = get_param(request, 'agent_stax', None)
    agent_cin = get_param(request, 'agent_cin', None)
    sms_credits = get_param(request, 'sms_credits', None)

    agent_part_share = get_param(request, 'agent_part_share', None)
    agent_lube_share = get_param(request, 'agent_lube_share', None)
    agent_consumable_share = get_param(request, 'agent_consumable_share', None)
    agent_labour_share = get_param(request, 'agent_labour_share', None)
    agent_vas_share = get_param(request, 'agent_vas_share', None)
    agent_denting_share = get_param(request, 'agent_denting_share', None)

    user_name = cleanstring(user_name).title()
    user_add = cleanstring(user_add).title()
    user_loc = cleanstring(user_loc).title()
    user_city = cleanstring(user_city).title()
    user_state = cleanstring(user_state).title()


    # WMS Modification Start
    if request.user.is_staff or request.user.is_admin or request.user.is_agent:
        if user_id == "" or user_id == None:
            if request.user.is_agent:
                user2 = create_check_user_modified(name=user_name,number=user_num,owner=request.user.id)
            else:
                user2 = create_check_user(name=user_name,number=user_num)
                # WMS Modification End

        else:
            user2 = CGUserNew.objects.filter(id=user_id)[0]
        address2 = {'address': user_add, 'locality': user_loc, 'city': user_city, 'state' : user_state}

        # if agent_vat:
        user2.agent_vat = agent_vat
        # if agent_stax:
        user2.agent_stax = agent_stax
        # if agent_cin:
        user2.agent_cin = agent_cin
        if sms_credits:
            user2.agent_sms_credits = sms_credits

        if agent_part_share:
            user2.agent_part_share = agent_part_share

        if agent_lube_share:
            user2.agent_lube_share = agent_lube_share

        if agent_consumable_share:
            user2.agent_consumable_share = agent_consumable_share

        if agent_labour_share:
            user2.agent_labour_share = agent_labour_share

        if agent_vas_share:
            user2.agent_vas_share = agent_vas_share

        if agent_denting_share:
            user2.agent_denting_share = agent_denting_share

        if user_state:
            user2.user_state = user_state

        if user_add:
            user2.user_address =  user_add
        if user_loc:
            user2.user_locality = user_loc
        if user_city:
            user2.user_city = user_city

        if address2 not in user2.user_saved_address:
            user2.user_saved_address.append(address2)

        if user_email not in user2.email_list:
            user2.email_list.append(user_email)
        user2.email = user_email

        if user_name:
            user_name = user_name.split(' ')
            user2.first_name = user_name[0]
            if len(user_name) > 1:
                lname = ""
                for i in range(1, len(user_name)):
                    if i == 1:
                        lname = user_name[i]
                    else:
                        lname = lname + " " + user_name[i]
                user2.last_name = lname

        if agent == "true":
            user2.is_agent = True
        else:
            user2.is_agent = False
        if b2b == "true":
            user2.is_b2b = True
        else:
            user2.is_b2b = False
        if admin == "true":
            user2.is_admin = True
        else:
            user2.is_admin = False
        if staff == "true":
            user2.is_staff = True
        else:
            user2.is_staff = False
        user2.save()
    obj['status'] = True
    obj['result'] = "Success"
    obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def update_booking(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking_id = get_param(request, 'b_id', None)
    # agent_id = get_param(request,'agent_id',None)
    email_n = get_param(request,'email',None)
    reg_number_n = get_param(request,'reg_number',None)
    comment_n = get_param(request,'comment',None)
    # estimate = get_param(request,'estimate',None)
    time_n = get_param(request,'time',None)
    date_n = get_param(request, 'date', None)
    notes_n = get_param(request,'note',None)
    amount_paid = get_param(request, 'amount_paid', None)
    name = get_param(request, 'name', None)
    number = get_param(request, 'number', None)
    address = get_param(request, 'address', None)
    locality = get_param(request, 'locality', None)
    city = get_param(request, 'city', None)
    source = get_param(request, 'source', None)
    date_delivery = get_param(request, 'date_del', None)
    date_follow = get_param(request, 'date_follow', None)
    time_follow = get_param(request, 'time_follow', None)
    follow_status = get_param(request, 'follow_status', None)
    odometer = get_param(request, 'odometer', None)
    job_summary = get_param(request, 'job_summary', None)

    booking = Bookings.objects.filter(booking_id=booking_id)[0]

    name = cleanstring(name).title()
    address = cleanstring(address).title()
    locality = cleanstring(locality).title()
    city = cleanstring(city).title()
    reg_number_n = cleanstring(reg_number_n).upper()

    curr_date = time.strftime("%d-%m-%Y")
    curr_time = datetime.datetime.time(datetime.datetime.now() + datetime.timedelta(hours = 5, minutes = 30))
    curr_time = str(curr_time.strftime('%I:%M %p'))


    # if agent_id != None and agent_id != "":
    #     booking.agent = agent_id
    if follow_status != None and follow_status != "":
        new_follow_status = {'Date': curr_date,
                             'Time': curr_time,
                             'Status': follow_status
                             }
        booking.follow_up_status.append(new_follow_status)

    if amount_paid != None:
        booking.amount_paid = amount_paid

    if source != None:
        booking.source = source

    if name != None:
        if  (booking.booking_user_name ==  booking.cust_name):
            booking.booking_user_name = name
            booking.cust_name = name
        else:
            booking.booking_user_name = name

    if number != None:
        if (booking.booking_user_name == booking.cust_name):
            booking.booking_user_number = number
            booking.cust_number = number
        else:
            booking.booking_user_number = number

    if address != None:
        booking.cust_address = address

    if locality != None:
        booking.cust_locality = locality

    if city != None:
        booking.cust_city = city


    if reg_number_n != None:
        booking.cust_regnumber = reg_number_n

    if comment_n != None:
        booking.comments = comment_n

    if job_summary != None:
        booking.jobssummary = json.loads(job_summary)

    if time_n != None or time_n != "":
        booking.time_booking = time_n

    if date_n != None or date_n != "":
        oldformat = date_n
        datetimeobject = datetime.datetime.strptime(oldformat, '%d-%m-%Y')
        newformat = datetimeobject.strftime('%Y-%m-%d')
        date_n = newformat
        booking.date_booking = date_n

    if date_delivery != None and date_delivery != "":
        oldformat_2 = date_delivery
        datetimeobject2 = datetime.datetime.strptime(oldformat_2, '%d-%m-%Y')
        newformat_2 = datetimeobject2.strftime('%Y-%m-%d')
        date_delivery = newformat_2
        booking.date_delivery = date_delivery

    if notes_n != None:
        booking.customer_notes = notes_n

    if email_n != None:
        booking.cust_email = email_n

    if date_follow != None and date_follow != "":
        oldformat_3 = date_follow
        datetimeobject3 = datetime.datetime.strptime(oldformat_3, '%d-%m-%Y')
        newformat_3 = datetimeobject3.strftime('%Y-%m-%d')
        date_follow = newformat_3
        booking.follow_up_date = date_follow

    if time_follow != None and time_follow != "":
        oldformat_time = time_follow
        time_format = datetime.datetime.strptime(oldformat_time, '%I:%M %p')
        # time_obj = time_format.strftime('%I:%M %p')

        print time_follow
        # print time_obj

        booking.follow_up_time = time_format

    if odometer != None and odometer != "":
        booking.odometer = odometer


    booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def add_delete_payment(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    data_id = get_param(request, 'data_id', None)
    payment_id = get_param(request,'payment_id',None)
    add_delete = get_param(request,'add_del',None)
    medium = get_param(request,'medium',None)
    amount= get_param(request, 'amount', None)
    col_by = get_param(request, 'col_by', None)
    booking = Bookings.objects.filter(id = data_id)[0]
    date_today = datetime.date.today()
    oldformat_b = str(date_today)
    datetimeobject = datetime.datetime.strptime(oldformat_b, '%Y-%m-%d')
    date_today_new= datetimeobject.strftime('%d-%m-%Y')
    total_paid = float(booking.amount_paid)
    if add_delete == "Add":
        if amount != "" and amount != None:
            obj = {
                "payment_id" : str(time.time()),
                "collected_by":col_by,
                "amount":amount,
                "medium":medium,
                "date_collected": date_today_new
            }
            total_paid = float(booking.amount_paid) + float(amount)
            booking.payment_booking.append(obj)
            booking.amount_paid = str(total_paid)
    if add_delete == "Delete":
        payment2 = []
        items = booking.payment_booking
        # print payment_id
        for item in items:
            print item['payment_id']
            if item['payment_id'] == payment_id:
                print "1"
                total_paid = float(booking.amount_paid) - float(item['amount'])
            else:
                # print "2"
                payment2.append(item)
        booking.amount_paid = str(total_paid)
        booking.payment_booking = payment2

    booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')




def update_estimate(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking_id = get_param(request, 'b_id', None)
    estimate = get_param(request,'estimate',None)

    booking = Bookings.objects.filter(booking_id=booking_id)[0]
    vat_part = 0
    vat_consumable = 0
    vat_lube = 0
    service_tax = 0
    agent_vas_share = 0
    agent_part_share = 0
    agent_lube_share = 0
    agent_consumable_share = 0
    agent_denting_share = 0
    agent_labour_share = 0

    if booking.agent != "Not Assigned" and booking.agent != "":
        agent = CGUserNew.objects.filter(id = booking.agent)[0]
        state = agent.user_state
        if booking.clickgarage_flag:
            agent_vas_share = agent.agent_vas_share
            agent_part_share = agent.agent_part_share
            agent_lube_share = agent.agent_lube_share
            agent_consumable_share = agent.agent_consumable_share
            agent_denting_share = agent.agent_denting_share
            agent_labour_share = agent.agent_labour_share
        else:
            agent_vas_share = 0
            agent_part_share = 0
            agent_lube_share = 0
            agent_consumable_share = 0
            agent_denting_share = 0
            agent_labour_share = 0

        taxes = get_tax(state)

        if agent.agent_vat !="" and agent.agent_vat != None:
            if taxes['result'][0]['vat_parts'] == "":
                vat_part = 0
            else:
                vat_part = float(taxes['result'][0]['vat_consumables'])

            if taxes['result'][0]['vat_parts'] == "":
                vat_consumable = 0
            else:
                vat_consumable = float(taxes['result'][0]['vat_consumables'])

            if taxes['result'][0]['vat_lube'] == "":
                vat_lube = 0
            else:
                vat_lube = float(taxes['result'][0]['vat_lube'])
        else:
            vat_part = 0
            vat_consumable = 0
            vat_lube = 0

        if agent.agent_stax != "" and agent.agent_stax != None:
            if taxes['result'][0]['service_tax'] == "":
                service_tax = 0
            else:
                service_tax = float(taxes['result'][0]['service_tax'])
        else:
            service_tax = 0

    if estimate != None:
        old_estimate = booking.service_items
        estimate = json.loads(estimate)
        if estimate != old_estimate:
            new_estimate_timestamp = time.time()
            estimate_by_id = request.user.id
            estimate_by_number = request.user.contact_no
            estimate_by_name = request.user.first_name + " " + request.user.last_name
            total_price = 0
            total_part = 0
            total_labour = 0
            total_discount = 0
            total_puchase_price = 0
            clickgarage_part_share = 0
            total_part_comm = 0
            total_part_pre_tax = 0
            clickgarage_labour_share = 0
            total_labour_comm = 0
            total_labour_pre_tax = 0
            clickgarage_denting_share = 0
            total_denting_comm = 0
            total_denting_pre_tax = 0
            clickgarage_vas_share = 0
            total_vas_comm = 0
            total_vas_pre_tax = 0
            clickgarage_lube_share = 0
            total_lube_comm = 0
            total_lube_pre_tax = 0
            clickgarage_consumable_share = 0
            total_consumable_comm = 0
            total_consumable_pre_tax = 0
            clickgarage_discount_share = 0
            total_discount_comm = 0
            total_discount_pre_tax = 0
            total_commission = 0
            obj_part = {}
            obj_lube = {}
            obj_consumable = {}
            obj_vas = {}
            obj_denting = {}
            obj_labour = {}
            obj_discount = {}

            commission = []
            estimate2 = []
            for item in estimate:
                obj2 = {}
                applicable_tax = 0
                # print item
                if item['type'] == "Part":
                    total_price = total_price + float(item['price'])
                    total_part = total_part + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])
                    applicable_tax = vat_part
                elif item['type'] == "Consumable":
                    total_price = total_price + float(item['price'])
                    total_part = total_part + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])
                    applicable_tax = vat_consumable
                elif item['type'] == "Lube":
                    total_price = total_price + float(item['price'])
                    total_part = total_part + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])
                    applicable_tax = vat_lube

                elif item['type']=="Labour":
                    total_price = total_price + float(item['price'])
                    total_labour = total_labour + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])
                    applicable_tax = service_tax

                elif item['type'] == "Discount":
                    total_price = total_price - float(item['price'])
                    total_discount = total_discount + float(item['price'])
                    total_puchase_price = total_puchase_price - float(item['purchase_price'])
                    applicable_tax = 0

                if item['settlement_cat'] == "Part":
                    applicable_commission_share = float(agent_part_share)
                    clickgarage_part_share = clickgarage_part_share + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                    total_part_comm = total_part_comm + float(item['purchase_price'])
                    total_part_pre_tax = total_part_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                elif item['settlement_cat'] == "Labour":
                    applicable_commission_share = float(agent_labour_share)
                    clickgarage_labour_share = clickgarage_labour_share + (float(item['purchase_price']) / (1 + applicable_tax / 100) * (applicable_commission_share) / 100)
                    total_labour_comm = total_labour_comm + float(item['purchase_price'])
                    total_labour_pre_tax = total_labour_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                elif item['settlement_cat'] == "VAS":
                    applicable_commission_share = float(agent_vas_share)
                    clickgarage_vas_share = clickgarage_vas_share + (float(item['purchase_price']) / (1 + applicable_tax / 100) * (applicable_commission_share) / 100)
                    total_vas_comm = total_vas_comm + float(item['purchase_price'])
                    total_vas_pre_tax = total_vas_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                elif item['settlement_cat'] == "Denting":
                    applicable_commission_share = float(agent_denting_share)
                    clickgarage_denting_share = clickgarage_denting_share + (float(item['purchase_price']) / (1 + applicable_tax / 100) * (applicable_commission_share) / 100)
                    total_denting_comm = total_denting_comm + float(item['purchase_price'])
                    total_denting_pre_tax = total_denting_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                elif item['settlement_cat'] == "Lube":
                    applicable_commission_share = float(agent_lube_share)
                    clickgarage_lube_share = clickgarage_lube_share + (float(item['purchase_price']) / (1 + applicable_tax / 100) * (applicable_commission_share) / 100)
                    total_lube_comm = total_lube_comm + float(item['purchase_price'])
                    total_lube_pre_tax = total_lube_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                elif item['settlement_cat'] == "Consumable":
                    applicable_commission_share = float(agent_consumable_share)
                    clickgarage_consumable_share = clickgarage_consumable_share + (float(item['purchase_price']) / (1 + applicable_tax / 100) * (applicable_commission_share) / 100)
                    total_consumable_comm = total_consumable_comm + float(item['purchase_price'])
                    total_consumable_pre_tax = total_consumable_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)
                elif item['settlement_cat'] == "Discount":
                    applicable_commission_share = 0
                    clickgarage_discount_share = clickgarage_discount_share + (float(item['purchase_price']) / (1 + applicable_tax / 100) * (applicable_commission_share) / 100)
                    total_discount_comm = total_discount_comm + float(item['purchase_price'])
                    total_discount_pre_tax = total_discount_pre_tax + float(item['purchase_price']) / (1 + applicable_tax / 100)
                    total_commission = total_commission + (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100)

                obj2 = {
                    'comment': item['comment'],
                    'name': item['name'],
                    'settlement_cat': item['settlement_cat'],
                    'price': item['price'],
                    'unit_price': item['unit_price'],
                    'pre_tax_price': float(item['price']) / (1 + applicable_tax / 100),
                    'type': item['type'],
                    'approved': item['approved'],
                    'quantity': item['quantity'],
                    'purchase_price': item['purchase_price'],
                    'purchase_price_pretax': float(item['purchase_price']) / (1 + applicable_tax / 100),
                    'clickgarage_share': (float(item['purchase_price']) / (1 + applicable_tax / 100)*(applicable_commission_share)/100),
                }
                estimate2.append(obj2)

            booking.service_items = estimate2
            if booking.frozen_flag or booking.settlement_flag:
                None
            else:
                obj_part = {"type":"Part",
                            "purchase_price":total_part_comm,
                            "purchase_price_pre_tax":total_part_pre_tax,
                            "clickgarage_share":round(clickgarage_part_share),
                            "share_percent" : agent_part_share}
                commission.append(obj_part)

                obj_labour = {"type": "Labour",
                            "purchase_price": total_labour_comm,
                            "purchase_price_pre_tax": total_labour_pre_tax,
                            "clickgarage_share": round(clickgarage_labour_share),
                              "share_percent": agent_labour_share}
                commission.append(obj_labour)

                obj_vas = {"type": "VAS",
                            "purchase_price": total_vas_comm,
                            "purchase_price_pre_tax": total_vas_pre_tax,
                            "clickgarage_share": round(clickgarage_vas_share),
                           "share_percent": agent_vas_share}
                commission.append(obj_vas)

                obj_denting = {"type": "Denting",
                            "purchase_price": total_denting_comm,
                            "purchase_price_pre_tax": total_denting_pre_tax,
                            "clickgarage_share": round(clickgarage_denting_share),
                               "share_percent": agent_denting_share}
                commission.append(obj_denting)

                obj_consumable = {"type": "Consumable",
                            "purchase_price": total_consumable_comm,
                            "purchase_price_pre_tax": total_consumable_pre_tax,
                            "clickgarage_share": round(clickgarage_consumable_share),
                                  "share_percent": agent_consumable_share}
                commission.append(obj_consumable)

                obj_lube = {"type": "Lube",
                            "purchase_price": total_lube_comm,
                            "purchase_price_pre_tax": total_lube_pre_tax,
                            "clickgarage_share": round(clickgarage_lube_share),
                            "share_percent": agent_lube_share}
                commission.append(obj_lube)

                obj_discount = {"type": "Discount",
                            "purchase_price": total_discount_comm,
                            "purchase_price_pre_tax": total_discount_pre_tax,
                            "clickgarage_share": round(clickgarage_discount_share),
                            "share_percent": 0}
                commission.append(obj_discount)

                booking.commission = commission
                booking.commission_total = str(round(total_commission,0))
            booking.purchase_price_total = str(total_puchase_price)
            booking.price_total = str(total_price)
            booking.price_labour = str(total_labour)
            booking.price_part = str(total_part)
            booking.price_discount = str(total_discount)
            a = booking.estimate_history.append({"timestamp": new_estimate_timestamp, "change_by_userid" : estimate_by_id, "change_by_number": estimate_by_number, "change_by_name":  estimate_by_name, 'estimate':old_estimate})
            print a

    booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def update_agent(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking_id = get_param(request, 'b_id', None)
    agent_id = get_param(request,'agent_id',None)
    send_sms = get_param(request, 'send_sms', "1")
    booking = Bookings.objects.filter(booking_id=booking_id)[0]
    send_sms_bool = True
    if send_sms == "1":
        send_sms_bool = True
    else:
        send_sms_bool = False

    if agent_id != None and agent_id != "":
        booking.agent = agent_id

    estimate = booking.service_items

    agent = fetch_user(agent_id)
    agent_name = agent['result'][0]['first_name']
    agent_num = agent['result'][0]['phone']
    cust_name = booking.cust_name
    cust_num = booking.cust_number
    oldformat_b = str(booking.date_booking)
    datetimeobject = datetime.datetime.strptime(oldformat_b, '%Y-%m-%d')
    date = datetimeobject.strftime('%d-%m-%Y')

    time = booking.time_booking
    comments = booking.comments
    total = booking.price_total
    address = booking.cust_address+" "+booking.cust_locality+" "+booking.cust_city
    vehicle = booking.cust_make+ " "+booking.cust_model+" "+booking.cust_fuel_varient
    # service_breakup = ""
    # for item in estimate:
    #     service_breakup = service_breakup + item['name'] +"-"+item['price']+" "
    booking.save()
    change_status_actual(booking_id=booking_id,status_id="Assigned",send_sms= send_sms_bool)
    # mviews.send_sms_agent(agent_name, agent_num, cust_num, date, time, booking_id, cust_name, comments,
    #                          total, address,vehicle)
    # booking.status = "Assigned"
    # booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def update_delete_expense(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    expense_id = get_param(request, 'expense_id', None)
    expense_date = get_param(request, 'expense_date', None)
    expense_cat = get_param(request, 'expense_cat',None)
    expense_subcat = get_param(request, 'expense_subcat',None)
    expense_reason = get_param(request, 'expense_reason',None)
    expense_comment = get_param(request, 'expense_comment',None)
    expense_amount = get_param(request, 'expense_amount',None)
    expense_owner = get_param(request, 'expense_owner', None)
    delete = get_param(request,'delete',None)
    try:
        oldformat_e = expense_date
        datetimeobject = datetime.datetime.strptime(oldformat_e, '%d-%m-%Y')
        newformat_e= datetimeobject.strftime('%Y-%m-%d')
    except:
        None
    # added_by_id = str(request.user.id)
    # WMS Modification Start
    if request.user.is_admin:
        if expense_id == "" or expense_id == None:
            expense = Expenses(timestamp_expense=time.time(),
                               date_expense=newformat_e,
                               category=expense_cat,
                               sub_category=expense_subcat,
                               reason=expense_reason,
                               comment=expense_comment,
                               amount=str(expense_amount),
                               expense_owner=expense_owner,
                               added_by=request.user.id)
            expense.save()
        else:
            findExpense = Expenses.objects.filter(id=expense_id)
            if len(findExpense):
                findExpense = findExpense[0]
                if delete == "True":
                    findExpense.delete()
                else:
                    findExpense.date_expense = newformat_e
                    findExpense.category = expense_cat
                    findExpense.sub_category = expense_subcat
                    findExpense.reason = expense_reason
                    findExpense.comment = expense_comment
                    findExpense.amount = expense_amount
                    findExpense.expense_owner = expense_owner
                    findExpense.save()
    obj['status'] = True
    obj['result'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def view_all_expense(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    expense_id = get_param(request, 'expense_id', None)
    if request.user.is_admin:
        if expense_id == None or expense_id == "":
            expenses = Expenses.objects.all()
        else:
            expenses = Expenses.objects.filter(id=expense_id)

        for expense in expenses:
            oldformat_e = str(expense.date_expense)
            datetimeobject = datetime.datetime.strptime(oldformat_e,'%Y-%m-%d')
            newformat_e = datetimeobject.strftime('%d-%m-%Y')

            obj['result'].append({
                'id':expense.id,
                'timestamp_expense': expense.timestamp_expense,
                'date_expense': newformat_e,
                'category': expense.category,
                'sub_category': expense.sub_category,
                'reason': expense.reason,
                'comment': expense.comment,
                'amount': expense.amount,
                'expense_owner': expense.expense_owner,
                'added_by': expense.added_by
            })
    obj['status'] = True
    obj['counter'] = 1
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')






def add_modify_coupon(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    coupon_code     = get_param(request, 'c_id', None)
    datetime_created    = time.time()
    date_start      = get_param(request, 'd_start', None)
    expiry_date     = get_param(request, 'd_end', None)
    type            = get_param(request, 'type', None)
    active          = get_param(request, 'active', None)
    message         = get_param(request, 'message', None)
    category        = get_param(request, 'cat_id', None)
    value           = get_param(request, 'val', None)
    car_bike        = get_param(request, 'veh_type', None)
    cap             = get_param(request, 'cap', None)

    oldformat_s = date_start
    datetimeobject = datetime.datetime.strptime(oldformat_s, '%d-%m-%Y')
    newformat_s = datetimeobject.strftime('%Y-%m-%d')
    date_start = newformat_s

    oldformat_e = expiry_date
    datetimeobject = datetime.datetime.strptime(oldformat_e, '%d-%m-%Y')
    newformat_e = datetimeobject.strftime('%Y-%m-%d')
    expiry_date = newformat_e
    if request.user.is_staff or request.user.is_admin:

        if active == "true":
            active_n = True
        else:
            active_n = False

        findCoupon = CouponNew.objects.filter(coupon_code = coupon_code)
        if len(findCoupon):
            findCoupon = findCoupon[0]
            findCoupon.date_start = date_start
            findCoupon.expiry_date = expiry_date
            findCoupon.type = type
            findCoupon.active = active_n
            findCoupon.message = message
            findCoupon.category = category
            findCoupon.value = value
            findCoupon.car_bike = car_bike
            findCoupon.cap = cap
            findCoupon.save()
        else:
            coupon = CouponNew(
                datetime_created= datetime_created,
                coupon_code=coupon_code,
                date_start=date_start,
                expiry_date=expiry_date,
                type=type,
                active=True,
                message=message,
                category=category,
                value=value,
                car_bike=car_bike,
                cap=cap)
            coupon.save()
    obj['status'] = True
    obj['result'] = "Success"
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def view_all_coupons(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    coupon_id = get_param(request, 'c_id', None)
    if request.user.is_staff or request.user.is_admin:
        if coupon_id == None:
            coupons = CouponNew.objects.all()
        else:
            coupons = CouponNew.objects.filter(id=coupon_id)

        for coupon in coupons:
            oldformat_s = str(coupon.date_start)
            datetimeobject = datetime.datetime.strptime(oldformat_s,'%Y-%m-%d')
            newformat_s = datetimeobject.strftime('%d-%m-%Y')

            oldformat_e = str(coupon.expiry_date)
            datetimeobject = datetime.datetime.strptime(oldformat_e, '%Y-%m-%d')
            newformat_e = datetimeobject.strftime('%d-%m-%Y')

            obj['result'].append({
                'id'   :coupon.id
                ,'datetime_created': coupon.datetime_created
                ,'date_start': newformat_s
                ,'expiry_date': newformat_e
                ,'type': coupon.type
                ,'active': coupon.active
                ,'message': coupon.message
                ,'coupon_code': coupon.coupon_code
                ,'category': coupon.category
                ,'value': coupon.value
                ,'car_bike': coupon.car_bike
                ,'cap': coupon.cap
            })
    obj['status'] = True
    obj['counter'] = 1
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')


def check_coupon(request):
    check = False
    msg = ''
    obj = {}
    obj['status'] = False
    obj['result'] = []
    coupon_id = get_param(request, 'c_id', None)
    vehtype_id = get_param(request, 'veh_type', None)
    coupons = CouponNew.objects.filter(coupon_code=coupon_id,car_bike=vehtype_id)
    date_today = datetime.date.today()
    if coupons:
        coupon = coupons[0]
        if (coupon.expiry_date >= date_today):
            active = True
        else:
            active = False

        if coupon.active and active:
            obj['result'].append({
                'id': coupon.id
                , 'type': coupon.type
                , 'active': coupon.active
                , 'message': coupon.message
                , 'coupon_code': coupon.coupon_code
                , 'category': coupon.category
                , 'value': coupon.value
                , 'car_bike': coupon.car_bike
                , 'cap': coupon.cap})
            msg = coupon.message
        else:
            msg = "Coupon Expired!"

    else:
        msg = "Invalid Coupon!"

    obj['status'] = True
    obj['msg'] = msg
    # obj['auth_rights'] = {'admin': request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent,
    #                       'staff': request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def send_booking(request):
    name = get_param(request, 'name', None)
    number = get_param(request, 'number', None)
    email = get_param(request, 'email', None)
    reg_number = get_param(request, 'reg_number', None)
    address = get_param(request, 'address', None)
    locality = get_param(request, 'locality', None)
    city = get_param(request, 'city', None)
    order_list = get_param(request, 'order_list', None)
    if order_list:
        order_list = json.loads(order_list)
    else:
        order_list = []
    job_summary_int = get_param(request, 'int_summary', None)

    if job_summary_int:
        job_summary_int = json.loads(job_summary_int)
    else:
        job_summary_int= []
    make = get_param(request, 'make', None)
    veh_type = get_param(request, 'veh_type', None)
    model = get_param(request, 'model', None)
    fuel = get_param(request, 'fuel', None)
    date = get_param(request, 'date', None)
    time_str = get_param(request, 'time', None)
    # comment = get_param(request, 'comment', None)
    jobsummary_list = get_param(request,'jobsummary_list',None)
    is_paid = get_param(request, 'is_paid', None)
    paid_amt = get_param(request, 'paid_amt', None)
    coupon = get_param(request, 'coupon', None)
    price_total = get_param(request, 'price_total', None)
    onetp = get_param(request,'otp',None)
    source = get_param(request,'source',None)
    booking_flag_user = get_param(request,'flag',"True")
    send_confirm = get_param(request,'send_confirm',"1")
    booking_user_name = get_param(request,'booking_user_name',None)
    booking_user_number = get_param(request,'booking_user_number',None)
    follow_time = get_param(request,'follow_time',None)
    odometer = get_param(request, 'odometer', "")
    # follow_up_date = get_param(request,'follow',None)
    # print email
    # print order_list

    # if follow_up_date == None:
    #     follow_up_date = date
    jobsummary_list = json.loads(jobsummary_list)
    oldformat = date
    datetimeobject = datetime.datetime.strptime(oldformat, '%d-%m-%Y')
    newformat = datetimeobject.strftime('%Y-%m-%d')
    date =newformat
    obj2 = {}
    obj2['status'] = False
    obj2['result'] = []

    if follow_time != None and follow_time != "":
        oldformat_time = follow_time
        time_format = datetime.datetime.strptime(oldformat_time, '%I:%M %p')
    else:
        time_format = ""
    obj = checkOTP_new(onetp, number)

    if request.user.is_authenticated():
        if request.user.is_b2b:
            user = request.user
            booking_flag = True
            name = request.user.first_name +' ' +request.user.last_name
            number = request.user.contact_no
            email = request.user.email
            booking = place_booking(str(request.user.id), name, number, email, reg_number, address, locality, city, order_list,
                                    make, veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                                    price_total, "B2B", booking_flag,job_summary_int,send_sms="0", booking_type="B2B",booking_user_name=booking_user_name,booking_user_number=booking_user_number,odometer=odometer)

        # WMS Modification Start

        elif request.user.is_agent:
            if booking_flag_user == "True":
                booking_flag = True
            else:
                booking_flag = False
            user = create_check_user_modified(name, number,request.user.id)
            # if request.user.id not in user.owner_user:
            #     user.owner_user.append(request.user.id)
            booking = place_booking(str(user.id), name, number, email, reg_number, address, locality, city,
                                    order_list,make, veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                                    price_total, source, booking_flag,
                                    job_summary_int, send_sms=send_confirm,owner=request.user.id,follow_up_date_book=date,follow_up_time_book=time_format,odometer=odometer)
        # WMS Modification End

        elif request.user.is_staff or request.user.is_admin:
            if booking_flag_user == "True":
                booking_flag = True
            else:
                booking_flag = False
            user = create_check_user(name, number)
            if user.is_b2b:
                name = user.first_name + ' ' + user.last_name
                number = user.contact_no
                email = user.email
                booking_flag = True

                booking = place_booking(str(user.id), name, number, email, reg_number, address, locality, city,
                                        order_list,
                                        make,
                                        veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                                        price_total, "B2B", booking_flag,job_summary_int,send_sms="0", booking_type="B2B",booking_user_name=booking_user_name,booking_user_number=booking_user_number,follow_up_date_book=date,follow_up_time_book=time_format,odometer=odometer)

            else:
                booking = place_booking(str(user.id), name, number, email, reg_number, address, locality, city,
                                        order_list,
                                        make,
                                        veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                                        price_total, source, booking_flag,
                                        job_summary_int,send_sms=send_confirm,follow_up_date_book=date,follow_up_time_book=time_format,odometer=odometer)

        else:
            print email
            user = request.user
            booking_flag = True
            if request.user.contact_no == number:
                # print email
                booking = place_booking(str(request.user.id), name, number, email, reg_number, address, locality, city,
                                        order_list, make,veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                                        price_total, source, booking_flag,job_summary_int,send_confirm,odometer=odometer)
            elif obj['status']:
                # print email
                user = create_check_user(name, number)
                booking = place_booking(str(request.user.id), name, number, email, reg_number, address, locality, city,
                                        order_list,
                                        make,
                                        veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                                        price_total, source, booking_flag,job_summary_int,send_confirm,odometer=odometer)
        obj2['result'] = {}
        obj2['result']['userid'] = user.id
        obj2['result']['booking'] = booking
        obj2['result']['auth'] = True
        obj2['result']['msg'] = "Authenticated User"

    elif obj['status']:
        user = create_check_user(name,number)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        booking_flag = True
        booking = place_booking(str(user.id), name, number, email, reg_number, address, locality, city, order_list, make,
                                veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon, price_total,source,booking_flag,job_summary_int,send_confirm,odometer=odometer)
        obj2['result'] = {}
        obj2['result']['userid'] = user.id
        obj2['result']['booking'] = booking
        obj2['result']['auth'] = True
        obj2['result']['msg'] = obj['msg']
    else:
        obj2['result'] = {}
        obj2['result']['auth'] = False
        obj2['result']['msg'] = obj['msg']

    obj2['status'] = True
    obj2['counter'] = 1
    obj2['msg'] = "Success"
    return HttpResponse(json.dumps(obj2), content_type='application/json')

# 1. Lead - Lead
# 2. Booking - Confirmed
# 3. Assign Vendor - Assigned
# 4. Left - Agent Left
# 5. Reached - Reached Workshop
# 6. Estimate shared - Estimate Shared
# 7. Job completed - Job completed
# 8. Feedback - Feedback Taken
# 9. Cancelled - Cancelled
# 10. Escalation - Escalation

def lead_correct():
    obj = {}
    obj['status'] = False
    obj['result'] = []
    bookings = Bookings.objects.filter(booking_flag = False)
    for booking in bookings:
        if booking.booking_flag == False:
            # print "1"
            if (booking.status == "Lead" or booking.status == "Follow Up" or booking.status == "Cold" or booking.status == "Warm" or booking.status == "Estimate Required"):
                # print "2"
                # booking.delay_count = booking.delay_count + 1
                oldformat = str(booking.follow_up_date)
                newformat = datetime.datetime.strptime(oldformat, '%Y-%m-%d')
                time_today = datetime.datetime.today()
                time_today = time_today.replace(hour=0, minute=0, second=0, microsecond=0)
                if newformat < time_today:
                    print "1"
                    booking.follow_up_date = datetime.date.today()
                    booking.follow_up_time = datetime.time(9, 30, 0, 0)
                    booking.delay_count = booking.delay_count + 1
                    booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')


def change_status(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking_id = get_param(request, 'b_id', None)
    status_id = get_param(request,'status_id',None)
    send_sms = get_param(request,'send_sms',"1")
    if send_sms == "1":
        send_sms_bool = True
    else:
        send_sms_bool = False
    change_status_actual(booking_id=booking_id,status_id=status_id,send_sms= send_sms_bool)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    # obj['auth_rights'] = {'admin': request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent,
    #                       'staff': request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')


def change_status_actual(booking_id,status_id,send_sms):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    booking = Bookings.objects.filter(booking_id=booking_id)[0]
    booking_user = booking.booking_user_type
    send_sms_bool = True

    if send_sms:
        if booking.clickgarage_flag:
            send_sms_bool = True
        else:
            user1 = CGUserNew.objects.filter(id = booking.agent)
            sms_credits = user1.agent_sms_credits
            num_sms = 1
            if num_sms <= sms_credits:
                send_sms_bool = True
                num_sms_left = sms_credits - 1
                user1.agent_sms_credits = num_sms_left
                user1.save()
            else:
                send_sms_bool = False
    else:
        send_sms_bool = False


    if status_id != None:
        old_status = booking.status

        # WMS Modification Start
        if booking.booking_owner != "ClickGarage":
            if status_id == "Confirmed":
                status_id = "Assigned"
            else:
                None
        # WMS Modification End
        booking.status = status_id
        # oldbooking_flag

        if (status_id =="Lead" or status_id == "Follow Up" or status_id == "Cold" or status_id == "Warm" or status_id == "Estimate Required"):
            if(status_id == "Lead" and booking.booking_flag == True):
                date_lead_convert = datetime.date.today() + datetime.timedelta(days=1)
                time_lead_convert =  datetime.time(9, 30, 0, 0)
                booking.follow_up_date = str(date_lead_convert)
                booking.follow_up_time = time_lead_convert
                booking.booking_flag = False
                if booking.clickgarage_flag:
                    booking.agent = ""
            else:
                booking.booking_flag = False

        elif (status_id == "Cancelled" and booking.booking_flag == False):
            booking.booking_flag = False
        else:
            booking.booking_flag = True

        # booking.job_completion_flag = False

        if (status_id == "Confirmed" and (old_status == "Lead" or old_status == "Follow Up" or old_status == "Cold" or old_status == "Warm"or old_status == "Estimate Required")):
            if (booking_user=="User"):
                user = create_check_user(booking.cust_name,booking.cust_number)
                booking.cust_id = user.id
                address2 = {'address': booking.cust_address, 'locality': booking.cust_locality, 'city': booking.cust_city}
                if address2 not in user.user_saved_address:
                    user.user_saved_address.append(address2)
                vehicle = {'type': booking.cust_vehicle_type, 'make': booking.cust_make, 'model': booking.cust_model, 'fuel': booking.cust_fuel_varient, "reg_num": booking.cust_regnumber}
                if vehicle not in user.user_veh_list:
                    user.user_veh_list.append(vehicle)
                if booking.cust_email not in user.email_list:
                    user.email_list.append(booking.cust_email)
                user.email = booking.cust_email
                user.save()
                # print "SMS Sent"
                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name,booking.cust_number,booking.booking_id,booking.date_booking,booking.time_booking,status="Confirmed")
            print "SMS not Sent"
        if (status_id == "Assigned" and old_status == "Confirmed" ):
            agent = fetch_user(booking.agent)
            agent_name = agent['result'][0]['first_name']
            agent_num = agent['result'][0]['phone']
            agent_details = agent_name + " - " + agent_num
            vehicle = booking.cust_make +" "+booking.cust_model+" "+booking.cust_fuel_varient
            address = booking.cust_address +", "+booking.cust_locality+", "+booking.cust_city
            if (booking_user == "User"):
                # print "SMS Sent"



                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name,booking.cust_number,booking.booking_id,booking.date_booking,booking.time_booking,agent_details,status="Assigned")
            if booking.clickgarage_flag:
                mviews.send_sms_agent(agent_name, agent_num, booking.booking_user_number, booking.date_booking, booking.time_booking, booking.booking_id, booking.booking_user_name, booking.jobssummary ,
                                  booking.price_total, address, vehicle)

        if(status_id == "Engineer Left"  and old_status == "Assigned"):
            agent = fetch_user(booking.agent)
            agent_name = agent['result'][0]['first_name']
            agent_num = agent['result'][0]['phone']
            # agent_details = agent_name + " - " + agent_num
            if (booking_user == "User"):
                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name,booking.cust_number,booking.booking_id,booking.date_booking, booking.time_booking,status="Engineer Left")


        if (status_id == "Reached Workshop"):
            if (booking_user == "User"):
                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name,booking.cust_number,booking.booking_id,booking.date_booking, booking.time_booking,status="Reached Workshop")

        if (status_id == "Estimate Shared"):
            # send email to customer about estimate breakup
            if (booking_user == "User"):
                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name,booking.cust_number,booking.booking_id,booking.date_booking, booking.time_booking,estimate=booking.price_total,status="Estimate Shared")

        if (status_id == "Job Completed" and old_status == "Escalation"):

            booking.job_completion_flag = True
            # send email to customer about bill reciept and an apology note
            booking.date_delivery = datetime.date.today()

            if (booking_user == "User"):
                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name,booking.cust_number,booking.booking_id,booking.date_booking, booking.time_booking,estimate=booking.price_total,status="Job Completed", status2 ="Escalation")

        if (status_id == "Job Completed" and old_status != "Escalation"):
            # booking.job_completion_flag = True
            # send email to customer about bill reciept and a thank you note
            if (booking_user == "User"):
                if send_sms_bool:
                    print "SMS Sent"
                    mviews.send_sms_customer(booking.cust_name, booking.cust_number, booking.booking_id, booking.date_booking,
                                         booking.time_booking, estimate=booking.price_total,
                                         status="Job Completed")
                # if booking.cust_vehicle_type == "Car":
                    # if booking.price_total >= 3500:
                    #     date_today = datetime.date.today() + datetime.timedelta(days=180)
                    # elif booking.price_total >= 1500:
                date_today = datetime.date.today() + datetime.timedelta(days=90)
                #     else:
                #         date_today = datetime.date.today() + datetime.timedelta(days=30)
                # else:
                #     date_today = datetime.date.today() + datetime.timedelta(days=60)

                booking.date_delivery = datetime.date.today()
                if booking.job_completion_flag == False:
                    booking.job_completion_flag = True
                    if booking.clickgarage_flag == True:
                        new_lead = place_booking(booking.cust_id, booking.cust_name, booking.cust_number, booking.cust_email, booking.cust_regnumber, booking.cust_address,booking.cust_locality, booking.cust_city, booking.service_items,
                                                 booking.cust_make, booking.cust_vehicle_type,booking.cust_model, booking.cust_fuel_varient, str(date_today), "9:30 AM - 12:30 PM", [{'Job':'Servicing/Repair - Reminder','Price':'0'}], False, "0", "NA",
                                                 "0", "Repeat Customer", False, "NA", send_sms="0",follow_up_date_book=str(date_today))
                    else:
                        new_lead = place_booking(booking.cust_id, booking.cust_name, booking.cust_number,
                                                 booking.cust_email, booking.cust_regnumber, booking.cust_address,
                                                 booking.cust_locality, booking.cust_city, booking.service_items,
                                                 booking.cust_make, booking.cust_vehicle_type, booking.cust_model,
                                                 booking.cust_fuel_varient, str(date_today), "9:30 AM - 12:30 PM",
                                                 [{'Job':'Servicing/Repair - Reminder','Price':'0'}], False, "0", "NA",
                                                 "0", "Repeat Customer", False, "NA", send_sms="0",owner=booking.booking_owner, follow_up_date_book=str(date_today))
                        # add a lead to the leads data base with follow_up_date as (bike - 60 days , car (bill_amount < 2000) - 30 days, car (bill_amount> 2000) 90 days

        if (status_id == "Feedback Taken"):
            booking.job_completion_flag = True
            None
        #     # send thankyou to the customer
        #     # if positive send sharing links and referral links
        #     # send_sms to customer about vehicle reaching the workshop
        if (status_id == "Cancelled"):
            booking.job_completion_flag = False

        #     # send sms saying sorry to let you go
        #     # send email to the customer about cancellation

        if (status_id == "Escalation"):
            booking.job_completion_flag = False
            if send_sms:
                print "SMS Sent"
                mviews.send_sms_customer(booking.cust_name, booking.cust_number, booking.booking_id, booking.date_booking,
                                     booking.time_booking, estimate=booking.price_total,
                                     status="Escalation")
            booking.escalation_flag = True
            #     # send sms to customer that sorry something happend we will take care of the same - Share number of agent diretly to sort his problems
            #     # send a sorry note to the customer over email

    booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def send_lead(request):
    name = get_param(request, 'name', None)
    number = get_param(request, 'number', None)
    email = get_param(request, 'email', None)
    reg_number = get_param(request, 'reg_number', None)
    address = get_param(request, 'address', None)
    locality = get_param(request, 'locality', None)
    city = get_param(request, 'city', None)
    order_list = get_param(request, 'order_list', None)

    if order_list:
        order_list = json.loads(order_list)
    else:
        order_list = []
    job_summary_int = get_param(request, 'int_summary', None)

    if job_summary_int:
        job_summary_int = json.loads(job_summary_int)
    else:
        job_summary_int = []
    make = get_param(request, 'make', None)
    veh_type = get_param(request, 'veh_type', None)
    model = get_param(request, 'model', None)
    fuel = get_param(request, 'fuel', None)
    date = get_param(request, 'date', None)
    time_str = get_param(request, 'time', None)
    jobsummary_list = get_param(request, 'jobsummary_list', None)

    comment = get_param(request, 'comment', None)
    is_paid = get_param(request, 'is_paid', None)
    paid_amt = get_param(request, 'paid_amt', None)
    coupon = get_param(request, 'coupon', None)
    price_total = get_param(request, 'price_total', None)
    source = get_param(request, 'source', None)
    send_confirm = get_param(request, 'send_confirm', "1")

    oldformat = date
    datetimeobject = datetime.datetime.strptime(oldformat, '%d-%m-%Y')
    newformat = datetimeobject.strftime('%Y-%m-%d')
    date = newformat
    jobsummary_list = json.loads(jobsummary_list)
    obj2 = {}
    obj2['status'] = False
    obj2['result'] = []

    booking_flag = False

    booking = place_booking('', name, number, email, reg_number, address, locality, city, order_list,
                            make, veh_type, model, fuel, date, time_str, jobsummary_list, is_paid, paid_amt, coupon,
                            price_total, source, booking_flag, job_summary_int, send_sms=send_confirm)
    obj2['result'] = {}
    obj2['result']['userid'] = 'None'
    obj2['result']['booking'] = booking
    obj2['status'] = True
    obj2['counter'] = 1
    obj2['msg'] = "Success"
    return HttpResponse(json.dumps(obj2), content_type='application/json')

def get_all_models(request):
    vehicle_type = get_param(request, 'vehicle_type', None)
    # make_id = get_param(request,'make_id',None)
    # model_id = get_param(request,'model_id',None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if vehicle_type == None:
        VehObjs = Vehicle.objects.all().order_by('make')
    elif vehicle_type == "Car":
        VehObjs = Vehicle.objects.filter(car_bike="Car").order_by('make')
    elif vehicle_type == "Bike":
        VehObjs = Vehicle.objects.filter(car_bike="Bike").order_by('make')
    else:
        VehObjs = Vehicle.objects.all().order_by('make')

    # vehicle = None
    # make = None
    # car_bike = None
    for veh in VehObjs:
        obj['result'].append({
            'id' :            veh.id,
            'make':           veh.make,
            'model' :         veh.model,
            'year' :          veh.year,
            'fuel_type' :     veh.fuel_type,
            'full_veh_name':  veh.full_veh_name,
            'aspect_ratio' :  veh.aspect_ratio,
            'type' :          veh.type,
            'car_bike' :      veh.car_bike,
            'engine_oil' :    veh.engine_oil,
            'active' :        veh.active,
        } )

    obj['result'] = {v['model']:v for v in obj['result']}.values()
    obj['result'] = sorted(obj['result'], key=operator.itemgetter('make','model'))
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def get_tax(state):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    taxObjs = Taxes.objects.filter(state=state)
    for tax in taxObjs:
        obj['result'].append({
            'state': tax.state,
            'vat_parts': tax.vat_parts,
            'vat_consumables': tax.vat_consumable,
            'vat_lube': tax.vat_lubes,
            'service_tax': tax.service_tax,
        })
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return obj


def get_all_taxes(request):
    state = get_param(request, 'state', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if state == None or state == "":
        taxObjs = Taxes.objects.all()
    else:
        taxObjs = Taxes.objects.filter(state=state)

    for tax in taxObjs:
        obj['result'].append({
            'state':tax.state               ,
            'vat_parts':tax.vat_parts             ,
            'vat_consumables':tax.vat_consumable               ,
            'vat_lube':tax.vat_lubes              ,
            'service_tax':tax.service_tax               ,

        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def generate_bill(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    data_id                 = get_param(request,'data_id', None)
    bill_owner              = get_param(request,'bill_owner',None)
    total_amount            = get_param(request,'total_amount',None)
    part_amount             = get_param(request,'part_amount',None)
    lube_amount             = get_param(request,'lube_amount',None)
    consumable_amount       = get_param(request,'consumable_amount',None)
    labour_amount           = get_param(request, 'labour_amount', None)
    vat_part                = get_param(request, 'vat_part', None)
    vat_lube                = get_param(request, 'vat_lube', None)
    vat_consumable          = get_param(request, 'vat_consumable', None)
    service_tax             = get_param(request, 'service_tax', None)
    payment_mode            = get_param(request, 'payment_mode', None)
    full_agent_name         = get_param(request, 'full_agent_name', None)
    agent_address           = get_param(request, 'agent_address', None)
    agent_vat_no            = get_param(request, 'agent_vat_no', None)
    agent_cin               = get_param(request, 'agent_cin', None)
    agent_stax              = get_param(request, 'agent_stax', None)
    state                   = get_param(request, 'state', None)
    vat_part_percent        = get_param(request, 'vat_part_percent', None)
    vat_lube_percent        = get_param(request, 'vat_lube_percent', None)
    vat_consumable_percent  = get_param(request, 'vat_consumable_percent', None)
    service_tax_percent     = get_param(request, 'service_tax_percent', None)
    notes                   = get_param(request, 'notes', None)
    cust_name               = get_param(request,'cust_name',None)
    cust_address            = get_param(request,'cust_address',None)
    cust_locality           = get_param(request,'cust_locality',None)
    cust_city               = get_param(request,'cust_city',None)
    reg_number              = get_param(request,'reg_number',None)
    vehicle                 = get_param(request,'vehicle',None)
    service_items           = get_param(request,'service_items',None)
    invoice_number          = get_param(request,'invoice_number',None)
    booking = None
    agent_vas_share = 0
    agent_part_share = 0
    agent_lube_share = 0
    agent_consumable_share = 0
    agent_denting_share = 0
    agent_labour_share = 0
    service_items = json.loads(service_items)
    if data_id != None and data_id != "":
        booking = Bookings.objects.filter(id=data_id)[0]
        booking_id = booking.booking_id

    if invoice_number == "Pre-Invoice":
        pre_invoice = True
        bill_type = "Pre-Invoice"
        invoice_number = 0
    else:
        pre_invoice = False
        bill_type = "Invoice"
        if invoice_number == "" or invoice_number == None:
            tran_len = len(Bills.objects.filter(owner=bill_owner,bill_type = "Invoice"))
            if tran_len:
                tran = Bills.objects.filter(owner=bill_owner,bill_type = "Invoice").aggregate(Max('invoice_number'))
                invoice_number = int(tran['invoice_number__max'] + 1)
            else:
                invoice_number = 10000

    # if bill_owner == "Agent Bill" or bill_owner = "":
    #     bill_owner

    if booking:
        billsobjs = Bills.objects.filter(booking_data_id=data_id)
        for bill in billsobjs:
            bill.status = "Cancelled"
            bill.save()


    if booking:
        clickgarage_flag = booking.clickgarage_flag
        cust_number = booking.cust_number
        cust_email = booking.cust_email
        if bill_owner == "Agent Bill" or bill_owner == "":
            bill_owner = booking.agent
        if not pre_invoice:
            if booking.clickgarage_flag:
                agent = CGUserNew.objects.filter(id=booking.agent)[0]
                if agent:
                    agent_vas_share = agent.agent_vas_share
                    agent_part_share = agent.agent_part_share
                    agent_lube_share = agent.agent_lube_share
                    agent_consumable_share = agent.agent_consumable_share
                    agent_denting_share = agent.agent_denting_share
                    agent_labour_share = agent.agent_labour_share
                else:
                    agent_vas_share = 0
                    agent_part_share = 0
                    agent_lube_share = 0
                    agent_consumable_share = 0
                    agent_denting_share = 0
                    agent_labour_share = 0

            else:
                agent_vas_share = 0
                agent_part_share = 0
                agent_lube_share = 0
                agent_consumable_share = 0
                agent_denting_share = 0
                agent_labour_share = 0

            new_estimate_timestamp = time.time()
            estimate_by_id = request.user.id
            estimate_by_number = request.user.contact_no
            estimate_by_name = request.user.first_name + " " + request.user.last_name
            old_estimate = booking.service_items
            booking.service_items = service_items
            total_price = 0
            total_part = 0
            total_labour = 0
            total_discount = 0
            # new addition
            clickgarage_part_share = 0
            total_part_comm = 0
            total_part_pre_tax = 0
            clickgarage_labour_share = 0
            total_labour_comm = 0
            total_labour_pre_tax = 0
            clickgarage_denting_share = 0
            total_denting_comm = 0
            total_denting_pre_tax = 0
            clickgarage_vas_share = 0
            total_vas_comm = 0
            total_vas_pre_tax = 0
            clickgarage_lube_share = 0
            total_lube_comm = 0
            total_lube_pre_tax = 0
            clickgarage_consumable_share = 0
            total_consumable_comm = 0
            total_consumable_pre_tax = 0
            clickgarage_discount_share = 0
            total_discount_comm = 0
            total_discount_pre_tax = 0
            total_commission = 0
            total_puchase_price = 0
            obj_part = {}
            obj_lube = {}
            obj_consumable = {}
            obj_vas = {}
            obj_denting = {}
            obj_labour = {}
            obj_discount = {}
            commission = []
            estimate2 = []

            # print estimate
            for item in service_items:
                obj2 = {}
                # print item
                if item['type'] == "Part":
                    total_price = total_price + float(item['price'])
                    total_part = total_part + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])
                elif item['type'] == "Consumable":
                    total_price = total_price + float(item['price'])
                    total_part = total_part + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])
                elif item['type'] == "Lube":
                    total_price = total_price + float(item['price'])
                    total_part = total_part + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])

                elif item['type'] == "Labour":
                    total_price = total_price + float(item['price'])
                    total_labour = total_labour + float(item['price'])
                    total_puchase_price = total_puchase_price + float(item['purchase_price'])

                elif item['type'] == "Discount":
                    total_price = total_price - float(item['price'])
                    total_discount = total_discount + float(item['price'])
                    total_puchase_price = total_puchase_price - float(item['purchase_price'])
                    applicable_tax = 0

                if item['settlement_cat'] == "Part":
                    applicable_commission_share = float(agent_part_share)
                    clickgarage_part_share = clickgarage_part_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_part_comm = total_part_comm + float(item['purchase_price'])
                    total_part_pre_tax = total_part_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                elif item['settlement_cat'] == "Labour":
                    applicable_commission_share = float(agent_labour_share)
                    clickgarage_labour_share = clickgarage_labour_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_labour_comm = total_labour_comm + float(item['purchase_price'])
                    total_labour_pre_tax = total_labour_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                elif item['settlement_cat'] == "VAS":
                    applicable_commission_share = float(agent_vas_share)
                    clickgarage_vas_share = clickgarage_vas_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_vas_comm = total_vas_comm + float(item['purchase_price'])
                    total_vas_pre_tax = total_vas_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                elif item['settlement_cat'] == "Denting":
                    applicable_commission_share = float(agent_denting_share)
                    clickgarage_denting_share = clickgarage_denting_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_denting_comm = total_denting_comm + float(item['purchase_price'])
                    total_denting_pre_tax = total_denting_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                elif item['settlement_cat'] == "Lube":
                    applicable_commission_share = float(agent_lube_share)
                    clickgarage_lube_share = clickgarage_lube_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_lube_comm = total_lube_comm + float(item['purchase_price'])
                    total_lube_pre_tax = total_lube_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                elif item['settlement_cat'] == "Consumable":
                    applicable_commission_share = float(agent_consumable_share)
                    clickgarage_consumable_share = clickgarage_consumable_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_consumable_comm = total_consumable_comm + float(item['purchase_price'])
                    total_consumable_pre_tax = total_consumable_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                elif item['settlement_cat'] == "Discount":
                    applicable_commission_share = 0
                    clickgarage_discount_share = clickgarage_discount_share + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                    total_discount_comm = total_discount_comm + float(item['purchase_price'])
                    total_discount_pre_tax = total_discount_pre_tax + float(item['purchase_price_pretax'])
                    total_commission = total_commission + (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100)
                print item
                obj2 = {
                    'comment': item['comment'],
                    'name': item['name'],
                    'settlement_cat': item['settlement_cat'],
                    'price': item['price'],
                    'unit_price': item['unit_price'],
                    'pre_tax_price': item['pre_tax_price'],
                    'type': item['type'],
                    'approved': item['approved'],
                    'quantity': item['quantity'],
                    'purchase_price': item['purchase_price'],
                    'purchase_price_pretax': float(item['purchase_price_pretax']),
                    'clickgarage_share': (float(item['purchase_price_pretax']) * (applicable_commission_share) / 100),
                }
                print obj2
                estimate2.append(obj2)




                # print item
            booking.service_items = estimate2
            booking.price_total = str(total_price)
            booking.purchase_price_total = str(total_puchase_price)
            booking.price_labour = str(total_labour)
            booking.price_part = str(total_part)
            booking.price_discount = str(total_discount)
            obj_part = {"type": "Part",
                        "purchase_price": total_part_comm,
                        "purchase_price_pre_tax": total_part_pre_tax,
                        "clickgarage_share": round(clickgarage_part_share,0),
                        "share_percent": agent_part_share}
            commission.append(obj_part)

            obj_labour = {"type": "Labour",
                          "purchase_price": total_labour_comm,
                          "purchase_price_pre_tax": total_labour_pre_tax,
                          "clickgarage_share": round(clickgarage_labour_share,0),
                          "share_percent": agent_labour_share}
            commission.append(obj_labour)

            obj_vas = {"type": "VAS",
                       "purchase_price": total_vas_comm,
                       "purchase_price_pre_tax": total_vas_pre_tax,
                       "clickgarage_share": round(clickgarage_vas_share,0),
                       "share_percent": agent_vas_share}
            commission.append(obj_vas)

            obj_denting = {"type": "Denting",
                           "purchase_price": total_denting_comm,
                           "purchase_price_pre_tax": total_denting_pre_tax,
                           "clickgarage_share": round(clickgarage_denting_share,0),
                           "share_percent": agent_denting_share}
            commission.append(obj_denting)

            obj_consumable = {"type": "Consumable",
                              "purchase_price": total_consumable_comm,
                              "purchase_price_pre_tax": total_consumable_pre_tax,
                              "clickgarage_share": round(clickgarage_consumable_share,0),
                              "share_percent": agent_consumable_share}
            commission.append(obj_consumable)

            obj_lube = {"type": "Lube",
                        "purchase_price": total_lube_comm,
                        "purchase_price_pre_tax": total_lube_pre_tax,
                        "clickgarage_share": round(clickgarage_lube_share,0),
                        "share_percent": agent_lube_share}
            commission.append(obj_lube)

            obj_discount = {"type": "Discount",
                            "purchase_price": total_discount_comm,
                            "purchase_price_pre_tax": total_discount_pre_tax,
                            "clickgarage_share": round(clickgarage_discount_share,0),
                            "share_percent": 0}
            commission.append(obj_discount)

            booking.commission = commission
            booking.commission_total = str(round(total_commission,0))

            a = booking.estimate_history.append(
                {"timestamp": new_estimate_timestamp, "change_by_userid": estimate_by_id,
                 "change_by_number": estimate_by_number, "change_by_name": estimate_by_name,
                 'estimate': old_estimate})

            booking.save()


    else:
        if bill_owner == "Agent Bill" or bill_owner == "":
            bill_owner = request.user.id
        data_id = ""
        cust_number = ""
        cust_email = ""
        if request.user.is_admin or request.user.is_staff:
            clickgarage_flag = True
        else:
            clickgarage_flag = False

    date_today = datetime.date.today()
    # date_due = date_today
    time_stamp = time.time()
    status = "Generated"


    tt = Bills(clickgarage_flag         = clickgarage_flag
               , invoice_number         = str(invoice_number)
               , total_amount           = total_amount
               , part_amount            = part_amount
               , lube_amount            = lube_amount
               , consumable_amount      = consumable_amount
               , labour_amount          = labour_amount
               , vat_part               = vat_part
               , vat_lube               = vat_lube
               , vat_consumable         = vat_consumable
               , service_tax            = service_tax
               , components             = service_items
               , status                 = status
               , date_created           = date_today
               , time_stamp             = time_stamp
               , owner                  = bill_owner
               , booking_data_id        = data_id
               # , file_name              = bill_type+'-'+str(invoice_number)+'_'+data_id+'.pdf'
               # , payment_status         = payment_status
               # , amount_paid            = amount_paid
               , payment_mode           = payment_mode
               , notes                  = notes
               , state                  = state
               , vat_part_percent       =vat_part_percent
               , vat_lube_percent       =vat_lube_percent
               , vat_consumable_percent =vat_consumable_percent
               , service_tax_percent    =service_tax_percent
               , agent_name             =full_agent_name
               , agent_address          =agent_address
               , agent_vat_no           =agent_vat_no
               , agent_cin              =agent_cin
               , agent_stax             =agent_stax
               , cust_name              =cust_name
               , cust_address           =cust_address
               , cust_locality          =cust_locality
               , cust_city              =cust_city
               , reg_number             =reg_number
               , vehicle                =vehicle
               ,bill_type               = bill_type
               ,date_due                = date_today
               ,cust_number             = cust_number
               ,cust_email              = cust_email
               ,amount_paid             = False
               )
    tt.save()
    tt2 = Bills.objects.filter(clickgarage_flag=clickgarage_flag, owner=bill_owner, time_stamp= time_stamp, booking_data_id=data_id, status="Generated", bill_type=bill_type, invoice_number=invoice_number)[0]
    if booking:
        booking.bill_id = tt2.id
        if tt2.bill_type == "Pre-Invoice":
            booking.bill_generation_flag  = False
        else:
            booking.bill_generation_flag = True
        booking.save()

    import pdfkit
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    print vat_part
    print service_tax
    if pre_invoice:
        if booking:
            html = mviews.bill_html(agent_name = full_agent_name,agent_address= agent_address,invoice_number="Pre-Invoice",booking_id = booking_id,created_date = date_today ,tin_number = agent_vat_no, cin_number=agent_cin,stax_number = agent_stax,cust_name= cust_name,cust_address= cust_address,cust_locality=cust_locality,cust_city=cust_city,cust_reg=reg_number,cust_veh=vehicle,service_items = service_items,vat_part_percent=vat_part_percent,vat_lube_percent=vat_lube_percent,vat_consumable_percent=vat_consumable_percent,stax_percent=service_tax_percent,vat_part=vat_part,vat_lube=vat_lube,vat_consumable=vat_consumable,stax_amount=service_tax,total=total_amount,recommendation=notes,logo=clickgarage_flag)
        else:
            html = mviews.bill_html(agent_name = full_agent_name,agent_address= agent_address,invoice_number="Pre-Invoice",booking_id = "",created_date = date_today ,tin_number = agent_vat_no, cin_number=agent_cin,stax_number = agent_stax,cust_name= cust_name,cust_address= cust_address,cust_locality=cust_locality,cust_city=cust_city,cust_reg=reg_number,cust_veh=vehicle,service_items = service_items,vat_part_percent=vat_part_percent,vat_lube_percent=vat_lube_percent,vat_consumable_percent=vat_consumable_percent,stax_percent=service_tax_percent,vat_part=vat_part,vat_lube=vat_lube,vat_consumable=vat_consumable,stax_amount=service_tax,total=total_amount,recommendation=notes,logo=clickgarage_flag)
    else:
        if booking:
            html = mviews.bill_html(agent_name=full_agent_name, agent_address=agent_address, invoice_number=invoice_number,
                                    booking_id=booking_id, created_date=date_today, tin_number=agent_vat_no, cin_number=agent_cin,
                                    stax_number=agent_stax, cust_name=cust_name, cust_address=cust_address,
                                    cust_locality=cust_locality, cust_city=cust_city, cust_reg=reg_number, cust_veh=vehicle,
                                    service_items=service_items, vat_part_percent=vat_part_percent,
                                    vat_lube_percent=vat_lube_percent, vat_consumable_percent=vat_consumable_percent,
                                    stax_percent=service_tax_percent, vat_part=vat_part, vat_lube=vat_lube,
                                    vat_consumable=vat_consumable, stax_amount=service_tax, total=total_amount,
                                    recommendation=notes,logo=clickgarage_flag)
        else:
            html = mviews.bill_html(agent_name=full_agent_name, agent_address=agent_address,
                                    invoice_number=invoice_number,
                                    booking_id="", created_date=date_today, tin_number=agent_vat_no,
                                    cin_number=agent_cin,
                                    stax_number=agent_stax, cust_name=cust_name, cust_address=cust_address,
                                    cust_locality=cust_locality, cust_city=cust_city, cust_reg=reg_number,
                                    cust_veh=vehicle,
                                    service_items=service_items, vat_part_percent=vat_part_percent,
                                    vat_lube_percent=vat_lube_percent, vat_consumable_percent=vat_consumable_percent,
                                    stax_percent=service_tax_percent, vat_part=vat_part, vat_lube=vat_lube,
                                    vat_consumable=vat_consumable, stax_amount=service_tax, total=total_amount,
                                    recommendation=notes,logo=clickgarage_flag)
            #     import subprocess
            #
    if socket.gethostname().startswith('ip-'):
        if PRODUCTION:
            cmd = pdfkit.from_string(html,'/home/ubuntu/beta/website/Bills/'+bill_type+'-'+str(invoice_number)+'_'+tt2.id+'.pdf')
        else:
            cmd = pdfkit.from_string(html,'/home/ubuntu/testing/website/Bills/'+bill_type+'-'+str(invoice_number)+'_'+tt2.id+'.pdf')
    else:
        cmd = pdfkit.from_string(html, '/home/shashwat/Desktop/codebase/website/Bills/' + bill_type + '-' + str(invoice_number) + '_' + tt2.id + '.pdf')


    if socket.gethostname().startswith('ip-'):
        if PRODUCTION:
            obj['filename'] = '/home/ubuntu/beta/website/Bills/'+bill_type+'-'+str(invoice_number)+'_'+tt2.id+'.pdf'
        else:
            obj['filename'] = '/home/ubuntu/testing/website/Bills/'+bill_type+'-'+str(invoice_number)+'_'+tt2.id+'.pdf'
    else:
        obj['filename'] = '/home/shashwat/Desktop/codebase/website/Bills/'+bill_type+'-'+str(invoice_number)+'_'+tt2.id+'.pdf'
        #
        #
    tt2.file_name = obj['filename']
    tt2.save()
    f = open(obj['filename'], 'r')
    if tt2.bill_type == "Pre-Invoice":
        filename = bill_type+'_'+tt2.id+'.pdf'
    else:
        filename = bill_type + '_' + str(invoice_number) + '_' + tt2.id + '.pdf'
    content = f.read()
    f.close()
    response_file = HttpResponse(content, mimetype='application/pdf')
    response_file['Content-Disposition'] = 'attachement; filename=' + filename

    obj['msg'] = "Bill Generated"
    obj['status'] = True
    obj['counter'] = 1

    return response_file
    return HttpResponse(json.dumps(obj), content_type='application/json')

# import pdfkit

# def print_page (url,output):
#     pdfkit.from_url(url, output)

# def get_bill(bill_id):
#     obj = {}
#     obj['status'] = False
#     obj['result'] = []
#     jobObjs = Bills.objects.filter(id = bill_id)
#
#     for job in jobObjs:
#         obj['result'].append({
#             'id': job.id,
#             'clickgarage_flag': job.clickgarage_flag,
#             'invoice_number': job.invoice_number,
#             'total_amount': job.total_amount,
#             'part_amount': job.part_amount,
#             'lube_amount': job.lube_amount,
#             'consumable_amount': job.consumable_amount,
#             'labour_amount': job.labour_amount,
#             'vat_part': job.vat_part,
#             'vat_lube': job.vat_lube,
#             'vat_consumable': job.vat_consumable,
#             'service_tax': job.service_tax,
#             'componenents': job.componenents,
#             'status': job.status,
#             'booking_id': job.booking_id,
#             'date_created': str(job.date_created),
#             # 'date_modified    ': str(job.date_modified),
#             'time_stamp': job.time_stamp,
#             'owner': job.owner,
#             'file_name': job.file_name,
#             'payment_status': job.payment_status,
#             'amount_paid': job.amount_paid,
#             'payment_mode': job.payment_mode
#         })
#
#     obj['status'] = True
#     obj['counter'] = 1
#     obj['msg'] = "Success"
#     return HttpResponse(json.dumps(obj), content_type='application/json')

def add_modify_subscription(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    sub_id                 = get_param(request, 'sub_id', None)
    cust_fname              = get_param(request, 'cust_fname',None)
    cust_lname              = get_param(request, 'cust_lname',None)
    cust_num_p              = get_param(request, 'cust_num_p',None)
    cust_num_s              = get_param(request, 'cust_num_s',None)
    cust_email              = get_param(request, 'cust_email',None)
    cust_add                = get_param(request, 'cust_add',None)
    cust_loc                = get_param(request, 'cust_loc',None)
    cust_city               = get_param(request, 'cust_city',None)
    cust_state              = get_param(request, 'cust_state', None)
    make                    = get_param(request, 'make', None)
    veh_type                = get_param(request, 'veh_type', None)
    model                   = get_param(request, 'model', None)
    fuel                    = get_param(request, 'fuel', None)
    vehicle_vin             = get_param(request, 'vehicle_vin', None)
    vehicle_regno           = get_param(request, 'vehicle_regno', None)
    sub_type                = get_param(request, 'sub_type', None)
    pack_name               = get_param(request, 'pack_name', None)
    date_start              = get_param(request, 'date_start', None)
    date_end                = get_param(request, 'date_end', None)
    comment                 = get_param(request, 'comment', None)
    is_active               = get_param(request, 'is_active', None)
    paid_amt                = get_param(request, 'paid_amt', None)
    source                  = get_param(request,'source',None)
    status                  = get_param(request, 'status', None)
    date_veh_purchase       = get_param(request, 'date_veh_purchase', None)

    if date_veh_purchase != None:
        oldformat_p = date_veh_purchase
        datetimeobject = datetime.datetime.strptime(oldformat_p, '%d-%m-%Y')
        newformat_p = datetimeobject.strftime('%Y-%m-%d')
        date_veh_purchase = newformat_p

    if date_start != None:
        oldformat_s = date_start
        datetimeobject = datetime.datetime.strptime(oldformat_s, '%d-%m-%Y')
        newformat_s = datetimeobject.strftime('%Y-%m-%d')
        date_start = newformat_s

    if date_end != None:
        oldformat_e = date_end
        datetimeobject = datetime.datetime.strptime(oldformat_e, '%d-%m-%Y')
        newformat_e = datetimeobject.strftime('%Y-%m-%d')
        date_end = newformat_e

    if is_active == None:
        active = False
    else:
        if is_active == "true":
            active = True
        else:
            active = False

    cust_fname = cleanstring(cust_fname).title()
    cust_lname = cleanstring(cust_lname).title()
    cust_add = cleanstring(cust_add).title()
    cust_loc = cleanstring(cust_loc).title()
    cust_city = cleanstring(cust_city).title()
    cust_state = cleanstring(cust_state).title()

    cust_full_name = cust_fname +' '+ cust_lname
    if request.user.is_staff or request.user.is_admin:
        if sub_id == "" or sub_id == None:
            user = create_check_user(name=cust_full_name,number=cust_num_p)

            address2 = {'address': cust_add, 'locality': cust_loc, 'city': cust_city}
            if address2 not in user.user_saved_address:
                user.user_saved_address.append(address2)
            vehicle = {'type': veh_type, 'make': make, 'model': model, 'fuel': fuel, "reg_num": vehicle_regno}
            if vehicle not in user.user_veh_list:
                user.user_veh_list.append(vehicle)
            if cust_email not in user.email_list:
                user.email_list.append(cust_email)
            user.email = cust_email
            user.save()
            print is_active
            subs_id = 100000
            tran_len = len(Subscriptions.objects.all())
            status = "Under Review"
            if tran_len:
                tran = Subscriptions.objects.all().aggregate(Max('subscription_id'))
                subs_id = int(tran['subscription_id__max'] + 1)
            tt = Subscriptions(booking_timestamp       = time.time()
                               ,subscription_id         = subs_id
                               ,cust_id                 = user.id
                               ,cust_fname              = cust_fname
                               ,cust_lname              = cust_lname
                               ,cust_make               = make
                               ,cust_model              = model
                               ,cust_vehicle_type       = veh_type
                               ,cust_fuel_varient       = fuel
                               ,cust_regnumber          = vehicle_regno
                               ,cust_vehicle_vin        = vehicle_vin
                               ,cust_number_primary     = cust_num_p
                               ,cust_number_secondary   = cust_num_s
                               ,cust_email              = cust_email
                               ,cust_address            = cust_add
                               ,cust_locality           = cust_loc
                               ,cust_city               = cust_city
                               , cust_state              = cust_state
                               ,subscription_type        = sub_type
                               ,package_name            = pack_name
                               ,date_start              = date_start
                               ,date_end                = date_end
                               ,is_active               = active
                               ,amount_paid             = paid_amt
                               ,status                  = status
                               ,comment                 = comment
                               ,source                  = source
                               ,date_veh_purchase       = date_veh_purchase
                               )
            tt.save()
        else:
            sub = Subscriptions.objects.filter(subscription_id = sub_id)[0]
            user = create_check_user(name=cust_full_name,number=cust_num_p)

            address2 = {'address': cust_add, 'locality': cust_loc, 'city': cust_city}
            if address2 not in user.user_saved_address:
                user.user_saved_address.append(address2)
            vehicle = {'type': veh_type, 'make': make, 'model': model, 'fuel': fuel, "reg_num": vehicle_regno}
            if vehicle not in user.user_veh_list:
                user.user_veh_list.append(vehicle)
            if cust_email not in user.email_list:
                user.email_list.append(cust_email)
            user.email = cust_email
            user.save()

            if cust_fname:
                sub.cust_fname = cust_fname
            if cust_lname:
                sub.cust_lname = cust_lname
            if make:
                sub.cust_make = make
            if model:
                sub.cust_model = model
            if veh_type:
                sub.cust_vehicle_type = veh_type
            if fuel:
                sub.cust_fuel_varient = fuel
            if vehicle_regno:
                sub.cust_regnumber = vehicle_regno
            if vehicle_vin:
                sub.cust_vehicle_vin = vehicle_vin
            if cust_num_p:
                sub.cust_number_primary = cust_num_p
            if cust_num_s:
                sub.cust_number_secondary = cust_num_s
            if cust_email:
                sub.cust_email = cust_email
            if cust_add:
                sub.cust_address = cust_add
            if cust_loc:
                sub.cust_locality = cust_loc
            if cust_city:
                sub.cust_city = cust_city
            if cust_state:
                sub.cust_state = cust_state
            if sub_type:
                sub.subscription_type = sub_type
            if date_start:
                sub.date_start = date_start
            if date_end:
                sub.date_end = date_end
            if date_veh_purchase:
                sub.date_veh_purchase = date_veh_purchase
            if is_active:
                sub.is_active = active
            if paid_amt:
                sub.amount_paid = paid_amt
            if status:
                sub.status = status
            if comment:
                sub.comment = comment
            if source:
                sub.source = source
            sub.save()
    obj['status'] = True
    obj['result'] = "Success"
    # obj['auth_rights'] = {'admin' : request.user.is_admin, 'b2b': request.user.is_b2b, 'agent': request.user.is_agent, 'staff':request.user.is_staff}
    return HttpResponse(json.dumps(obj), content_type='application/json')

def view_all_subscription(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    subs_id = get_param(request, 'subs_id', None)
    if subs_id == None:
        jobObjs = Subscriptions.objects.all()
    else:
        jobObjs = Subscriptions.objects.filter(id=subs_id)

    for job in jobObjs:
        if job.date_veh_purchase != None:
            oldformat_p = str(job.date_veh_purchase)
            datetimeobject = datetime.datetime.strptime(oldformat_p, '%Y-%m-%d')
            newformat_p = datetimeobject.strftime('%d-%m-%Y')
        else:
            newformat_p = "None"

        if job.date_start  != None:
            oldformat_s = str(job.date_start)
            datetimeobject = datetime.datetime.strptime(oldformat_s, '%Y-%m-%d')
            newformat_s = datetimeobject.strftime('%d-%m-%Y')
        else:
            newformat_s = "None"

        if job.date_end != None:
            oldformat_e = str(job.date_end)
            datetimeobject = datetime.datetime.strptime(oldformat_e, '%Y-%m-%d')
            newformat_e = datetimeobject.strftime('%d-%m-%Y')
        else:
            newformat_e = "None"

        obj['result'].append({
            'id': job.id,
            'booking_timestamp': job.booking_timestamp,
            'subscription_id': job.subscription_id,
            'cust_id': job.cust_id,
            'cust_fname': job.cust_fname,
            'cust_lname': job.cust_lname,
            'cust_make': job.cust_make,
            'cust_model': job.cust_model,
            'cust_vehicle_type': job.cust_vehicle_type,
            'cust_fuel_varient': job.cust_fuel_varient,
            'cust_regnumber': job.cust_regnumber,
            'cust_vehicle_vin': job.cust_vehicle_vin,
            'cust_number_primary': job.cust_number_primary,
            'cust_number_secondary': job.cust_number_secondary,
            'cust_email': job.cust_email,
            'cust_address': job.cust_address,
            'cust_locality': job.cust_locality,
            'cust_city': job.cust_city,
            'cust_state': job.cust_state,
            'subscription_type': job.subscription_type,
            'package_name': job.package_name,
            'date_start': newformat_s,
            'date_end': newformat_e,
            'date_veh_purchase': newformat_p,
            'is_active': job.is_active,
            'amount_paid': job.amount_paid,
            'status': job.status,
            'comment': job.comment,
            'source': job.source
        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def send_sms_campaign(request):
    obj = {}
    obj['status'] = False
    obj['result'] = {}
    message = get_param(request, 'message', None)
    if request.user.is_staff or request.user.is_admin:
        tranObjs = CGUserNew.objects.all(clickgarage_flag = True)

    if request.user.is_agent:
        tranObjs = CGUserNew.objects.filter(owner_user=request.user.id)
    numbers = []
    numberString = ""
    for tran in tranObjs:
        numbers.append(tran.contact_no)

    numberString = ",".join(numbers)
    user1 = request.user
    sms_credits = user1.agent_sms_credits
    if request.user.is_staff or request.user.is_admin:
        mviews.send_promo_campaign_agent(numberString,message)
    if request.user.is_agent:
        message_length = len(message)
        credits_per_message = math.ceil(float(message_length)/160)
        num_sms = len(numbers) * credits_per_message

        if num_sms <= request.user.agent_sms_credits:
            mviews.send_promo_campaign_cg(numberString,message)
            obj['result']['msg'] = "SMS's Sent! Campaign Success"
            num_sms_left = sms_credits - num_sms

            request.user.agent_sms_credits = num_sms_left

            request.user.save()
        else:
            obj['result']['msg'] = "Insufficient Credits! Campaign Failed"

    print num_sms
    print num_sms_left
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def download_pdf(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    file_name = get_param(request, 'file_name', None)
    f = open(file_name, 'r')
    content = f.read()
    f.close()
    filename_list = file_name.split('/')
    filename_len = len(filename_list) -1
    file_name_out = filename_list[filename_len]
    response_file = HttpResponse(content, mimetype='application/pdf')
    response_file['Content-Disposition'] = 'attachement; filename=' + file_name_out
    obj['msg'] = "File Downloaded"
    obj['status'] = True
    obj['counter'] = 1
    return response_file

# def export_bookings():


# <<---- Checking Code ---->>

def view_all_bills(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    data_id = get_param(request, 'data_id', None)
    bill_type = get_param(request, 'bill_type', None)

    if request.user.is_admin:
        if (data_id == None or data_id == ""):
            jobObjs = Bills.objects.all().order_by('-time_stamp')
        else:
            jobObjs = Bills.objects.filter(id=data_id)

    elif request.user.is_staff:
        if (data_id == None or data_id == ""):
            jobObjs = Bills.objects.filter(clickgarage_flag=True).order_by('-time_stamp')
        else:
            jobObjs = Bills.objects.filter(id=data_id)
    elif request.user.is_b2b:
        if data_id == None or data_id == "":
            jobObjs = Bills.objects.filter(cust_id=request.user.id).order_by('-time_stamp')
        else:
            jobObjs = Bills.objects.filter(id=data_id)

    elif request.user.is_agent:
        if data_id == None or data_id == "":
            jobObjs = Bills.objects.filter(owner=request.user.id).order_by('-time_stamp')
        else:
            jobObjs = Bills.objects.filter(id=data_id)
    else:
        jobObjs = None

    if bill_type != None and bill_type != "":
        jobObjs = jobObjs.filter(bill_type=bill_type)

    # jobObjs = Bills.objects.all()

    for job in jobObjs:
        booking = None
        booking_id = "NA"
        date_job_created = "NA"
        if job.booking_data_id != "":
            booking = Bookings.objects.filter(id = job.booking_data_id)[0]
        if booking:
            booking_id = booking.booking_id
            # date_job_created = booking.date_booking
            oldformat_j = str(booking.date_booking)
            datetimeobject = datetime.datetime.strptime(oldformat_j, '%Y-%m-%d')
            date_job_created = datetimeobject.strftime('%d-%m-%Y')

        oldformat_d = str(job.date_due)
        datetimeobject = datetime.datetime.strptime(oldformat_d, '%Y-%m-%d')
        newformat_d = datetimeobject.strftime('%d-%m-%Y')

        oldformat_c = str(job.date_created)
        datetimeobject = datetime.datetime.strptime(oldformat_c, '%Y-%m-%d')
        newformat_c = datetimeobject.strftime('%d-%m-%Y')

        obj['result'].append({
            'id': job.id,
            'clickgarage_flag': job.clickgarage_flag,
            'invoice_number': job.invoice_number,
            'total_amount': job.total_amount,
            'part_amount': job.part_amount,
            'lube_amount': job.lube_amount,
            'consumable_amount': job.consumable_amount,
            'labour_amount': job.labour_amount,
            'vat_part': job.vat_part,
            'vat_lube': job.vat_lube,
            'vat_consumable': job.vat_consumable,
            'service_tax': job.service_tax,
            'components': job.components,
            'status': job.status,
            'booking_data_id': job.booking_data_id,
            'booking_id': booking_id,
            'date_job_created':str(date_job_created),
            'date_created': newformat_c,
            # 'date_modified    ': str(job.date_modified),
            'time_stamp': job.time_stamp,
            'owner': job.owner,
            'file_name': job.file_name,
            'payment_status': job.payment_status,
            'amount_paid': job.amount_paid,
            'payment_mode': job.payment_mode,
            'notes': job.notes,
            'state': job.state,
            'vat_part_percent': job.vat_part_percent,
            'vat_lube_percent': job.vat_lube_percent,
            'vat_consumable_percent': job.vat_consumable_percent,
            'service_tax_percent': job.service_tax_percent,
            'agent_name': job.agent_name,
            'agent_address': job.agent_address,
            # 'agent_locality': job.agent_locality,
            # 'agent_city': job.agent_city,
            'agent_vat_no': job.agent_vat_no,
            'agent_cin': job.agent_cin,
            'agent_stax': job.agent_stax,
            'cust_name': job.cust_name,
            'reg_number': job.reg_number,
            'cust_address': job.cust_address,
            'bill_type': job.bill_type,
            'date_due': newformat_d,
            'cust_email': job.cust_email,
            'cust_number': job.cust_number,

        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')



def update_bill(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    data_id = get_param(request, 'data_id', None)
    cust_number = get_param(request, 'cust_number', None)
    cust_email = get_param(request,'cust_email',None)
    payment_mode = get_param(request, 'payment_mode', None)
    amount_paid = get_param(request, 'amount_paid', None)
    due_date = get_param(request, 'due_date', None)
    status = get_param(request, 'status', None)
    bill = Bills.objects.filter(id=data_id)[0]

    if cust_number != "" and cust_number != None:
        bill.cust_number = cust_number

    if cust_email != "" and cust_email != None:
        bill.cust_email = cust_email

    if payment_mode != "" and payment_mode != None:
        bill.payment_mode = payment_mode

    if amount_paid != "" and amount_paid != None:
        if amount_paid == "true":
            bill.amount_paid = True
        else:
            bill.amount_paid = False

    if due_date != "" and due_date != None:
        oldformat = due_date
        datetimeobject = datetime.datetime.strptime(oldformat, '%d-%m-%Y')
        newformat = datetimeobject.strftime('%Y-%m-%d')
        due_date = newformat
        bill.due_date = due_date

    if status != "" and status != None:
        bill.status = status

    bill.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def send_bill(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    data_id = get_param(request, 'data_id', None)
    cust_number = get_param(request, 'cust_number', None)
    cust_email = get_param(request, 'cust_email', None)
    bill = Bills.objects.filter(id=data_id)[0]
    filename = bill.file_name
    cust_name = bill.cust_name
    mviews.send_bill(cust_name,cust_email,cust_number,filename)
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def settle_freeze_booking(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    data_id = get_param(request, 'data_id', None)
    part_share = get_param(request, 'part_share', None)
    labour_share = get_param(request,'labour_share',None)
    vas_share = get_param(request,'vas_share',None)
    lube_share = get_param(request, 'lube_share', None)
    consumable_share = get_param(request, 'consumable_share', None)
    denting_share = get_param(request, 'denting_share', None)
    to_do = get_param(request, 'to_do', None)
    booking = Bookings.objects.filter(id=data_id)[0]
    if to_do == "Freeze" or to_do == "Settle":
        booking.frozen_flag = True
        if to_do == "Settle":
            booking.settlement_flag = True
        item2 = []
        items = booking.commission
        for item in items:
            if item['type'] == "Part":
                obj_part = {"type": "Part",
                    "purchase_price": item['purchase_price'],
                    "purchase_price_pre_tax":item['purchase_price_pre_tax'],
                    "clickgarage_share": part_share,
                    "share_percent": item['share_percent']}
                item2.append(obj_part)

            if item['type'] == "Labour":
                obj_labour = {"type": "Labour",
                            "purchase_price": item['purchase_price'],
                            "purchase_price_pre_tax": item['purchase_price_pre_tax'],
                            "clickgarage_share": labour_share,
                            "share_percent": item['share_percent']}
                item2.append(obj_labour)

            if item['type'] == "Denting":
                obj_denting = {"type": "Denting",
                            "purchase_price": item['purchase_price'],
                            "purchase_price_pre_tax": item['purchase_price_pre_tax'],
                            "clickgarage_share": denting_share,
                            "share_percent": item['share_percent']}
                item2.append(obj_denting)
            if item['type'] == "Lube":
                obj_lube = {"type": "Lube",
                            "purchase_price": item['purchase_price'],
                            "purchase_price_pre_tax": item['purchase_price_pre_tax'],
                            "clickgarage_share": lube_share,
                            "share_percent": item['share_percent']}
                item2.append(obj_lube)
            if item['type'] == "VAS":
                obj_vas = {"type": "VAS",
                            "purchase_price": item['purchase_price'],
                            "purchase_price_pre_tax": item['purchase_price_pre_tax'],
                            "clickgarage_share": vas_share,
                            "share_percent": item['share_percent']}
                item2.append(obj_vas)
            if item['type'] == "Consumable":
                obj_consumable = {"type": "Consumable",
                            "purchase_price": item['purchase_price'],
                            "purchase_price_pre_tax": item['purchase_price_pre_tax'],
                            "clickgarage_share": consumable_share,
                            "share_percent": item['share_percent']}
                item2.append(obj_consumable)
            if item['type'] == "Discount":
                obj_discount = item
                item2.append(obj_discount)
        booking.commission = item2
        total_comm = float(part_share) + float(labour_share)+ float(denting_share)+ float(lube_share)+ float(vas_share)+ float(consumable_share)
        booking.commission_total = str(total_comm)

    if to_do == "Unsettle":
        booking.settlement_flag = False

    if to_do == "Unfreeze":
        if booking.settlement_flag == False:
            booking.frozen_flag = False
    booking.save()
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def get_all_jobs(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    jobObjs = Services.objects.all()

    for job in jobObjs:
        obj['result'].append({
            'city               ': job.city
            , 'vendor             ': job.vendor
            , 'car_bike           ': job.car_bike
            , 'service_cat        ': job.service_cat
            , 'job_name           ': job.job_name
            , 'job_sub_cat        ': job.job_sub_cat
            , 'type               ': job.type
            , 'total_price        ': job.total_price
            , 'total_price_comp   ': job.total_price_comp
            , 'doorstep           ': job.doorstep
            , 'year               ': job.year
            , 'fuel_type          ': job.fuel_type
            , 'full_veh_name      ': job.full_veh_name
            , 'aspect_ratio       ': job.aspect_ratio
            , 'job_summary        ': job.job_summary
            , 'job_desc           ': job.job_desc
            , 'job_symptoms       ': job.job_symptoms
            , 'job_features       ': job.job_features
            , 'time               ': job.time
            , 'price_active       ': job.price_active
            , 'priority           ': job.priority
            , 'make               ': job.make
            , 'model              ': job.model
            , 'default_components ': job.default_components
            , 'optional_components': job.optional_components
            , 'total_part         ': job.total_part
            , 'total_labour       ': job.total_labour
            , 'total_discount     ': job.total_discount
        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def get_all_labour(request):
    obj = {}

    obj['status'] = False
    obj['result'] = []
    jobObjs = ServiceLabour.objects.all()

    for job in jobObjs:
        obj['result'].append({
            'city             ': job.city
            , 'vendor           ': job.vendor
            , 'car_bike         ': job.car_bike
            , 'service_cat      ': job.service_cat
            , 'job_name         ': job.job_name
            , 'job_sub_cat      ': job.job_sub_cat
            , 'type             ': job.type
            , 'total_price      ': job.total_price
            , 'total_price_comp ': job.total_price_comp
            , 'doorstep         ': job.doorstep
            # , 'year             ': job.year
            # , 'fuel_type        ': job.fuel_type
            # , 'full_veh_name    ': job.full_veh_name
            # , 'aspect_ratio     ': job.aspect_ratio
            , 'job_summary      ': job.job_summary
            , 'job_desc         ': job.job_desc
            , 'job_symptoms     ': job.job_symptoms
            , 'job_features     ': job.job_features
            , 'time             ': job.time
            , 'price_active     ': job.price_active
            , 'priority         ': job.priority,
        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')




def get_all_part(request):
    obj = {}
    obj['status'] = False
    obj['result'] = []
    jobObjs = ServicePart.objects.all()

    for job in jobObjs:
        obj['result'].append({
            'city               ':job.city               ,
            'vendor             ':job.vendor             ,
            'make               ':job.make               ,
            'model              ':job.model              ,
            'year               ':job.year               ,
            'fuel_type          ':job.fuel_type          ,
            'full_veh_name      ':job.full_veh_name      ,
            'type               ':job.type               ,
            'car_bike           ':job.car_bike           ,
            'doorstep           ':job.doorstep           ,
            'service_cat        ':job.service_cat        ,
            'job_name           ':job.job_name           ,
            'job_sub_cat        ':job.job_sub_cat        ,
            'default_components ':job.default_components ,
            'optional_components':job.optional_components,
            'total_price        ':job.total_price        ,
            'total_price_comp   ':job.total_price_comp

        })

    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')



