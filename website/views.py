from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from django.middleware.csrf import get_token

from ajaxuploader.views import AjaxFileUploader

import datetime
import math
import json, urllib
import os
import re
from decimal import Decimal
from api import views
from api.models import ServiceDealerCat,ServiceDealerCatNew, CleaningCategoryServices, VASCategoryServices, WindShieldServiceDetails, Car, Coupon
from cgutils import common

repair_map = {
    'diagnostics':{'name':'Diagnostics','detail':"I don't know what is wrong with my car"},
    'dent-paint':{'name':'Denting / Painting','detail':""},
    'custom':{'name':'Custom Repair Request','detail':""}
}

ad_landing_map = {
    'car':{
        'servicing':{
            'title':'ClickGarage Car Servicing - On Demand Car Services',
            'meta_desc':'',
            'meta_keys':''
        },
        'cleaning':{
            'title':'ClickGarage Car Cleaning - On Demand Car Services',
            'meta_desc':'',
            'meta_keys':''
        },
        'repair':{
            'title':'ClickGarage Car Repair - On Demand Car Services',
            'meta_desc':'',
            'meta_keys':''
        }
    },
    'bike':{
        'servicing':{
            'title':'ClickGarage Car Servicing - On Demand Car Services',
            'meta_desc':'',
            'meta_keys':''
        }
    }
}

# Create your views here.
def index_old(request):

    selectedCarName = request.COOKIES.get('clgacarname')
    selectedCarID = request.COOKIES.get('clgacarid')
    carObj = Car.objects.filter(id=selectedCarID)
    source = views.get_param(request, 'source', None)
    path =  request.path
    redir = (source == 'logo')

    specific_land = None
    if path:
        path = re.sub('[//]','',path)
        if path == 'cars' or path == 'bikes':
            specific_land = path

    if (not specific_land) and (not redir) and request.user and request.user.is_authenticated() and len(carObj):
        carObj = carObj[0]
        return redirect("/order")
    else:
        # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
        flag = views.get_param(request, 'logReq',False)

        template = loader.get_template('website/index.html')
        cars = views.fetch_all_cars(request).content
        cars = json.loads(cars)
        cars = cars['result']
        context = RequestContext(request, {
            'cars': cars,
            'loginFlag':flag,
            'specific_land':specific_land
        })
        return HttpResponse(template.render(context))

def ad_landing_cars(request, service):
    if service in ['servicing','cleaning','repair']:
        template = loader.get_template('website/ad_service.html')

        print ad_landing_map['car'][service]
        title = ad_landing_map['car'][service]['title']
        meta_desc = ad_landing_map['car'][service]['meta_desc']
        logoText = 'ClickGarage'
        category_list = []
        dd = {
            'servicing':'Servicing',
            'cleaning':'Car Cleaning',
            'repair': 'Car Repair'
        }
        dds = {
            'servicing':[['general','General Check Up'],['standard','Standard Service'],['comprehensive','Comprehensive Service']],
            'cleaning':[['interior','Interior Cleaning'],['exterior','Exterior Cleaning'],['overall','Overall Package']],
            'carcare': [],
            'repair': []
        }
        service_list = False
        print len(dds[service])
        if dds[service] and len(dds[service]):
            service_list = True
        for opt, label in dd.iteritems():
            if opt == service:
                category_list.append({'label':label, 'value':opt,'active':True})
            else:
                category_list.append({'label':label, 'value':opt,'active':False})

        context = RequestContext(request, {
            'car_bike': 'Car',
            'service':service,
            'title':title,
            'category_list':category_list,
            'service_dict':dds,
            'service_list':service_list,
            'meta_desc':meta_desc,
            'logo_text':logoText
        })
        return HttpResponse(template.render(context))

    template = loader.get_template('website/privacy.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def ad_landing_bikes(request, service):
    if service in ['servicing']:
        template = loader.get_template('website/ad_service.html')

        print ad_landing_map['bike'][service]
        title = ad_landing_map['bike'][service]['title']

        meta_desc = ad_landing_map['bike'][service]['meta_desc']
        logoText = 'ClickGarage'
        category_list = []
        dd = {
            'servicing':'Servicing'
        }
        dds = {
            'servicing':[['general','General Check Up'],['standard','Standard Service']],
        }
        service_list = False
        if dds[service] and len(dds[service]):
            service_list = True
        for opt, label in dd.iteritems():
            if opt == service:
                category_list.append({'label':label, 'value':opt,'active':True})
            else:
                category_list.append({'label':label, 'value':opt,'active':False})

        context = RequestContext(request, {
            'car_bike': 'Bike',
            'service':service,
            'title':title,
            'category_list':category_list,
            'service_dict':dds,
            'service_list':service_list,
            'meta_desc':meta_desc,
            'logo_text':logoText
        })
        return HttpResponse(template.render(context))

    template = loader.get_template('website/privacy.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

# def privacy(request):
#     # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
#     template = loader.get_template('website/privacy.html')
#     context = RequestContext(request, {
#     })
#     return HttpResponse(template.render(context))
#
#
# def cancel(request):
#     # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
#     template = loader.get_template('website/cancel.html')
#     context = RequestContext(request, {
#     })
#     return HttpResponse(template.render(context))
#
#
#
# def contact(request):
#     # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
#     template = loader.get_template('website/contact.html')
#     context = RequestContext(request, {
#     })
#     return HttpResponse(template.render(context))


def history(request):
    print 'history'
    print 'd ', request.user
    print 'tru ', request.user.is_authenticated()
    if request.user.is_authenticated():
        template = loader.get_template('website/history.html')
        car_obj = views.fetch_car(request, False)
        if(car_obj['status']):
            car_obj = car_obj['result']
        else:
            car_obj = False

        cars = views.fetch_all_cars(request).content
        cars = json.loads(cars)
        cars = cars['result']
        context = RequestContext(request, {
            'carSelected': car_obj,
            'cars':cars
        })
        return HttpResponse(template.render(context))

    else:
        return redirect("../?logReq=True")


def adminpanel_old(request):
    template = loader.get_template('website/adminpanel.html')
    coupon_flag = False

    if request.user and request.user.is_authenticated():
        if request.user.email in ['shashwat@clickgarage.in', 'bhuvan@clickgarage.in', 'v.rajeev92@gmail.com']:
            coupon_flag = True
    print coupon_flag
    context = RequestContext(request, {
        'coupon_flag' : coupon_flag
    })
    return HttpResponse(template.render(context))




# def tnc(request):
#     # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
#     template = loader.get_template('website/tnc.html')
#     context = RequestContext(request, {
#     })
#     return HttpResponse(template.render(context))

#def serviceSchedule(request):
#    # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
#    template = loader.get_template('website/service-schedule.html')
#    context = RequestContext(request, {
#    })
#    return HttpResponse(template.render(context))

def mobile(request):
    # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
    template = loader.get_template('website/mobile.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def order(request):
    if 1 or request.user.is_authenticated():
        template = loader.get_template('website/order.html')
        car_obj = views.fetch_car(request, False)
        if(car_obj['status']):
            car_obj = car_obj['result']
        else:
            car_obj = False

        cars = views.fetch_all_cars(request).content
        cars = json.loads(cars)
        cars = cars['result']

        if car_obj and car_obj['car_bike'] == 'Bike':
            template = loader.get_template('website/b_order.html')

        context = RequestContext(request, {
            'carSelected': car_obj,
            'cars':cars
        })
        return HttpResponse(template.render(context))

    else:
        return redirect("../?logReq=True")

def checkout(request):
    selectCarID = request.COOKIES.get('clgacarid')
    cookieCartData = request.COOKIES.get('clgacart')
    ccdAdditional = request.COOKIES.get('clgacartaddi')
    couponData = request.COOKIES.get('clgacoup')
    singleCoupon = None
    if couponData and len(couponData):
        try:
            couponData = json.loads( urllib.unquote(couponData) )

            if 'Singleton' in couponData:
                print couponData['Singleton']
                for code in couponData['Singleton'].iterkeys():
                    print code
                    cpnObjs = Coupon.objects.filter(coupon_code=code).exclude(valid="0")
                    if len(cpnObjs):
                        cpnObjs = cpnObjs[0]
                        singleCoupon = {
                            'coupon_code'       :    cpnObjs.coupon_code
                            ,'message'          :    cpnObjs.message
                            ,'value'            :    cpnObjs.value
                            ,'cap'            :    cpnObjs.cap
                            ,'type'            :    cpnObjs.type
                            ,'vendor'            :    cpnObjs.vendor
                            ,'category'            :    cpnObjs.category
                            ,'price_key'            :    cpnObjs.price_key
                            ,'car_bike'            :    cpnObjs.car_bike
                        }
        except:
            print 'Coupon Error'
            singleCoupon = None
    cartEmpty = False
    if request.user.is_authenticated():
        template = loader.get_template('website/checkout.html')
        carInfo = {}
        varCarObj = Car.objects.filter(id=selectCarID)

        userObj = {}
        userObj['userid'] = request.user.id
        if request.user.first_name and len(request.user.first_name):
            userObj['username'] = request.user.first_name
        else:
            userObj['username'] = request.user.username
        # res['username'] = request.user.first_name
        userObj['contact'] = request.user.contact_no
        userObj['email'] = request.user.email


        selectCarName = False
        if len(varCarObj):
            varCarObj = varCarObj[0]
            selectCarName = " ".join([varCarObj.make, varCarObj.name])
            carInfo['car_bike'] = varCarObj.car_bike
        cartDict = request.user.uc_cart

        contextDict = {}

        emergFlag = False

        if cookieCartData and len(cookieCartData):
            cookieCartArray = cookieCartData.split(',')
            for cookieItem in cookieCartArray:
                cookieA = cookieItem.split('*')
                ts = cookieA[0]
                if ts not in cartDict:
                    dealer = " ".join(cookieA[2].split('#$'))
                    obj = {
                        'dealer'    : dealer,
                        'service'   : cookieA[1],
                        'service_id': cookieA[3],
                    }
                    carObj = Car.objects.filter(id=selectCarID)
                    carObj = carObj[0]
                    obj['car'] = {
                        'make'  :   carObj.make,
                        'model' :   carObj.model,
                        'year'  :   carObj.year,
                        'name'  :   carObj.name,
                        'size'  :   carObj.size,
                        'car_bike':carObj.car_bike
                    }
                    cartDict[ts] = obj

                #do something

            # request.user.uc_cart = cartDict
            # request.user.save()
        if ('emergency' in cartDict) and len(cartDict['emergency'].keys()):
            template = loader.get_template('website/emergency-checkout.html')

            emergFlag = True
            for ts in cartDict['emergency']:
                cartObj = cartDict['emergency'][ts]
                if cartObj.has_key("car"):
                    carCmpName = " ".join([cartObj['car']['make'], cartObj['car']['name']])
                else:
                    carCmpName = ""

                item = {}

                if not selectCarName:
                    selectCarName = carCmpName

                newDict = cartObj
                newDict['ts'] = ts
                newDict['datetime'] = common.localTimeString(int(ts)/1000)
                if not contextDict.has_key(carCmpName):
                    contextDict[carCmpName] = []

                contextDict[carCmpName].append(newDict)

            if contextDict.has_key(selectCarName):
                context = RequestContext(request, {
                    'address': [],
                    'cart':contextDict,
                    'cart_number':len(contextDict[selectCarName]),
                    'car_info':carInfo,
                    'emergFlag':emergFlag
                })
                return HttpResponse(template.render(context))
                # return HttpResponse(json.dumps({
                #     'address': [],
                #     'cart':contextDict,
                #     'cart_number':len(contextDict[selectCarName]),
                #     'car_info':carInfo
                # }), content_type='application/json')

            else:
                return redirect('/loginPage/')

        else:
            for ts in cartDict:
                print ts
                if ts == 'emergency':
                    continue
                print ts

                cartObj = cartDict[ts]
                if cartObj.has_key("car"):
                    carCmpName = " ".join([cartObj['car']['make'], cartObj['car']['name']])
                else:
                    carCmpName = ""

                item = {}
                if not selectCarName:
                    selectCarName = carCmpName

                service_id = cartObj['service_id']
                if (carCmpName == selectCarName.strip()) and len(carCmpName):
                    if not contextDict.has_key(carCmpName):
                        contextDict[carCmpName] = []

                    if cartObj['service'] == 'servicing':
                        serviceDetail = ServiceDealerCat.objects.filter(id=service_id)
                        serviceDetailNew = ServiceDealerCatNew.objects.filter(id=service_id)

                        if len(serviceDetail):
                            serviceDetail = serviceDetail[0]
                            print serviceDetail.price_parts, serviceDetail.price_labour
                            total_price = 0
                            if len(serviceDetail.price_parts):
                                total_price = total_price+ float(serviceDetail.price_parts)
                            # if serviceDe
                            if len(serviceDetail.price_labour):
                                total_price = int(total_price + float(serviceDetail.price_labour)+ 0)
                            item = {
                                'id':serviceDetail.id,
                                'name':serviceDetail.name,
                                'brand':serviceDetail.brand,
                                'car_bike':serviceDetail.car_bike,
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
                                'total_price':total_price
                            }
                            cartDict[ts]['service_detail'] = item
                            cartDict[ts]['ts'] = ts

                        elif len(serviceDetailNew):
                            serviceDetail = serviceDetailNew[0]
                            print serviceDetail.price_parts, serviceDetail.price_labour
                            total_price = 0
                            if len(serviceDetail.price_parts):
                                total_price = total_price+ float(serviceDetail.price_parts)
                            # if (serviceDetail.car_bike =="Bike"):
                            #     total_price = total_price+ float(150)
                            if len(serviceDetail.price_labour):
                                if (serviceDetail.car_bike == "Bike"):
                                    if (serviceDetail.dealer_category == "ClickGarage Doorstep"):
                                        total_price =  int(total_price +  float(serviceDetail.price_labour))
                                    else:
                                        total_price =  int(total_price +  float(serviceDetail.price_labour)+ 150)
                                else:
                                    total_price =  int(total_price + float(serviceDetail.price_labour)+ 0)
                            item = {
                                'id':serviceDetail.id,
                                'name':serviceDetail.name,
                                'brand':serviceDetail.brand,
                                'car_bike':serviceDetail.car_bike,
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
                                'total_price':total_price
                            }
                            # print total_price
                            cartDict[ts]['service_detail'] = item
                            cartDict[ts]['ts'] = ts

                            contextDict[carCmpName].append(cartDict[ts])
                    elif cartObj['service'] == 'cleaning':
                        serviceDetail = CleaningCategoryServices.objects.filter(id=service_id)
                        if len(serviceDetail):
                            serviceDetail = serviceDetail[0]
                            total_price = 0
                            if len(serviceDetail.price_parts):
                                total_price = total_price+ float(serviceDetail.price_parts)
                            if len(serviceDetail.price_labour):
                                total_price = total_price + float(serviceDetail.price_labour)

                            # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                            total_price = int(float(serviceDetail.price_total)*(1-float(serviceDetail.discount)))
                            item = {
                                'id':serviceDetail.id,
                                'category':serviceDetail.category,
                                'car_cat':serviceDetail.car_cat,
                                'service':serviceDetail.service,
                                'vendor':serviceDetail.vendor,
                                'parts_price':serviceDetail.price_parts,
                                'labour_price':serviceDetail.price_labour,
                                'total_price':total_price,
                                # 'total_price':total_price,
                                'description':serviceDetail.description,
                            }
                            # print total_price
                            cartDict[ts]['service_detail'] = item
                            cartDict[ts]['ts'] = ts

                            contextDict[carCmpName].append(cartDict[ts])
                    elif cartObj['service'] == 'vas':
                        serviceDetail = VASCategoryServices.objects.filter(id=service_id)
                        if len(serviceDetail):
                            serviceDetail = serviceDetail[0]
                            total_price = 0
                            # if len(serviceDetail.price_parts):
                            #     total_price = total_price+ float(serviceDetail.price_parts)
                            # if len(serviceDetail.price_labour):
                            #     total_price = total_price + float(serviceDetail.price_labour)

                            try:
                                total_price = float(serviceDetail.price_total)
                            except ValueError:
                                total_price = serviceDetail.price_total
                            item = {
                                'id':serviceDetail.id,
                                'category':serviceDetail.category,
                                'car_cat':serviceDetail.car_cat,
                                'service':serviceDetail.service,
                                'vendor':serviceDetail.vendor,
                                'parts_price':serviceDetail.price_parts,
                                'labour_price':serviceDetail.price_labour,
                                'total_price':total_price,
                                # 'total_price':total_price,
                                'description':serviceDetail.description,
                            }
                            # print total_price
                            cartDict[ts]['service_detail'] = item
                            cartDict[ts]['ts'] = ts

                            contextDict[carCmpName].append(cartDict[ts])

                    elif cartObj['service'] == 'windshield':
                        serviceDetail = WindShieldServiceDetails.objects.filter(id=service_id)
                        if len(serviceDetail):
                            serviceDetail = serviceDetail[0]
                            total_price = 0
                            # if len(serviceDetail.price_parts):
                            #     total_price = total_price+ float(serviceDetail.price_parts)
                            # if len(serviceDetail.price_labour):
                            #     total_price = total_price + float(serviceDetail.price_labour)

                            # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                            # total_price = int(float(serviceDetail.price_total)*(1-float(serviceDetail.discount)))
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
                            }
                            # print total_price
                            cartDict[ts]['service_detail'] = item
                            cartDict[ts]['ts'] = ts

                            contextDict[carCmpName].append(cartDict[ts])
                    elif cartObj['service'] == 'repair':
                        s_id = cartObj['service_id']
                        if len(s_id) and (s_id in repair_map):
                            item = {
                                'category':repair_map[s_id]['name']
                            }
                        else:
                            item = {}

                        cartDict[ts]['service_detail'] = item
                        cartDict[ts]['ts'] = ts
                        contextDict[carCmpName].append(cartDict[ts])

            # print contextDict
            if contextDict.has_key(selectCarName):
                context = RequestContext(request, {
                    'address': [],
                    'cart':contextDict,
                    'cart_number':len(contextDict[selectCarName]),
                    'car_info':carInfo,
                    'emergFlag':emergFlag,
                    'userObj':userObj,
                    'singleCoupon' : singleCoupon
                })
                return HttpResponse(template.render(context))

            else:
                return redirect('/loginPage/')

            # address : request.user.saved_address
    else:
        return redirect('/loginPage/')

def dashboard(request):
    if request.user.is_authenticated():
        template = loader.get_template('himank/checkout.html')

        context = RequestContext(request, {
            cart : request.user.uc_cart,
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('/loginPage/')

def cart(request):
    selectCar = request.COOKIES.get('clgacarid')
    cookieCartData = request.COOKIES.get('clgacart')
    ccdAdditional = request.COOKIES.get('clgacartaddi')
    loginFlag = False
    if request.user.is_authenticated():
        loginFlag = True

    if cookieCartData or loginFlag:
        template = loader.get_template('website/cart.html')
        carList = []
        cartList = []

        cartDict = {}
        if loginFlag:
            cartDict = request.user.uc_cart

        contextDict = {}

        if cookieCartData and len(cookieCartData):
            cookieCartArray = cookieCartData.split(',')
            for cookieItem in cookieCartArray:
                cookieA = cookieItem.split('*')
                ts = cookieA[0]
                if ts not in cartDict:
                    dealer = " ".join(cookieA[2].split('#$'))
                    obj = {
                        'dealer'    : dealer,
                        'service'   : cookieA[1],
                        'service_id': cookieA[3],
                    }
                    carObj = Car.objects.filter(id=selectCar)
                    carObj = carObj[0]
                    obj['car'] = {
                        'make'  :   carObj.make,
                        'model' :   carObj.model,
                        'year'  :   carObj.year,
                        'name'  :   carObj.name,
                        'size'  :   carObj.size,
                        'car_bike'  :   carObj.car_bike
                    }
                    cartDict[ts] = obj
            if loginFlag:
                request.user.uc_cart = cartDict
                request.user.save()
        if ccdAdditional and len(ccdAdditional):
            try:
                ccdaObj = json.loads( urllib.unquote(ccdAdditional) )
                # for ts in ccdaObj:
                    # if ts in cartDict:
                    #     obj = cartDict[ccdaObj]
                for ts in ccdaObj:
                    print ts
                    print (ts in cartDict)
                    # print ('additional_data' not in cartDict[ts])
                    if (ts in cartDict) and ('additional_data' not in cartDict[ts]):
                        cartDict[ts]['additional_data'] = ccdaObj[ts]
            except ValueError:
                print 'error'
            if loginFlag:
                request.user.uc_cart = cartDict
                request.user.save()
        for ts in cartDict:
            if ts == 'emergency':
                contextDict['emergency'] = []
                for ts2 in cartDict['emergency']:
                    emergObj = cartDict['emergency'][ts2]
                    emergObj['ts'] = ts2
                    emergObj['datetime'] = common.localTimeString(int(ts2)/1000)
                    contextDict['emergency'].append(emergObj)
                continue

            cartObj = cartDict[ts]
            if cartObj.has_key("car"):
                carCmpName = " ".join([cartObj['car']['make'], cartObj['car']['name']])
                if not contextDict.has_key(carCmpName):
                    contextDict[carCmpName] = []
            else:
                carCmpName = ""
            item = {}
            service_id = cartObj['service_id']
            if cartObj['service'] == 'servicing':
                serviceDetail = ServiceDealerCat.objects.filter(id=service_id)
                serviceDetailNew = ServiceDealerCatNew.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    print serviceDetail.price_parts, serviceDetail.price_labour
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price =  int(total_price  + float(serviceDetail.price_labour)+ 0)
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        # 'car_bike':serviceDetail.car_bike,
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
                        'total_price':total_price
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
                elif len(serviceDetailNew):
                    serviceDetail = serviceDetailNew[0]
                    print serviceDetail.price_parts, serviceDetail.price_labour
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        if (serviceDetail.car_bike == "Bike"):
                            if(serviceDetail.dealer_category == "ClickGarage Doorstep"):
                                total_price =  int(total_price  + float(serviceDetail.price_labour))
                            else:
                                total_price =  int(total_price + float(serviceDetail.price_labour)+ 150)
                        else:
                            total_price =  int(total_price + float(serviceDetail.price_labour)+ 0)
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        'car_bike':serviceDetail.car_bike,
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

                        'total_price':total_price
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)

            elif cartObj['service'] == 'cleaning':
                serviceDetail = CleaningCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    total_price = float(serviceDetail.price_total)
                    disc = 0
                    if (serviceDetail.discount) and len(serviceDetail.discount):
                        try:
                            disc = float(serviceDetail.discount)
                        except ValueError: 
                            disc = 0
                    total_price = int(total_price*(1-disc))
                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    item = {
                        'id':serviceDetail.id,
                        'category':serviceDetail.category,
                        'car_cat':serviceDetail.car_cat,
                        'service':serviceDetail.service,
                        'vendor':serviceDetail.vendor,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'total_price':total_price,
                        # 'total_price':total_price,
                        'description':serviceDetail.description,
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)

            elif cartObj['service'] == 'vas':
                serviceDetail = VASCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price + float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    try:
                        total_price = float(serviceDetail.price_total)
                    except ValueError:
                        total_price = serviceDetail.price_total

                    # disc = 0
                    # if (serviceDetail.discount) and len(serviceDetail.discount):
                    #     try:
                    #         disc = float(serviceDetail.discount)
                    #     except ValueError:
                    #         disc = 0
                    # total_price = int(total_price*(1-disc))
                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
                    item = {
                        'id':serviceDetail.id,
                        'category':serviceDetail.category,
                        'car_cat':serviceDetail.car_cat,
                        'service':serviceDetail.service,
                        'vendor':serviceDetail.vendor,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'total_price':total_price,
                        # 'total_price':total_price,
                        'description':serviceDetail.description,
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
            elif cartObj['service'] == 'windshield':
                serviceDetail = WindShieldServiceDetails.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    # if len(serviceDetail.price_parts):
                    #     total_price = total_price+ float(serviceDetail.price_parts)
                    # if len(serviceDetail.price_labour):
                    #     total_price = total_price + float(serviceDetail.price_labour)
                    try:
                        total_price = float(serviceDetail.price_total)
                    except ValueError:
                        total_price = serviceDetail.price_total
                    disc = 0
                    # if (serviceDetail.discount) and len(serviceDetail.discount):
                    #     try:
                    #         disc = float(serviceDetail.discount)
                    #     except ValueError:
                    #         disc = 0

                    # total_price = total_price
                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
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
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
            elif cartObj['service'] == 'repair':
                s_id = cartObj['service_id']
                if len(s_id) and (s_id in repair_map):
                    item = {
                        'category':repair_map[s_id]['name']
                    }
                else:
                    item = {}

                cartDict[ts]['service_detail'] = item
                cartDict[ts]['ts'] = ts
                if len(carCmpName):
                    contextDict[carCmpName].append(cartDict[ts])
                    if carCmpName not in carList:
                        carList.append(carCmpName)

        # print contextDict
        if len(carList):
            carList = views.getCarObjFromName(carList)
        context = RequestContext(request, {
            'cart' : contextDict,
            'carList':carList,
            'login_flag':loginFlag
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('/loginPage/')

def defResponse(request):

    return HttpResponse('Go Away')

def loginPage(request):
    c = {}
    c.update(csrf(request))
    # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
    template = loader.get_template('website/login.html')
    context = RequestContext(request, {
    })
    # return render_to_response('website/login.html', c)
    return HttpResponse(template.render(context))



def bookings(request):
    selectCar = request.COOKIES.get('clgacarid')
    cookieCartData = request.COOKIES.get('clgacart')
    if request.user.is_authenticated():
        template = loader.get_template('website/cart.html')
        carList = []
        cartList = []
        cartDict = request.user.uc_cart
        contextDict = {}

        if cookieCartData and len(cookieCartData):
            cookieCartArray = cookieCartData.split(',')
            for cookieItem in cookieCartArray:
                cookieA = cookieItem.split('*')
                ts = cookieA[0]
                if ts not in cartDict:
                    dealer = " ".join(cookieA[2].split('#$'))
                    obj = {
                        'dealer'    : dealer,
                        'service'   : cookieA[1],
                        'service_id': cookieA[3],
                    }
                    carObj = Car.objects.filter(id=selectCar)
                    carObj = carObj[0]
                    obj['car'] = {
                        'make'  :   carObj.make,
                        'model' :   carObj.model,
                        'year'  :   carObj.year,
                        'name'  :   carObj.name,
                        'size'  :   carObj.size,
                        'car_bike'  :   carObj.car_bike,
                    }
                    cartDict[ts] = obj

            # request.user.uc_cart = cartDict
            # request.user.save()
        for ts in cartDict:
            cartObj = cartDict[ts]
            if cartObj.has_key("car"):
                carCmpName = " ".join([cartObj['car']['make'], cartObj['car']['name']])
                if not contextDict.has_key(carCmpName):
                    contextDict[carCmpName] = []
            else:
                carCmpName = ""
            item = {}
            service_id = cartObj['service_id']
            if cartObj['service'] == 'servicing':
                serviceDetail = ServiceDealerCat.objects.filter(id=service_id)
                serviceDetailNew = ServiceDealerCatNew.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    print serviceDetail.price_parts, serviceDetail.price_labour
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)
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
                        'total_price':total_price
                    }
                elif len(serviceDetailNew):
                    serviceDetail = serviceDetailNew[0]
                    print serviceDetail.price_parts, serviceDetail.price_labour
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)
                    item = {
                        'id':serviceDetail.id,
                        'name':serviceDetail.name,
                        'brand':serviceDetail.brand,
                        'car':serviceDetail.carname,
                        'odometer':serviceDetail.type_service,
                        'dealer_cat':serviceDetail.dealer_category,
                        'parts_list':serviceDetail.part_replacement,
                        'parts_price':serviceDetail.price_parts,
                        'labour_price':serviceDetail.price_labour,
                        'wa_price':serviceDetail.wheel_alignment,
                        'wb_price':serviceDetail.wheel_balancing,
                        'wa_wb_present':serviceDetail.WA_WB_Inc,
                        'dealer_details':serviceDetail.detail_dealers,
                        # 'year':serviceDetail.year,
                        'total_price':total_price
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
            elif cartObj['service'] == 'cleaning':
                serviceDetail = CleaningCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
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
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
            elif cartObj['service'] == 'vas':
                serviceDetail = VASCategoryServices.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    if len(serviceDetail.price_parts):
                        total_price = total_price+ float(serviceDetail.price_parts)
                    if len(serviceDetail.price_labour):
                        total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
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
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
            elif cartObj['service'] == 'windshield':
                serviceDetail = WindShieldServiceDetails.objects.filter(id=service_id)
                if len(serviceDetail):
                    serviceDetail = serviceDetail[0]
                    total_price = 0
                    # if len(serviceDetail.price_parts):
                    #     total_price = total_price+ float(serviceDetail.price_parts)
                    # if len(serviceDetail.price_labour):
                    #     total_price = total_price + float(serviceDetail.price_labour)

                    # total_price = float(serviceDetail.price_parts) + float(serviceDetail.price_labour)
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
                                ,'price_insu,rance':serviceDetail.price_insurance
                                ,'price_total'   :serviceDetail.price_total
                                ,'city'           :serviceDetail.city
                                ,'description':serviceDetail.description
                    }
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
                        contextDict[carCmpName].append(cartDict[ts])
                        if carCmpName not in carList:
                            carList.append(carCmpName)
        # print contextDict
        if len(carList):
            carList = views.getCarObjFromName(carList)
        context = RequestContext(request, {
            'cart' : contextDict,
            'carList':carList
        })
        return HttpResponse(template.render(context))
    else:
        return redirect('/loginPage/')

def orderParse(request, carName, city):
    obj = {}
    obj['car'] = carName
    obj['city'] = city
    service = views.get_param(request,'cat','servicing')
    template = loader.get_template('website/order.html')
    car_obj = False
    if not (city and (city in ["Delhi", "Gurgaon", "Noida"]) ):
        city = False

    title = ''
    meta_desc = ''
    if carName:
        carName = " ".join(carName.split('-'))
        car_obj = views.getCarObjFromName([carName])
        if len(car_obj):
            car_obj = car_obj[0]
            carCleanName = carName.replace('Diesel',' ').replace('Petrol',' ').strip()
            title = carCleanName + ' Servicing, Repair & Cleaning @ ClickGarage'
            meta_desc = 'Solution to all your '+carCleanName+' maintenance needs.' \
                                  ' Compare prices, choose from a network of authorized and multibrand service centers, ' \
                                  'book doorstep services, get expert advice and save money. All within a few clicks.'
        else:
            car_obj = False
    else:
        car_obj = views.fetch_car(request, False)
        if(car_obj['status']):
            car_obj = car_obj['result']
        else:
            car_obj = False
    print car_obj
    if car_obj and (car_obj['car_bike'] == 'Bike'):
        template = loader.get_template('website/b_order.html')


    descript_dict = {
        'servicing':'',
        'cleaning' :'',
        'repair'   :'',
        'emergency':'',
        'windshield':'',
        'car_care':''

    }
    cars = views.fetch_all_cars(request).content
    cars = json.loads(cars)
    cars = cars['result']
    context = RequestContext(request, {
        'carSelected': car_obj,
        'cars':cars,
        'city':city,
        'title':title,
        'meta_desc':meta_desc,
        'service':service,
        'descript_dict':descript_dict
    })
    return HttpResponse(template.render(context))

def orderParseNew(request, carName, city):
    obj = {}
    obj['car'] = carName
    obj['city'] = city
    service = views.get_param(request,'cat','servicing')
    template = loader.get_template('website/order.html')
    car_obj = False
    if not (city and (city in ["Delhi", "Gurgaon", "Noida"]) ):
        city = False

    title = ''
    meta_desc = ''
    if carName:
        carName = " ".join(carName.split('-'))
        car_obj = views.getCarObjFromName([carName])
        if len(car_obj):
            car_obj = car_obj[0]
            carCleanName = carName.replace('Diesel',' ').replace('Petrol',' ').strip()
            title = carCleanName + ' Servicing, Repair & Cleaning @ ClickGarage'
            meta_desc = 'Solution to all your '+carCleanName+' maintenance needs.' \
                                  ' Compare prices, choose from a network of authorized and multibrand service centers, ' \
                                  'book doorstep services, get expert advice and save money. All within a few clicks.'
        else:
            car_obj = False
    else:
        car_obj = views.fetch_car(request, False)
        if(car_obj['status']):
            car_obj = car_obj['result']
        else:
            car_obj = False
    print car_obj
    if car_obj and (car_obj['car_bike'] == 'Bike'):
        template = loader.get_template('website/b_order_new.html')


    descript_dict = {
        'servicing':'',
        'cleaning' :'',
        'repair'   :'',
        'emergency':'',
        'windshield':'',
        'car_care':''

    }
    cars = views.fetch_all_cars(request).content
    cars = json.loads(cars)
    cars = cars['result']
    context = RequestContext(request, {
        'carSelected': car_obj,
        'cars':cars,
        'city':city,
        'title':title,
        'meta_desc':meta_desc,
        'service':service,
        'descript_dict':descript_dict
    })
    return HttpResponse(template.render(context))




def serviceSchedule(request, carName):
    obj = {}
    obj['car'] = carName
    template = loader.get_template('website/service-schedule.html')
    car_obj = False
    title = ''
    if carName:
        carName = " ".join(carName.split('-'))
        car_obj = views.getCarObjFromName([carName])
        if len(car_obj):
            car_obj = car_obj[0]
            title = carName + ' Service Schedule - ClickGarage'
        else:
            car_obj = False
    else:
        car_obj = views.fetch_car(request, False)
        if(car_obj['status']):
            car_obj = car_obj['result']
        else:
            car_obj = False
    cars = views.fetch_all_cars(request).content
    cars = json.loads(cars)
    cars = cars['result']
    context = RequestContext(request, {
        'carSelected': car_obj,
        'cars':cars,
        'title':title
    })
    return HttpResponse(template.render(context))


def upload_test(request):
    csrf_token = get_token(request)
    template = loader.get_template('website/upload_test.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def drivers(request):
    # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
    template = loader.get_template('website/drivers.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def start(request):
    csrf_token = get_token(request)
    return render_to_response('import.html',
        {'csrf_token': csrf_token}, context_instance = RequestContext(request))

import_uploader = AjaxFileUploader()


# <----- revamp code ------>


def advert(request,service='',veh_type='',source=''):
    template = loader.get_template('revamp/advert.html')
    context = RequestContext(request ,locals())
    return HttpResponse(template.render(context))

def index(request):
    template = loader.get_template('revamp/index.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def get_quote(request,veh_type='',veh='',service=''):
    template = loader.get_template('revamp/order.html')
    display_name = veh.replace('-',' ').replace('_',' ')
    context = RequestContext(request,locals())
    return HttpResponse(template.render(context))


def adminpanel(request):
    template = loader.get_template('revamp/admin.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

# def adminpanel(request):
#     template = loader.get_template('revamp/admin.html')
#     context = RequestContext(request, {
#     })
#     return HttpResponse(template.render(context))

def billing(request,bill_type=''):
    template = loader.get_template('revamp/bills.html')
    context = RequestContext(request ,locals())
    return HttpResponse(template.render(context))



def rsa(request,veh_type=''):
    template = loader.get_template('revamp/rsa.html')
    context = RequestContext(request, locals())
    return HttpResponse(template.render(context))




def howitworks(request):
    template = loader.get_template('revamp/howitworks.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def faq(request):
    template = loader.get_template('revamp/faq.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def whyclickgarage(request):
    template = loader.get_template('revamp/whyclickgarage.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def howitworks(request):
    template = loader.get_template('revamp/howitworks.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def aboutclickgarage(request):
    template = loader.get_template('revamp/aboutclickgarage.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def press(request):
    template = loader.get_template('revamp/press.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def careers(request):
    template = loader.get_template('revamp/careers.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def cities(request):
    template = loader.get_template('revamp/cities.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def brands(request):
    template = loader.get_template('revamp/brands.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def blog(request):
    template = loader.get_template('revamp/blog.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def partners(request):
    template = loader.get_template('revamp/partners.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def serviceschedule(request):
    template = loader.get_template('revamp/serviceschedule.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def servicewarranty(request):
    template = loader.get_template('revamp/servicewarranty.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def privacy(request):
    template = loader.get_template('revamp/privacy.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))
def tnc(request):
    template = loader.get_template('revamp/tnc.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def cancel(request):
    template = loader.get_template('revamp/cancel.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def signuppartner(request):
    template = loader.get_template('revamp/signuppartner.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def fleetservicing(request):
    template = loader.get_template('revamp/fleetservicing.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def sitemap(request):
    template = loader.get_template('revamp/sitemap.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def services(request,service=''):
    template = loader.get_template('revamp/services.html')
    context = RequestContext(request ,locals())
    return HttpResponse(template.render(context))


def contactus(request):
    template = loader.get_template('revamp/contactus.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))