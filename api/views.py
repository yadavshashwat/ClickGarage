from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import operator
import json

from models import *
from dataEntry.runentry import carMakers, cleanstring


#login views
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

def fetch_all_cars(request):
    obj = {}
    result = []
    allCars = Car.objects.all()
    for car in allCars:
        result.append({'name':car.name, 'make':car.make, 'aspect_ratio':car.aspect_ratio,'size':car.size, 'id':car.id})

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
            result = {'name':carObj.name, 'make':carObj.make, 'aspect_ratio':carObj.aspect_ratio, 'size':carObj.size,'id':carObj.id}
            obj['result'] = result
            obj['status'] = True

    obj['counter'] = 1
    obj['msg'] = "Success"
    if(HTTPFlag):
        return HttpResponse(json.dumps(obj), content_type='application/json')
    else:
        return obj

def fetch_car_services(request):
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
                ServiceObjs = Servicing.objects.filter(carname = car, brand = make).order_by('odometer')
                #ServiceObjs = Service_wo_sort.objects.order_by('odometer')
                for service in ServiceObjs:
                    obj['result'].append({
                        'id':service.id
                        ,'Name':service.name             
                        ,'Brand':service.brand            
                        ,'Car Name':service.carname          
                        ,'Odometer':service.odometer         
                        ,'Year':service.year             
                        ,'Regular Checks':service.regular_checks   
                        ,'Paid-Free':service.paid_free
                        ,'Parts Replaced':service.part_replacement
                        ,'Dealers list':service.dealer} )
            
            
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_servicedetails(request):
    service_id = get_param(request, 'service_id', None)
    obj = {}
    obj['status'] = False
    obj['result'] = []
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
            if car:
                ServicedetailObjs = ServiceDealerCat.objects.filter(carname = car, brand = make, odometer=odo).order_by('odometer','dealer_category')
                for service in ServicedetailObjs:
                    obj['result'].append({
                        'id':service.id
                          ,'name':service.name
                          ,'brand':service.brand
                          ,'car':service.carname
                          ,'odometer':service.odometer
                          ,'dealer_cat':service.dealer_category
                          ,'parts_list':service.part_replacement
                          ,'parts_price':service.price_parts
                          ,'labour_price':service.price_labour
                          ,'wa_price':service.wheel_alignment
                          ,'wb_price':service.wheel_balancing
                          ,'wa_wb_present':service.WA_WB_Inc
                          ,'dealer_details':service.detail_dealers      } )
            
            
    obj['status'] = True
    obj['counter'] = 1
    obj['msg'] = "Success"
    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_cleaning(request):
    dealers = fetch_all_cleaningdealer(request, False)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if dealers['result'] and len(dealers['result']):
        obj['status'] = True
        for dealer in dealers['result']:
            print dealer
            CleanCatObjs = CleaningServiceCat.objects.filter(vendor = dealer['Name'])
            oneObj = {
                'name':dealer['Name'],
                'list':[]
                                 }
            for service in CleanCatObjs:
                oneObj['list'].append({
                        'id':service.id
                      ,'Name':service.vendor
                      ,'Category':service.category
                      ,'Description':service.description
                })
            obj['result'].append(oneObj)


    return HttpResponse(json.dumps(obj), content_type='application/json')

def fetch_car_vas(request):
    dealers = fetch_all_vasdealer(request, False)
    obj = {}
    obj['status'] = False
    obj['result'] = []
    if dealers['result'] and len(dealers['result']):
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
                          ,'Name':service.vendor
                          ,'Category':service.category
                          ,'Description':service.description
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
                        'Name' : service.name  
                        ,'Brand' : service.brand     
                        ,'Car Name' : service.carname                   
                        ,'Odometer Reading' : service.odometer               
                        ,'Time Reading' : service.year                   
                        ,'Checks done' : service.regular_checks                    
                        ,'Paid-Free' : service.paid_free
                        ,'Parts Replaced' : service.part_replacement       
                        ,'Dealer Category' : service.dealer} )

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
                        ,'Name':service.name                
                        ,'Brand Name':service.brand               
                        ,'Car Name':service.carname             
                        ,'Odometer':service.odometer
                        ,'year':service.year           
                        ,'Dealer Category':service.dealer_category     
                        ,'Parts Replaced':service.part_replacement    
                        ,'Parts Price':service.price_parts         
                        ,'Labour Price':service.price_labour        
                        ,'Wheel Alignment price':service.wheel_alignment     
                        ,'Wheel Balancing Price':service.wheel_balancing     
                        ,'WA-WB':service.WA_WB_Inc
                        ,'Dealer Details':service.detail_dealers
                        ,'Paid-Free':service.paid_free
                        ,'RegularChecks':service.regular_checks       
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
                        ,'Make':service.make           
                        ,'Dealer Category':service.dealer_category
                        ,'Address':service.address        
                        ,'Phone':service.phone          
                        ,'Timing':service.timing         
                        ,'Rating':service.rating         
                        ,'Reviews':service.reviews        } )
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

        result.append({'id':service.id, 'Name':service.vendor           
                        ,'Rating':service.rating           
                        ,'Description':service.description} )
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
                          ,'Name':service.vendor  
                          ,'Category':service.category             
                          ,'Description':service.description               
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
                        ,'Price Labour':service.price_labour    
                        ,'Price Parts':service.price_parts     
                        ,'Total Price':service.price_total     
                        ,'Description':service.description     
                        ,'Rating':service.rating          
                        ,'Reviews':service.reviews                        
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

        result.append({'id':service.id, 'Name':service.vendor           
                        ,'Category':service.category          
                        ,'Description':service.description} )
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
            ,'Name':service.vendor         
            ,'Category':service.category       
            ,'car_cat':service.car_cat        
            ,'Service':service.service        
            ,'Price Labour':service.price_labour   
            ,'Price Parts':service.price_parts    
            ,'Price Total':service.price_total    
            ,'Service Description':service.description    
            ,'Rating':service.rating         
            ,'Reviews':service.reviews        } )
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
                          ,'Name':service.vendor  
                          ,'Category':service.category             
                          ,'Description':service.description               
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
                        ,'Price Labour':service.price_labour    
                        ,'Price Parts':service.price_parts     
                        ,'Total Price':service.price_total     
                        ,'Description':service.description     
                        ,'Rating':service.rating          
                        ,'Reviews':service.reviews                        
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

        result.append({'id':service.id, 'Name':service.vendor           
                        ,'Category':service.category          
                        ,'Description':service.description} )
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
            ,'Name':service.vendor         
            ,'Category':service.category       
            ,'car_cat':service.car_cat        
            ,'Service':service.service        
            ,'Price Labour':service.price_labour   
            ,'Price Parts':service.price_parts    
            ,'Price Total':service.price_total    
            ,'Service Description':service.description    
            ,'Rating':service.rating         
            ,'Reviews':service.reviews        } )
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
    catg_id = get_param(request, 'cat_id', None)
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
            ,'vendor         ':service.vendor           
            ,'brand          ':service.brand            
            ,'carname        ':service.carname          
            ,'ws_type        ':service.ws_type          
            ,'ws_subtype     ':service.ws_subtype       
            ,'price_ws       ':service.price_ws         
            ,'price_sealant  ':service.price_sealant    
            ,'price_labour   ':service.price_labour     
            ,'price_insurance':service.price_insurance  
            ,'description    ':service.description      
            ,'rating         ':service.rating           
            ,'reviews        ':service.reviews              } )
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
                        'Name':service.name        
                        ,'Service':service.service     
                        ,'Description':service.description     

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
                'Name':service.name    
                ,'Address':service.address 
                ,'Phone':service.phone   
                ,'Timing':service.timing  
                ,'Rating':service.rating  
                ,'Reviews':service.reviews 
                ,'Service':service.service 
                ,'Car':service.car     
                ,'Price':service.price   } )
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
                    'Name':service.name          
                    ,'address':service.address       
                    ,'rating dealer':service.rating_dealer 
                    ,'aspect key':service.aspect_key    
                    ,'Brand':service.brand         
                    ,'Model':service.model         
                    ,'Width':service.width         
                    ,'Aspect Ratio':service.aspect_ratio  
                    ,'Rim Size':service.rim_size      
                    ,'Load Rating':service.load_rating   
                    ,'Speed Rating':service.speed_rating  
                    ,'Warranty':service.warranty      
                    ,'Rating':service.rating        
                    ,'Reviews':service.reviews       
                    ,'Price':service.price                         

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
                    'Name':tyre.name          
                    ,'address':tyre.address       
                    ,'rating dealer':tyre.rating_dealer 
                    ,'aspect key':tyre.aspect_key    
                    ,'Brand':tyre.brand         
                    ,'Model':tyre.model         
                    ,'Width':tyre.width         
                    ,'Aspect Ratio':tyre.aspect_ratio  
                    ,'Rim Size':tyre.rim_size      
                    ,'Load Rating':tyre.load_rating   
                    ,'Speed Rating':tyre.speed_rating  
                    ,'Warranty':tyre.warranty      
                    ,'Rating':tyre.rating        
                    ,'Reviews':tyre.reviews       
                    ,'Price':tyre.price                         
                 } )
                  
    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"

    return HttpResponse(json.dumps(obj), content_type='application/json')

def addItemToCart(request):
    obj = {}
    aspect = None
    obj['status'] = False
    obj['result'] =[]

    obj['counter'] = 1
    obj['status'] = True
    obj['msg'] = "Success"

    return HttpResponse(json.dumps(obj), content_type='application/json')


def getCarObjFromName(carNameArray):
    res = []
    for carCompoundName in carNameArray:
         carCompoundName = cleanstring(carCompoundName)
         make = carCompoundName.split(' ')[0]
         name_model = ''
         if make not in carMakers:
             make = ''
             name_model = carCompoundName
         else:
             name_model = carCompoundName.split(' ', 1)[1]

         # print name_model
         findCar = Car.objects.filter(name=name_model, make=make)
         if len(findCar):
            carObj = findCar[0]
            result = {'name':carObj.name, 'make':carObj.make, 'aspect_ratio':carObj.aspect_ratio, 'size':carObj.size,'id':carObj.id}
            res.append(result)

    return res

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

    return HttpResponse(json.dumps(obj), content_type='application/json')


#run this just once if possible

carTrieObj = trie(carsTrie)