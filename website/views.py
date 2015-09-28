from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings

import json
import os
from decimal import Decimal
from api import views
from api.models import ServiceDealerCat, CleaningCategoryServices, Car

# Create your views here.
def index(request):
    # template = loader.get_template(os.path.join(settings.TEMPLATES.DIRS, 'templates/website/index.html'))
    template = loader.get_template('website/index.html')
    cars = views.fetch_all_cars(request).content
    cars = json.loads(cars)
    cars = cars['result']
    context = RequestContext(request, {
        'cars': cars,
    })
    return HttpResponse(template.render(context))

def order(request):
    print 'order'
    print 'd ', request.user
    print 'tru ', request.user.is_authenticated()
    if request.user.is_authenticated():
        template = loader.get_template('website/order.html')
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
        return redirect("/loginPage/")

def checkout(request):
    selectCarID = request.COOKIES.get('clgacarid')
    cartEmpty = False
    if request.user.is_authenticated():
        template = loader.get_template('website/checkout.html')
        varCarObj = Car.objects.filter(id=selectCarID)

        selectCarName = False
        if len(varCarObj):
            varCarObj = varCarObj[0]
            selectCarName = " ".join([varCarObj.make, varCarObj.name])
        cartDict = request.user.uc_cart
        contextDict = {}

        for ts in cartDict:
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

                        contextDict[carCmpName].append(cartDict[ts])

        print contextDict
        if contextDict.has_key(selectCarName):
            context = RequestContext(request, {
                'address': [],
                'cart':contextDict,
                'cart_number':len(contextDict[selectCarName])

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
    if request.user.is_authenticated():
        template = loader.get_template('website/cart.html')
        cartList = []
        cartDict = request.user.uc_cart
        contextDict = {}
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
                    # print total_price
                    cartDict[ts]['service_detail'] = item
                    cartDict[ts]['ts'] = ts
                    if len(carCmpName):
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
        print contextDict
        context = RequestContext(request, {
            'cart' : contextDict
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
