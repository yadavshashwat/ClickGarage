from __future__ import absolute_import
from mailing import views as mViews
from celery import shared_task

@shared_task
def test_function():
	return "yay"

@shared_task
def send_sms(type,to,message):
	mViews.send_sms(type,to,message)
	return True

@shared_task
def send_otp(to,message):
	mViews.send_otp(to,message)
	return True

@shared_task
def send_booking_sms(to_name, to, date, pick_time_start, booking_id):
	mViews.send_booking_sms(to_name, to, date, pick_time_start, booking_id)
	return True

@shared_task
def send_cancel_sms(to_name, to, booking_id):
	mViews.send_cancel_sms(to_name, to, booking_id)
	return True

@shared_task
def send_advisor(to_name, to, advisor_name, advisor_number, experience, booking_id):
	mViews.send_advisor(to_name, to, advisor_name, advisor_number, experience, booking_id)
	return True

@shared_task
def send_driver(to_name,to,driver_name, driver_number, driver_id, time_start, time_end, booking_id):
	mViews.send_driver(to_name,to,driver_name, driver_number, driver_id, time_start, time_end, booking_id)
	return True

@shared_task
def send_servicedrop(to_name,to, service_centre, booking_id):
	mViews.send_servicedrop(to_name,to, service_centre, booking_id)
	return True

@shared_task
def send_price_update(to_name,to,advisor_name,price,booking_id):
	mViews.send_price_update(to_name,to,advisor_name,price,booking_id)
	return True

@shared_task
def send_predrop(to_name,to, amount,booking_id):
	mViews.send_predrop(to_name,to, amount,booking_id)
	return True

@shared_task
def send_postdrop(to_name,to,booking_id):
	mViews.send_postdrop(to_name,to,booking_id)
	return True

@shared_task
def send_booking_email_doorstep(to_address,to_name,time_start,date,booking_id):
	mViews.send_booking_email_doorstep(to_address,to_name,time_start,date,booking_id)
	return True 
