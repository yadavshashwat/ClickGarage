from dataEntry import runentry
from api.models import *
from activity.models import Transactions, CGUser, CGUserNew
import re
from api.views import *
import datetime
def cleanstring(query):
    query = query.strip()
    query = re.sub('\s{2,}', ' ', query)
    query = re.sub(r'^"|"$', '', query)
    query = query.title()
    return query


transactions = Bookings.objects.filter(clickgarage_flag=True)
for trans in transactions:
    name = trans.cust_name
    number = trans.cust_number
    user = create_check_user(name, number)
    total_price = 0
    total_part = 0
    total_labour = 0
    total_discount = 0

    for item in trans.service_items:
        if item['type'] == "Part" or item['type'] == "Part28":
            total_price = total_price + float(item['price'])
            total_part = total_part + float(item['price'])

        elif item['type'] == "Part18":
            total_price = total_price + float(item['price'])
            total_part = total_part + float(item['price'])

        elif item['type'] == "Consumable":
            total_price = total_price + float(item['price'])
            total_part = total_part + float(item['price'])

        elif item['type'] == "Lube" or item['type'] == "Lube18":
            total_price = total_price + float(item['price'])
            total_part = total_part + float(item['price'])

        elif item['type'] == "Lube28":
            total_price = total_price + float(item['price'])
            total_part = total_part + float(item['price'])

        elif item['type'] == "Labour":
            total_price = total_price + float(item['price'])
            total_labour = total_labour + float(item['price'])
        elif item['type'] == "Discount":
            total_price = total_price - float(item['price'])
            total_discount = total_discount + float(item['price'])

    trans.price_total = total_price
    trans.price_labour = total_labour
    trans.price_discount = total_discount
    trans.price_total = total_price
    trans.save()


