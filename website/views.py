from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.conf import settings

import json
import os

from api import views


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
    if request.user.is_authenticated():
        template = loader.get_template('website/checkout.html')
        context = RequestContext(request, {

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
