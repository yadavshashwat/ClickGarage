from api.models import *
from activity.models import *
from django.http import HttpResponse
import api.tasks as tasks

secret_string = "dmFydW5ndWxhdGlsaWtlc2dhbG91dGlrZWJhYg=="


def test_func():
    return tasks.test_function()

def signUpDriver(request):
    if (request.method == 'POST') :
        b_unicode   = request.body.decode('utf-8')
        body        = json.loads(b_unicode)
        mobile      = body.get('mobile')
        name        = body.get('name')
        
        if (body.get('secret') and body.get('secret')=='anaconda') :
            driver, exists = Driver.objects.get_or_create(mobile=mobile, name=name)

            if exists :
                result = dict(status=True, message='User exists')

            else :
                driver.save()
                result = dict(status=True, mobile=mobile, rID=rID)

            return HttpResponse(result, content_type='application/json')

def fetchAllBookings(request):
    if (request.method == 'GET') :
        params = request.GET

        if (params.get('rID')) :
            all_bookings = list()
            #TODO show booking details
            return HttpResponse(all_bookings, content_type='application/json')

def updateBookingStatus(request):
    if (request.method == 'POST') :
        b_unicode   = request.body.decode('utf-8')
        body        = json.loads(b_unicode)

        if (request.POST.get('rID')) :
            mobile  = body.get('mobile')
            name    = body.get('name')
            status  = body.get('status')
            lat     = body.get('lat')
            lon     = body.get('lon')
            booking_id = body.get('booking_id')

            booking_object = DriverBookings(driver__name=name, 
                                            driver__mobile=mobile, 
                                            booking__booking_id=booking_id,
                                            status__status=status,
                                            lat=lat,
                                            lon=lon)
            booking_object.save()



            # todo send_messages(status, params)
            result = dict(status=True, message='updated')
            return HttpResponse(result, content_type='application/json')

def getDriverBookings(request):
    if (request.method == 'GET') :
        params = request.GET
        if (params.get('rID')) :
            mobile  = params.get('mobile')
            name    = params.get('name')

            bookings = DriverBookings.objects.filter(driver__name=name, driver__mobile=mobile, status__status='accepted')

            result = list()

            for booking in bookings : 
                booking_dict = dict()
                booking_details = booking.booking
                booking_dict['id'] = booking_details.booking_id 
                booking_dict['cust_id'] = booking_details.cust_id
                booking_dict['make'] = booking_details.cust_brand
                booking_dict['model'] = booking_details.cust_carname
                # booking_dict['service_selected']
                # booking_dict['additional_details']
                booking_dict['pick_up_time'] = booking_details.time_booking
                booking_dict['pick_up_date'] = booking_details.date_booking
                booking_dict['cust_number'] = booking_details.cust_number
                # booking_dict['car_bike']
                # booking_dict['vendor'] =
                # TODO fill necessary details

                result.append(booking_dict)

            return HttpResponse(result, content_type='application/json')

# def send_message(status, params)
def send_message(status,car_bike,cust_number,cust_name,driver_mechanic_name,driver_mechanic_number, driver_mechanic_link, due_amount, payment):
    sms_type = "TRANS"
    if (car_bike == "bike"):
        if (status="accepted"):
            # message = "Hi " + cust_name +
            message = "Hi " + cust_name + " our team ("+driver_mechanic_name +" : "+driver_mechanic_number +" | " + driver_mechanic_link +") is out for your bike servicing. They will reach your location at around " + time + ". They will need a water source for washing your bike."
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

        if (status=="complete"):
            message = "Hi " + cust_name + "  is out for your bike servicing. They will reach your location at around " + time + ". They will need a water source for washing your bike."
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

    if (car_bike == "car"):
        if (status="accepted"):
            # message = "Hi " + cust_name +
            message = "Hi " + cust_name + " our driver ("+driver_mechanic_name +" : "+driver_mechanic_number +" | " + driver_mechanic_link +") is out to pick your vehicle. He will reach your location at around " + time + ". Kindly keep your vehicle documents ready."
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

        if (status=="checked-in"):
            message = "Hi " + cust_name + " your car was successfully checked in at the service centre. Our service advisor will give you a call post vehicle inspection."
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

        if (status=="work-complete"):
            message = "Hi " + cust_name + " our driver is out to deliver your vehicle. He will need the due payment of Rs."+ due_amount +" and receiving form for handing over the vehicle. You can pay the amount online at http://imojo.in/wukje"
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

        if (status=="paid-feedback"):
            message = "Hi " + cust_name + " Thanks for using ClickGarage! We have recieved your payment of Rs."+ payment +". It was a pleasure serving you. Can you please write a testimonial for us? Your kind words keep us motivated. :) Link - http://bit.ly/1QGgSXc"
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

        if (status=="unpaid-feedback"):
            message = "Hi " + cust_name + " Thanks for using ClickGarage! It was a pleasure serving you. Can you please write a testimonial for us? Your kind words keep us motivated. :) Link - http://bit.ly/1QGgSXc"
            message = message.replace(" ","+")
            tasks.send_sms(sms_type,cust_number,message)

