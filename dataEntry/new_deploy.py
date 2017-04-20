from dataEntry import runentry
from api.models import *
import datetime

# Taxes.objects.all().delete()
# runentry.loadTaxes('States_Taxes.csv')
#
Bills.objects.all().delete()
bookings = Bookings.objects.all()

for booking in bookings:
    booking.bill_generation_flag = False
    booking.bill_id = ""
    booking.save()

bookings = Bookings.objects.all()
for booking in bookings:
    jobs_summary = booking.comments
    total_items = jobs_summary.split(", ")
    items = []
    for item in total_items:
        if (item != "" and item != " "):
            obj = {'Job':item,
                'Price':"0"}
            items.append(obj)
    booking.jobssummary = items
    booking.save()
