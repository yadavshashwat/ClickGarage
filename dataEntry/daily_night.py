production = 1

# from clickgarage import settings
# from django.core.management import setup_environ
# setup_environ(settings)

from clickgarage import settings
from django.core.management import setup_environ
setup_environ(settings)

# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "../clickgarage.settings")

# your imports, e.g. Django models
# from your_project_name.models import Location



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
from api.models import *
# from dataEntry.runentry import carMakers, cleanstring
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

def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

num_bookings = 0
num_leads = 0
total_amount = 0
# def calculate_customer_data():
bookings = Bookings.objects.filter(clickgarage_flag=True,booking_flag=True,job_completion_flag=True)
i = 0
for booking in bookings:
    list = []
    # print i
    cust_number = booking.cust_number
    cust_name = booking.cust_name
    users = CGUserNew.objects.filter(id=booking.cust_id)
    if len(users):
        user = users[0]
    else:
        user = create_check_user_modified(cust_name,cust_number,"ClickGarage")
    list = user.booking_id_list
    if booking.id not in list:
        list.append(booking.id)
        user.last_booking_date = booking.date_booking
        user.num_bookings = str(float(user.num_bookings) + 1)
        user.total_amount = str(float(user.total_amount) + float(booking.price_total))

    # print list
    user.booking_id_list = list
    user.save()
    # i = i +1

campaigns = Campaign.objects.filter(clickgarage_flag=True)
for campaign in campaigns:
    num_bookings = 0
    num_leads = 0
    total_amount = 0
    bookings = Bookings.objects.filter(clickgarage_flag=True,booking_flag=True,job_completion_flag=True,source = campaign.campaign_name)
    for booking in bookings:
        num_bookings = num_bookings + 1
        total_amount = total_amount + float(booking.price_total)
        print num_bookings

    leads = Bookings.objects.filter(clickgarage_flag=True,source = campaign.campaign_name)
    for lead in leads:
        num_leads = num_leads + 1
    campaign.num_bookings = num_bookings
    campaign.num_leads = num_leads
    campaign.total_amount = total_amount
    campaign.save()


