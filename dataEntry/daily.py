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



def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    return query

today = datetime.date.today()
day_today = float(today.day)

campaigns = Campaign.objects.filter(clickgarage_flag=True,auto_flag = True)
for campaign in campaigns:
    sms = campaign.sms_draft
    customers = CGUserNew.objects.filter(clickgarage_flag=True,subscribed=True)
    target = campaign.target
    sms_count = float(campaign.sms_sent)
    email_count = float(campaign.email_sent)
    for customer in customers:
        if campaign.type == "Number of Bookings":
            if float(customer.num_bookings) > float(campaign.target):
                sms2 = sms.replace("$name$",customer.first_name)
                if (day_today % float(campaign.frequency)) == 0:
                    try:
                        mviews.send_sms_msg91(customer.contact_no,sms2)
                        sms_count = sms_count + 1
                    except:
                        None

        if campaign.type == "Last Booking Date":
            date_gap = customer.last_booking_date - datetime.date.today()
            if (customer.last_booking_date - datetime.date.today()) >= float(campaign.target):
                sms2 = sms.replace("$name$",customer.first_name)
                if (day_today % float(campaign.frequency)) == 0:
                    try:
                        mviews.send_sms_msg91(customer.contact_no,sms2)
                        sms_count = sms_count + 1
                    except:
                        None

        if campaign.type == "Total Billing":
            if float(customer.total_amount) > float(campaign.target):
                sms2 = sms.replace("$name$",customer.first_name)
                if (day_today % float(campaign.frequency)) == 0:
                    try:
                        mviews.send_sms_msg91(customer.contact_no,sms2)
                        sms_count = sms_count + 1
                    except:
                        None

        if campaign.type == "Birthday":
            if customer.birth_date == today:
                sms2 = sms.replace("$name$",customer.first_name)
                try:
                    mviews.send_sms_msg91(customer.contact_no,sms2)
                    sms_count = sms_count + 1
                except:
                    None

        if campaign.type == "Anniversary":
            if customer.anniversary == today:
                sms2 = sms.replace("$name$",customer.first_name)
                try:
                    mviews.send_sms_msg91(customer.contact_no,sms2)
                    sms_count = sms_count + 1
                except:
                    None
    campaign.sms_sent = sms_count
    campaign.save()
