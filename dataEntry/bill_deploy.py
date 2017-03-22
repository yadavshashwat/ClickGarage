from dataEntry import runentry
from api.models import *

Taxes.objects.all().delete()
runentry.loadTaxes('States_Taxes.csv')

Bills.objects.all().delete()
bookings = Bookings.objects.all()

for booking in bookings:
    booking.bill_generation_flag = False
    booking.bill_id = ""
    booking.save()


