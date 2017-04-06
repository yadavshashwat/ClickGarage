from dataEntry import runentry
from api.models import *
import datetime

# Taxes.objects.all().delete()
# runentry.loadTaxes('States_Taxes.csv')
#
# Bills.objects.all().delete()

# for booking in bookings:
#     booking.bill_generation_flag = False
#     booking.bill_id = ""
#     booking.save()

bookings = Bookings.objects.all()
for booking in bookings:
    booking.follow_up_date = booking.date_booking
    booking.follow_up_time = str(datetime.datetime.time(datetime.datetime.now() + datetime.timedelta(hours = 5, minutes = 30)))
    booking.save()


