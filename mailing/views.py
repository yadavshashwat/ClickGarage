# Create your views here
import requests
import smtplib
import urllib2
from datetime import datetime

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders
import sendgrid
from sendgrid.helpers.mail import *

helpline_number = "7045996415"
escalation_number = "9953083005"


key = "ab33f626-fba5-4bff-9a2b-68a7e9eed43c"
# ab33f626-fba5-4bff-9a2b-68a7e9eed43c
sendername = "CARCRW"
staffmails = ["shashwat@clickgarage.in", "bhuvan@clickgarage.in","bookings@clickgarage.in", "rajiv@clickgarage.in","amit.kumar@clickgarage.in","jitendra@clickgarage.in"]
booking_mail = ["bookings@clickgarage.in"]

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = 'email-smtp.us-west-2.amazonaws.com'
smtp_username = 'AKIAJ4U5VOXPWBT37X4A'
smtp_password = 'AkJxDBO/FOsxkF1Ucd1EhblV5DTAVLpFfqWQv/KI2gn7'
from_address = "Carcrew <bookings@clickgarage.in>"
helpline_number = "7045996415"

import boto
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto.ses
from api.models import *
from activity.models import Transactions, CGUser, CGUserNew
import string


def send_sms(type,to,message):
	url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message="+ message + "&sendername=" + sendername+ "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)


def send_trans_sms(to, message):
	url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message=" + message + "&sendername=" + sendername + "&smstype=TRANS&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)


def send_booking_sms(to_name, to, date, pick_time_start, booking_id):
	message = "Hi "+ to_name +"! Your Carcrew appointment has been confirmed. Appointment date: " +date + ", Time: "  + pick_time_start  + ". For further assistance, please contact us on " + helpline_number + " and quote your booking ID: " + booking_id + "."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_cancel_sms(to_name, to, booking_id):
	message = "Hi "+ to_name +"! Your Carcrew appointment for booking id :#"+booking_id+"has been cancelled."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)


def send_advisor(to_name, to, advisor_name, advisor_number, experience, booking_id):
	message = to_name + ", we have assigned our auto expert Mr. "+ advisor_name + " (Mob: "+ advisor_number +") for your car. He has an experience of over " + experience + " years. He will make sure you get maximum value for your money. Booking ID: " + booking_id
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_driver(to_name,to,driver_name, driver_number, driver_id, time_start, time_end, booking_id):
	message = "Hi "+to_name+", our driver "+ driver_name+" is out to pick your car . He will reach your location between "+ time_start + "-" + time_end +". You can contact him on " + driver_number + ". Booking ID: " + booking_id + "."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_servicedrop(to_name,to, service_centre, booking_id):
	message = to_name+ ", your car has been safely checked in at " +service_centre+ " service center at " + datetime.now().time().strftime('%I:%M %p') + " on "+ datetime.now().date().strftime('%d-%b-%Y') + ". Booking ID - " + booking_id + "."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_price_update(to_name,to,advisor_name,price,booking_id):
	message = to_name + " as informed to you by our auto expert Mr. " + advisor_name + " , the total bill amount for your booking- " + booking_id + " is Rs. " + price + ". You can pay the bill amount through payment gateway on our app/website or by cash/card to the driver at the time of delivery."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_predrop(to_name,to, amount,booking_id):
	message = "Hey "+to_name+", your requested job for the car is complete. Our driver is out to deliver your car and will reach in next 1-2 hrs. Please ensure someone is there to receive the vehicle with the recieving form and the differential amount of Rs."+ amount+". Booking ID - " + booking_id + "."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_postdrop(to_name,to,booking_id):
	message = "Hi "+to_name+", Thank you for using Carcrew. Kindly share your valuable feedback by replying to the email which you'll receive shortly."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def prompt(prompt):
	return raw_input(prompt).strip()


def send_parts_inquiry(make, model, pd, name, phone):
	print "Sedning email for parts inquiry"
	sg = sendgrid.SendGridAPIClient("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")
	data = "Parts Inquiry \n Make: {0} \n Model: {1} \n Part: {2} \n Name: {3} \n Phone: {4}".format(make, model, pd, name, phone)
	from_email = Email("parts@carcrew.in")
	to_email = Email("mrunal.saxena@carcrew.in")
	subject = "Parts Inquiry"
	content = Content("text/plain", data)
	mail = Mail(from_email, subject, to_email, content)
	#mail.set_from(Email("test@example.com", "Example User"))
	# mail.set_subject("Hello World from the SendGrid Python Library")
    #
	# personalization = Personalization()
	# personalization.add_to(Email("test1@example.com", "Example User"))
	# personalization.add_to(Email("test2@example.com", "Example User"))
	# mail.add_personalization(personalization)
    #
	# mail.add_content(Content("text/plain", "some text here"))
	# mail.add_content(Content("text/html", "<html><body>some text here</body></html>"))

	response = sg.client.mail.send.post(request_body=mail.get())
	print(response.status_code)
	print(response.body)
	print(response.headers)

def send_booking_email_doorstep(to_address,to_name,time_start,date,booking_id):
	me = from_address
	you = to_address

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Confirmation! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
	<head>
		<!-- NAME: 1:3 COLUMN - BANDED -->
		<!--[if gte mso 15]>
		<xml>
			<o:OfficeDocumentSettings>
			<o:AllowPNG/>
			<o:PixelsPerInch>96</o:PixelsPerInch>
			</o:OfficeDocumentSettings>
		</xml>
		<![endif]-->
		<meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<title>*|MC:SUBJECT|*</title>

    <style type="text/css">
		p{
			margin:10px 0;
			padding:0;
		}
		table{
			border-collapse:collapse;
		}
		h1,h2,h3,h4,h5,h6{
			display:block;
			margin:0;
			padding:0;
		}
		img,a img{
			border:0;
			height:auto;
			outline:none;
			text-decoration:none;
		}
		body,#bodyTable,#bodyCell{
			height:100%;
			margin:0;
			padding:0;
			width:100%;
		}
		#outlook a{
			padding:0;
		}
		img{
			-ms-interpolation-mode:bicubic;
		}
		table{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}
		.ReadMsgBody{
			width:100%;
		}
		.ExternalClass{
			width:100%;
		}
		p,a,li,td,blockquote{
			mso-line-height-rule:exactly;
		}
		a[href^=tel],a[href^=sms]{
			color:inherit;
			cursor:default;
			text-decoration:none;
		}
		p,a,li,td,body,table,blockquote{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}
		.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{
			line-height:100%;
		}
		a[x-apple-data-detectors]{
			color:inherit !important;
			text-decoration:none !important;
			font-size:inherit !important;
			font-family:inherit !important;
			font-weight:inherit !important;
			line-height:inherit !important;
		}
		.templateContainer{
			max-width:600px !important;
		}
		a.mcnButton{
			display:block;
		}
		.mcnImage{
			vertical-align:bottom;
		}
		.mcnTextContent{
			word-break:break-word;
		}
		.mcnTextContent img{
			height:auto !important;
		}
		.mcnDividerBlock{
			table-layout:fixed !important;
		}
	/*
	@tab Page
	@section Background Style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		body,#bodyTable{
			/*@editable*/background-color:#FAFAFA;
		}
	/*
	@tab Page
	@section Background Style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		#bodyCell{
			/*@editable*/border-top:0;
		}
	/*
	@tab Page
	@section Heading 1
	@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
	@style heading 1
	*/
		h1{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:26px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section Heading 2
	@tip Set the styling for all second-level headings in your emails.
	@style heading 2
	*/
		h2{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:22px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section Heading 3
	@tip Set the styling for all third-level headings in your emails.
	@style heading 3
	*/
		h3{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:20px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section Heading 4
	@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
	@style heading 4
	*/
		h4{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:18px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section Preheader Style
	@tip Set the background color and borders for your email's preheader area.
	*/
		#templatePreheader{
			/*@editable*/background-color:#FAFAFA;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Preheader
	@section Preheader Text
	@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
	*/
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{
			/*@editable*/color:#656565;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:12px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section Preheader Link
	@tip Set the styling for your email's preheader links. Choose a color that helps them stand out from your text.
	*/
		#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{
			/*@editable*/color:#656565;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Header
	@section Header Style
	@tip Set the background color and borders for your email's header area.
	*/
		#templateHeader{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:0;
		}
	/*
	@tab Header
	@section Header Text
	@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
	*/
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Header
	@section Header Link
	@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
	*/
		#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{
			/*@editable*/color:#2BAADF;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Body
	@section Body Style
	@tip Set the background color and borders for your email's body area.
	*/
		#templateBody{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Body
	@section Body Text
	@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
	*/
		#templateBody .mcnTextContent,#templateBody .mcnTextContent p{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Body
	@section Body Link
	@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
	*/
		#templateBody .mcnTextContent a,#templateBody .mcnTextContent p a{
			/*@editable*/color:#2BAADF;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Columns
	@section Column Style
	@tip Set the background color and borders for your email's columns.
	*/
		#templateColumns{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:2px solid #EAEAEA;
			/*@editable*/padding-top:0;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Columns
	@section Column Text
	@tip Set the styling for your email's column text. Choose a size and color that is easy to read.
	*/
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Columns
	@section Column Link
	@tip Set the styling for your email's column links. Choose a color that helps them stand out from your text.
	*/
		#templateColumns .columnContainer .mcnTextContent a,#templateColumns .columnContainer .mcnTextContent p a{
			/*@editable*/color:#2BAADF;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Footer
	@section Footer Style
	@tip Set the background color and borders for your email's footer area.
	*/
		#templateFooter{
			/*@editable*/background-color:#FAFAFA;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Footer
	@section Footer Text
	@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
	*/
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{
			/*@editable*/color:#656565;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:12px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:center;
		}
	/*
	@tab Footer
	@section Footer Link
	@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
	*/
		#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{
			/*@editable*/color:#656565;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	@media only screen and (min-width:768px){
		.templateContainer{
			width:600px !important;
		}

}	@media only screen and (max-width: 480px){
		body,table,td,p,a,li,blockquote{
			-webkit-text-size-adjust:none !important;
		}

}	@media only screen and (max-width: 480px){
		body{
			width:100% !important;
			min-width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		#bodyCell{
			padding-top:10px !important;
		}

}	@media only screen and (max-width: 480px){
		.columnWrapper{
			max-width:100% !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImage{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnCaptionTopContent,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{
			max-width:100% !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnBoxedTextContentContainer{
			min-width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageGroupContent{
			padding:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{
			padding-top:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageCardBottomImageContent{
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageGroupBlockInner{
			padding-top:0 !important;
			padding-bottom:0 !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageGroupBlockOuter{
			padding-top:9px !important;
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnTextContent,.mcnBoxedTextContentColumn{
			padding-right:18px !important;
			padding-left:18px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{
			padding-right:18px !important;
			padding-bottom:0 !important;
			padding-left:18px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcpreview-image-uploader{
			display:none !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 1
	@tip Make the first-level headings larger in size for better readability on small screens.
	*/
		h1{
			/*@editable*/font-size:22px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 2
	@tip Make the second-level headings larger in size for better readability on small screens.
	*/
		h2{
			/*@editable*/font-size:20px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 3
	@tip Make the third-level headings larger in size for better readability on small screens.
	*/
		h3{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 4
	@tip Make the fourth-level headings larger in size for better readability on small screens.
	*/
		h4{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:150% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Boxed Text
	@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:150% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Visibility
	@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
	*/
		#templatePreheader{
			/*@editable*/display:block !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Text
	@tip Make the preheader text larger in size for better readability on small screens.
	*/
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:150% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Header Text
	@tip Make the header text larger in size for better readability on small screens.
	*/
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:150% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Body Text
	@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		#templateBody .mcnTextContent,#templateBody .mcnTextContent p{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:150% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Column Text
	@tip Make the column text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:150% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Footer Text
	@tip Make the footer content text larger in size for better readability on small screens.
	*/
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:150% !important;
		}

}</style></head>
    <body>
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                <tr>
                    <td align="center" valign="top" id="bodyCell">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
								<td align="center" valign="top" id="templatePreheader">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="preheaderContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
    <tbody class="mcnImageBlockOuter">
            <tr>
                <td valign="top" style="padding:9px" class="mcnImageBlockInner">
                    <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
                        <tbody><tr>
                            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">


                                        <img align="center" alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/21adee04-1b96-4836-802c-e535315d88bf.jpg" width="564" style="max-width:603px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">


                            </td>
                        </tr>
                    </tbody></table>
                </td>
            </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateHeader">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong><span style="font-size:18px">Appointment Confirmation</span></strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateBody">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <h1 style="text-align: left;"><span style="font-size:16px">Booking ID #"""+booking_id+"""</span></h1>

<p style="text-align: left; line-height: normal;">Your Carcrew booking for has been confirmed. Time chosen by you is between """+ time_start +""" &nbsp;on """+ date +""". If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</p>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateColumns">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
                                        <tr>
                                            <td valign="top">
												<!--[if gte mso 9]>
												<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
												<tr>
												<td align="center" valign="top" width="200" style="width:200px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="columnWrapper">
													<tr>
														<td valign="top" class="columnContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong>Step #1</strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/3dea4e90-c001-4c16-9397-a80b4a2511cc.png" width="164" style="max-width:700px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding:0 9px 0 9px;" width="164">

        </td>
    </tr>
</tbody></table>





            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><span style="font-size:12px">Our team reaches the given address. Our staff will require access to <u>water source</u> and an <u>electricity power point</u>. &nbsp;</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="200" style="width:200px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="columnWrapper">
													<tr>
														<td valign="top" class="columnContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong>Step #2</strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/f0af2571-2ceb-47e6-adb8-6b9418777c21.png" width="164" style="max-width:700px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding:0 9px 0 9px;" width="164">

        </td>
    </tr>
</tbody></table>





            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><span style="font-size:12px">Our team will perform the requested job.</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="200" style="width:200px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="columnWrapper">
													<tr>
														<td valign="top" class="columnContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong>Step #3</strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/2f767aab-44ab-4610-bf89-85faba56435f.png" width="164" style="max-width:200px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding:0 9px 0 9px;" width="164">

        </td>
    </tr>
</tbody></table>





            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><span style="font-size:12px">Our team will collect the cash, and will give you a job receipt. Note: Kindly keep the car windows open in case of dry cleaning jobs.</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												</tr>
												</table>
												<![endif]-->
											</td>
										</tr>
									</table>
								</td>
                            </tr>
                            <tr>
								<td align="center" valign="top" id="templateFooter">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="footerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer">
    <tbody><tr>
        <td align="center" style="padding-left:9px;padding-right:9px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
                        <table border="0" cellpadding="0" cellspacing="0">
                            <tbody><tr>
                                <td valign="top">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->



                                            <table align="left" border="0" cellpadding="0" cellspacing="0">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
                                                                                    <a href="http://www.twitter.com/theclickgarage" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display:block;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
                                                                                    <a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display:block;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:0; padding-bottom:9px;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
                                                                                    <a href="www.carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display:block;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>


                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
    <tbody class="mcnDividerBlockOuter">
        <tr>
            <td class="mcnDividerBlockInner" style="min-width: 100%; padding: 10px 18px 25px;">
                <table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top-width: 2px;border-top-style: solid;border-top-color: #EEEEEE;">
                    <tbody><tr>
                        <td>
                            <span></span>
                        </td>
                    </tr>
                </tbody></table>
<!--
                <td class="mcnDividerBlockInner" style="padding: 18px;">
                <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
-->
            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: left;"><em style="background-color: #CCCCCC;color: #606060;font-family: helvetica;font-size: 11px;line-height: 13.75px;"><span style="background-color:#FFFFFF">Copyright (C) 2015 Sui Generis Innovations, All rights reserved.</span></em><br>
<span style="color: #606060;font-family: helvetica;font-size: 11px;line-height: 13.75px;">Email : sales@carcrew.in | Phone No. : +91-7045996415</span></div>

<div style="text-align: left;"><br>
<span style="color: #606060;font-family: helvetica;font-size: 11px;line-height: 13.75px;">W-22, Second Floor, Green Park, New Delhi - 110016</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>"""


	script = MIMEText(html, 'html')

	msg.attach(script)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#     host = smtp_server,
	#     port = smtp_port,
	#     timeout = 30
	# )
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	#
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())



def send_booking_email_pick(to_address,to_name,time_start,date,booking_id):
	me = from_address
	you = to_address

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Confirmation! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
	<head>
		<!-- NAME: 1:3 COLUMN - BANDED -->
		<!--[if gte mso 15]>
		<xml>
			<o:OfficeDocumentSettings>
			<o:AllowPNG/>
			<o:PixelsPerInch>96</o:PixelsPerInch>
			</o:OfficeDocumentSettings>
		</xml>
		<![endif]-->
		<meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<title>*|MC:SUBJECT|*</title>

    <style type="text/css">
		p{
			margin:10px 0;
			padding:0;
		}
		table{
			border-collapse:collapse;
		}
		h1,h2,h3,h4,h5,h6{
			display:block;
			margin:0;
			padding:0;
		}
		img,a img{
			border:0;
			height:auto;
			outline:none;
			text-decoration:none;
		}
		body,#bodyTable,#bodyCell{
			height:100%;
			margin:0;
			padding:0;
			width:100%;
		}
		#outlook a{
			padding:0;
		}
		img{
			-ms-interpolation-mode:bicubic;
		}
		table{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}
		.ReadMsgBody{
			width:100%;
		}
		.ExternalClass{
			width:100%;
		}
		p,a,li,td,blockquote{
			mso-line-height-rule:exactly;
		}
		a[href^=tel],a[href^=sms]{
			color:inherit;
			cursor:default;
			text-decoration:none;
		}
		p,a,li,td,body,table,blockquote{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}
		.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{
			line-height:100%;
		}
		a[x-apple-data-detectors]{
			color:inherit !important;
			text-decoration:none !important;
			font-size:inherit !important;
			font-family:inherit !important;
			font-weight:inherit !important;
			line-height:inherit !important;
		}
		.templateContainer{
			max-width:600px !important;
		}
		a.mcnButton{
			display:block;
		}
		.mcnImage{
			vertical-align:bottom;
		}
		.mcnTextContent{
			word-break:break-word;
		}
		.mcnTextContent img{
			height:auto !important;
		}
		.mcnDividerBlock{
			table-layout:fixed !important;
		}
	/*
	@tab Page
	@section Background Style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		body,#bodyTable{
			/*@editable*/background-color:#FAFAFA;
		}
	/*
	@tab Page
	@section Background Style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		#bodyCell{
			/*@editable*/border-top:0;
		}
	/*
	@tab Page
	@section Heading 1
	@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
	@style heading 1
	*/
		h1{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:26px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:32px;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section Heading 2
	@tip Set the styling for all second-level headings in your emails.
	@style heading 2
	*/
		h2{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:22px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:30px;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section Heading 3
	@tip Set the styling for all third-level headings in your emails.
	@style heading 3
	*/
		h3{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:20px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:26px;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section Heading 4
	@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
	@style heading 4
	*/
		h4{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:18px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:24px;
			/*@editable*/letter-spacing:normal;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section Preheader Style
	@tip Set the background color and borders for your email's preheader area.
	*/
		#templatePreheader{
			/*@editable*/background-color:#FAFAFA;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Preheader
	@section Preheader Text
	@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
	*/
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{
			/*@editable*/color:#656565;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:12px;
			/*@editable*/line-height:18px;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section Preheader Link
	@tip Set the styling for your email's preheader links. Choose a color that helps them stand out from your text.
	*/
		#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{
			/*@editable*/color:#656565;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Header
	@section Header Style
	@tip Set the background color and borders for your email's header area.
	*/
		#templateHeader{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:0;
		}
	/*
	@tab Header
	@section Header Text
	@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
	*/
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/line-height:24px;
			/*@editable*/text-align:left;
		}
	/*
	@tab Header
	@section Header Link
	@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
	*/
		#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{
			/*@editable*/color:#2BAADF;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Body
	@section Body Style
	@tip Set the background color and borders for your email's body area.
	*/
		#templateBody{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Body
	@section Body Text
	@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
	*/
		#templateBody .mcnTextContent,#templateBody .mcnTextContent p{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/line-height:24px;
			/*@editable*/text-align:left;
		}
	/*
	@tab Body
	@section Body Link
	@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
	*/
		#templateBody .mcnTextContent a,#templateBody .mcnTextContent p a{
			/*@editable*/color:#2BAADF;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Columns
	@section Column Style
	@tip Set the background color and borders for your email's columns.
	*/
		#templateColumns{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:2px solid #EAEAEA;
			/*@editable*/padding-top:0;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Columns
	@section Column Text
	@tip Set the styling for your email's column text. Choose a size and color that is easy to read.
	*/
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{
			/*@editable*/color:#202020;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/line-height:24px;
			/*@editable*/text-align:left;
		}
	/*
	@tab Columns
	@section Column Link
	@tip Set the styling for your email's column links. Choose a color that helps them stand out from your text.
	*/
		#templateColumns .columnContainer .mcnTextContent a,#templateColumns .columnContainer .mcnTextContent p a{
			/*@editable*/color:#2BAADF;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Footer
	@section Footer Style
	@tip Set the background color and borders for your email's footer area.
	*/
		#templateFooter{
			/*@editable*/background-color:#FAFAFA;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
			/*@editable*/padding-top:9px;
			/*@editable*/padding-bottom:9px;
		}
	/*
	@tab Footer
	@section Footer Text
	@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
	*/
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{
			/*@editable*/color:#656565;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:12px;
			/*@editable*/line-height:18px;
			/*@editable*/text-align:center;
		}
	/*
	@tab Footer
	@section Footer Link
	@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
	*/
		#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{
			/*@editable*/color:#656565;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	@media only screen and (min-width:768px){
		.templateContainer{
			width:600px !important;
		}

}	@media only screen and (max-width: 480px){
		body,table,td,p,a,li,blockquote{
			-webkit-text-size-adjust:none !important;
		}

}	@media only screen and (max-width: 480px){
		body{
			width:100% !important;
			min-width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		#bodyCell{
			padding-top:10px !important;
		}

}	@media only screen and (max-width: 480px){
		.columnWrapper{
			max-width:100% !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImage{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnShareContent,.mcnCaptionTopContent,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{
			max-width:100% !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnBoxedTextContentContainer{
			min-width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageGroupContent{
			padding:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{
			padding-top:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageCardBottomImageContent{
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageGroupBlockInner{
			padding-top:0 !important;
			padding-bottom:0 !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageGroupBlockOuter{
			padding-top:9px !important;
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnTextContent,.mcnBoxedTextContentColumn{
			padding-right:18px !important;
			padding-left:18px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{
			padding-right:18px !important;
			padding-bottom:0 !important;
			padding-left:18px !important;
		}

}	@media only screen and (max-width: 480px){
		.mcpreview-image-uploader{
			display:none !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 1
	@tip Make the first-level headings larger in size for better readability on small screens.
	*/
		h1{
			/*@editable*/font-size:22px !important;
			/*@editable*/line-height:28px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 2
	@tip Make the second-level headings larger in size for better readability on small screens.
	*/
		h2{
			/*@editable*/font-size:20px !important;
			/*@editable*/line-height:26px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 3
	@tip Make the third-level headings larger in size for better readability on small screens.
	*/
		h3{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:24px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Heading 4
	@tip Make the fourth-level headings larger in size for better readability on small screens.
	*/
		h4{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:22px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Boxed Text
	@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:22px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Visibility
	@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
	*/
		#templatePreheader{
			/*@editable*/display:block !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Text
	@tip Make the preheader text larger in size for better readability on small screens.
	*/
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:22px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Header Text
	@tip Make the header text larger in size for better readability on small screens.
	*/
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:24px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Body Text
	@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		#templateBody .mcnTextContent,#templateBody .mcnTextContent p{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:24px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Column Text
	@tip Make the column text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:24px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Footer Text
	@tip Make the footer content text larger in size for better readability on small screens.
	*/
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:22px !important;
		}

}</style></head>
    <body>
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                <tr>
                    <td align="center" valign="top" id="bodyCell">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
								<td align="center" valign="top" id="templatePreheader">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="preheaderContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="366" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 0px 9px 18px; line-height: normal;">


                        </td>
                    </tr>
                </tbody></table>

                <table align="right" border="0" cellpadding="0" cellspacing="0" width="197" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px 9px 0px; line-height: normal;">

                            <a href="*|ARCHIVE|*" target="_blank"></a>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
    <tbody class="mcnImageBlockOuter">
            <tr>
                <td valign="top" style="padding:9px" class="mcnImageBlockInner">
                    <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
                        <tbody><tr>
                            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">


                                        <img align="center" alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/8b0df50f-a54b-4a7b-9ef6-c31d66aff1f1.jpg" width="564" style="max-width:1440px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">


                            </td>
                        </tr>
                    </tbody></table>
                </td>
            </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateHeader">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong><span style="font-size:18px">Appointment Confirmation</span></strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateBody">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <h1 style="text-align: left;"><span style="font-size:16px">Booking ID #"""+booking_id+"""</span></h1>

<p style="text-align: left; line-height: normal;">Hi """+to_name+""",</p>
<p style="text-align: left; line-height: normal;">Your Carcrew booking for has been confirmed. Pick up time chosen by you is """+ time_start +""" on """+ date +""". If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</p>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateColumns">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
                                        <tr>
                                            <td align="center" valign="top">
												<!--[if gte mso 9]>
												<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
												<tr>
												<td align="center" valign="top" width="200" style="width:200px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="columnWrapper">
													<tr>
														<td valign="top" class="columnContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong>Step #1</strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/b3c5a6a3-90de-420b-b750-7194672f4dbd.png" width="164" style="max-width:200px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding:0 9px 0 9px;" width="164">

        </td>
    </tr>
</tbody></table>





            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><span style="font-size:12px">Our driver does a quick vehicle inspection and gives you a <u>receipt</u>. You will have to keep the <u>RC</u>&nbsp;&amp;&nbsp;<u>service coupon</u> (if applicable) handy.</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="200" style="width:200px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="columnWrapper">
													<tr>
														<td valign="top" class="columnContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong>Step #2</strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/24862755-3aee-46c4-8dc5-3c5d674ea029.png" width="164" style="max-width:200px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding:0 9px 0 9px;" width="164">

        </td>
    </tr>
</tbody></table>





            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><span style="font-size:12px">Our AutoExpert&nbsp;interacts with the service station staff and&nbsp;informs you about <u>additional jobs required</u> and <u>cost estimate revisions</u>&nbsp;(if any)</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="200" style="width:200px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="columnWrapper">
													<tr>
														<td valign="top" class="columnContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><strong>Step #3</strong></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/2f767aab-44ab-4610-bf89-85faba56435f.png" width="164" style="max-width:200px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding:0 9px 0 9px;" width="164">

        </td>
    </tr>
</tbody></table>





            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="200" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: center;"><span style="font-size:12px">Our driver drives the vehicle to&nbsp;the drop-off location.&nbsp;You must keep the <u>receipt</u>&nbsp;and <u>amount due</u> ready for collecting the vehicle back.</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												</tr>
												</table>
												<![endif]-->
											</td>
										</tr>
									</table>
								</td>
                            </tr>
                            <tr>
								<td align="center" valign="top" id="templateFooter">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
										<tr>
                                			<td valign="top" class="footerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer">
    <tbody><tr>
        <td align="center" style="padding-left:9px;padding-right:9px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
                        <table border="0" cellpadding="0" cellspacing="0">
                            <tbody><tr>
                                <td valign="top">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->



                                            <table align="left" border="0" cellpadding="0" cellspacing="0">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
                                                                                    <a href="http://www.twitter.com/theclickgarage" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display:block;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
                                                                                    <a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display:block;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:0; padding-bottom:9px;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
                                                                                    <a href="www.Carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display:block;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>


                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
    <tbody class="mcnDividerBlockOuter">
        <tr>
            <td class="mcnDividerBlockInner" style="min-width: 100%; padding: 10px 18px 25px;">
                <table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top-width: 2px;border-top-style: solid;border-top-color: #EEEEEE;">
                    <tbody><tr>
                        <td>
                            <span></span>
                        </td>
                    </tr>
                </tbody></table>
<!--
                <td class="mcnDividerBlockInner" style="padding: 18px;">
                <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
-->
            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding: 9px 18px; line-height: normal;">

                            <div style="text-align: left;"><em style="background-color: #CCCCCC;color: #606060;font-family: helvetica;font-size: 11px;line-height: 13.75px;"><span style="background-color:#FFFFFF">Copyright (C) 2015 Sui Generis Innovations, All rights reserved.</span></em><br>
<span style="color: #606060;font-family: helvetica;font-size: 11px;line-height: 13.75px;">Email : sales@carcrew.in | Phone No. : +91-7045996415</span></div>

<div style="text-align: left;"><br>
<span style="color: #606060;font-family: helvetica;font-size: 11px;line-height: 13.75px;">W-22, Second Floor, Green Park, New Delhi - 110016</span></div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>"""


	script = MIMEText(html, 'html')

	msg.attach(script)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#    host = smtp_server,
	#    port = smtp_port,
	#    timeout = 30
	# )
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()

	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())

#send_booking(to_address="y.shashwat@gmail.com",to_name="Shashwat",service="Servicing",time_start="9:00AM",time_end="10:00AM",date="16-Aug-2015",booking_id="0001")



def send_ses(fromaddr,subject,body,recipient, attachment=None,filename=''):
	"""Send an email via the Amazon SES service.

    Example:
      send_ses('me@example.com, 'greetings', "Hi!", 'you@example.com)

    Return:
      If 'ErrorResponse' appears in the return message from SES,
      return the message, otherwise return an empty '' string.
    """
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg['From'] = fromaddr
	msg['To'] = recipient
	msg.attach(MIMEText(body))
	if attachment:
		part = MIMEApplication(attachment)
		part.add_header('Content-Disposition', 'attachment', filename=filename)
		msg.attach(part)

	smtp_username = 'AKIAJ4U5VOXPWBT37X4A'
	smtp_password = 'AkJxDBO/FOsxkF1Ucd1EhblV5DTAVLpFfqWQv/KI2gn7'
	# conn = boto.connect_ses(smtp_username,smtp_password)
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())
	return result if 'ErrorResponse' in result else ''

def send_booking_email1(to_address,to_name,time_start,date,booking_id):
	me = from_address
	you = to_address

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Confirmation! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
	<html xmlns="http://www.w3.org/1999/xhtml">
	    <head>
	    	<!-- NAME: 1 COLUMN -->
	        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
	        <meta name="viewport" content="width=device-width, initial-scale=1.0">
	        <title>*|MC:SUBJECT|*</title>

	    <style type="text/css">
			body,#bodyTable,#bodyCell{
				height:100% !important;
				margin:0;
				padding:0;
				width:100% !important;
			}
			table{
				border-collapse:collapse;
			}
			img,a img{
				border:0;
				outline:none;
				text-decoration:none;
			}
			h1,h2,h3,h4,h5,h6{
				margin:0;
				padding:0;
			}
			p{
				margin:1em 0;
				padding:0;
			}
			a{
				word-wrap:break-word;
			}
			.ReadMsgBody{
				width:100%;
			}
			.ExternalClass{
				width:100%;
			}
			.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{
				line-height:100%;
			}
			table,td{
				mso-table-lspace:0pt;
				mso-table-rspace:0pt;
			}
			#outlook a{
				padding:0;
			}
			img{
				-ms-interpolation-mode:bicubic;
			}
			body,table,td,p,a,li,blockquote{
				-ms-text-size-adjust:100%;
				-webkit-text-size-adjust:100%;
			}
			#bodyCell{
				padding:20px;
			}
			.mcnImage{
				vertical-align:bottom;
			}
			.mcnTextContent img{
				height:auto !important;
			}
		/*
		@tab Page
		@section background style
		@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
		*/
			body,#bodyTable{
				/*@editable*/background-color:#F2F2F2;
			}
		/*
		@tab Page
		@section background style
		@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
		*/
			#bodyCell{
				/*@editable*/border-top:0;
			}
		/*
		@tab Page
		@section email border
		@tip Set the border for your email.
		*/
			#templateContainer{
				/*@editable*/border:0;
			}
		/*
		@tab Page
		@section heading 1
		@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
		@style heading 1
		*/
			h1{
				/*@editable*/color:#606060 !important;
				display:block;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:40px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:-1px;
				margin:0;
				/*@editable*/text-align:left;
			}
		/*
		@tab Page
		@section heading 2
		@tip Set the styling for all second-level headings in your emails.
		@style heading 2
		*/
			h2{
				/*@editable*/color:#404040 !important;
				display:block;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:26px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:-.75px;
				margin:0;
				/*@editable*/text-align:left;
			}
		/*
		@tab Page
		@section heading 3
		@tip Set the styling for all third-level headings in your emails.
		@style heading 3
		*/
			h3{
				/*@editable*/color:#606060 !important;
				display:block;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:18px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:-.5px;
				margin:0;
				/*@editable*/text-align:left;
			}
		/*
		@tab Page
		@section heading 4
		@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
		@style heading 4
		*/
			h4{
				/*@editable*/color:#808080 !important;
				display:block;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:16px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:normal;
				margin:0;
				/*@editable*/text-align:left;
			}
		/*
		@tab Preheader
		@section preheader style
		@tip Set the background color and borders for your email's preheader area.
		*/
			#templatePreheader{
				/*@editable*/background-color:#FFFFFF;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
			}
		/*
		@tab Preheader
		@section preheader text
		@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
		*/
			.preheaderContainer .mcnTextContent,.preheaderContainer .mcnTextContent p{
				/*@editable*/color:#606060;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:11px;
				/*@editable*/line-height:125%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Preheader
		@section preheader link
		@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
		*/
			.preheaderContainer .mcnTextContent a{
				/*@editable*/color:#606060;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		/*
		@tab Header
		@section header style
		@tip Set the background color and borders for your email's header area.
		*/
			#templateHeader{
				/*@editable*/background-color:#ffffff;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
			}
		/*
		@tab Header
		@section header text
		@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
		*/
			.headerContainer .mcnTextContent,.headerContainer .mcnTextContent p{
				/*@editable*/color:#606060;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:15px;
				/*@editable*/line-height:150%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Header
		@section header link
		@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
		*/
			.headerContainer .mcnTextContent a{
				/*@editable*/color:#6DC6DD;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		/*
		@tab Body
		@section body style
		@tip Set the background color and borders for your email's body area.
		*/
			#templateBody{
				/*@editable*/background-color:#fafafa;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
			}
		/*
		@tab Body
		@section body text
		@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
		*/
			.bodyContainer .mcnTextContent,.bodyContainer .mcnTextContent p{
				/*@editable*/color:#606060;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:15px;
				/*@editable*/line-height:150%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Body
		@section body link
		@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
		*/
			.bodyContainer .mcnTextContent a{
				/*@editable*/color:#6DC6DD;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		/*
		@tab Footer
		@section footer style
		@tip Set the background color and borders for your email's footer area.
		*/
			#templateFooter{
				/*@editable*/background-color:#cccccc;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
			}
		/*
		@tab Footer
		@section footer text
		@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
		*/
			.footerContainer .mcnTextContent,.footerContainer .mcnTextContent p{
				/*@editable*/color:#606060;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:11px;
				/*@editable*/line-height:125%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Footer
		@section footer link
		@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
		*/
			.footerContainer .mcnTextContent a{
				/*@editable*/color:#606060;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		@media only screen and (max-width: 480px){
			body,table,td,p,a,li,blockquote{
				-webkit-text-size-adjust:none !important;
			}

	}	@media only screen and (max-width: 480px){
			body{
				width:100% !important;
				min-width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			td[id=bodyCell]{
				padding:10px !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcnTextContentContainer]{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcnBoxedTextContentContainer]{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcpreview-image-uploader]{
				width:100% !important;
				display:none !important;
			}

	}	@media only screen and (max-width: 480px){
			img[class=mcnImage]{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcnImageGroupContentContainer]{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageGroupContent]{
				padding:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageGroupBlockInner]{
				padding-bottom:0 !important;
				padding-top:0 !important;
			}

	}	@media only screen and (max-width: 480px){
			tbody[class=mcnImageGroupBlockOuter]{
				padding-bottom:9px !important;
				padding-top:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcnCaptionTopContent],table[class=mcnCaptionBottomContent]{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcnCaptionLeftTextContentContainer],table[class=mcnCaptionRightTextContentContainer],table[class=mcnCaptionLeftImageContentContainer],table[class=mcnCaptionRightImageContentContainer],table[class=mcnImageCardLeftTextContentContainer],table[class=mcnImageCardRightTextContentContainer]{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
				padding-right:18px !important;
				padding-left:18px !important;
				padding-bottom:0 !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageCardBottomImageContent]{
				padding-bottom:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageCardTopImageContent]{
				padding-top:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
				padding-right:18px !important;
				padding-left:18px !important;
				padding-bottom:0 !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageCardBottomImageContent]{
				padding-bottom:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnImageCardTopImageContent]{
				padding-top:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			table[class=mcnCaptionLeftContentOuter] td[class=mcnTextContent],table[class=mcnCaptionRightContentOuter] td[class=mcnTextContent]{
				padding-top:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnCaptionBlockInner] table[class=mcnCaptionTopContent]:last-child td[class=mcnTextContent]{
				padding-top:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnBoxedTextContentColumn]{
				padding-left:18px !important;
				padding-right:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=mcnTextContent]{
				padding-right:18px !important;
				padding-left:18px !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section template width
		@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.
		*/
			table[id=templateContainer],table[id=templatePreheader],table[id=templateHeader],table[id=templateBody],table[id=templateFooter]{
				/*@tab Mobile Styles
	@section template width
	@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.*/max-width:600px !important;
				/*@editable*/width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section heading 1
		@tip Make the first-level headings larger in size for better readability on small screens.
		*/
			h1{
				/*@editable*/font-size:24px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section heading 2
		@tip Make the second-level headings larger in size for better readability on small screens.
		*/
			h2{
				/*@editable*/font-size:20px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section heading 3
		@tip Make the third-level headings larger in size for better readability on small screens.
		*/
			h3{
				/*@editable*/font-size:18px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section heading 4
		@tip Make the fourth-level headings larger in size for better readability on small screens.
		*/
			h4{
				/*@editable*/font-size:16px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Boxed Text
		@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
		*/
			table[class=mcnBoxedTextContentContainer] td[class=mcnTextContent],td[class=mcnBoxedTextContentContainer] td[class=mcnTextContent] p{
				/*@editable*/font-size:18px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Preheader Visibility
		@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
		*/
			table[id=templatePreheader]{
				/*@editable*/display:block !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Preheader Text
		@tip Make the preheader text larger in size for better readability on small screens.
		*/
			td[class=preheaderContainer] td[class=mcnTextContent],td[class=preheaderContainer] td[class=mcnTextContent] p{
				/*@editable*/font-size:14px !important;
				/*@editable*/line-height:115% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Header Text
		@tip Make the header text larger in size for better readability on small screens.
		*/
			td[class=headerContainer] td[class=mcnTextContent],td[class=headerContainer] td[class=mcnTextContent] p{
				/*@editable*/font-size:18px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Body Text
		@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
		*/
			td[class=bodyContainer] td[class=mcnTextContent],td[class=bodyContainer] td[class=mcnTextContent] p{
				/*@editable*/font-size:18px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section footer text
		@tip Make the body content text larger in size for better readability on small screens.
		*/
			td[class=footerContainer] td[class=mcnTextContent],td[class=footerContainer] td[class=mcnTextContent] p{
				/*@editable*/font-size:14px !important;
				/*@editable*/line-height:115% !important;
			}

	}	@media only screen and (max-width: 480px){
			td[class=footerContainer] a[class=utilityLink]{
				display:block !important;
			}

	}</style></head>
	    <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
	        <center>
	            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
	                <tr>
	                    <td align="center" valign="top" id="bodyCell">
	                        <!-- BEGIN TEMPLATE // -->
	                        <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateContainer">
	                            <tr>
	                                <td align="center" valign="top">

	                                </td>
	                            </tr>
	                            <tr>
	                                <td align="center" valign="top">
	                                    <!-- BEGIN HEADER // -->
	                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateHeader">
	                                        <tr>
	                                            <td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock">
	    <tbody class="mcnImageBlockOuter">
	            <tr>
	                <td valign="top" style="padding:9px" class="mcnImageBlockInner">
	                    <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer">
	                        <tbody><tr>
	                            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">


	                                        <img align="center" alt="" src="http://blog.clickgarage.in/wp-content/uploads/2015/09/ClickGarage_Final-e1443311969815.png" width="300" style="max-width:300px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">


	                            </td>
	                        </tr>
	                    </tbody></table>
	                </td>
	            </tr>
	    </tbody>
	</table></td>
	                                        </tr>
	                                    </table>
	                                    <!-- // END HEADER -->
	                                </td>
	                            </tr>
	                            <tr>
	                                <td align="center" valign="top">
	                                    <!-- BEGIN BODY // -->
	                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
	                                        <tr>
	                                            <td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
	    <tbody class="mcnTextBlockOuter">
	        <tr>
	            <td valign="top" class="mcnTextBlockInner">

	                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
	                    <tbody><tr>

	                        <td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

	                            <h1>Appointment Confirmation</h1>

	<h3><br>
	Booking ID #"""+booking_id+"""</h3>
	&nbsp;


	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Hi """+to_name+""",</span></span></p>
	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Your Carcrew booking has been confirmed. Pick up time chosen by you is """+ time_start +""" on """+ date +""". If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</span></span></p>

	<div>&nbsp;</div>

	                        </td>
	                    </tr>
	                </tbody></table>

	            </td>
	        </tr>
	    </tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock">
	    <tbody class="mcnFollowBlockOuter">
	        <tr>
	            <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
	                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer">
	    <tbody><tr>
	        <td align="center" style="padding-left:9px;padding-right:9px;">
	            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border: 1px solid #EEEEEE;background-color: #FAFAFA;">
	                <tbody><tr>
	                    <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
							<table border="0" cellpadding="0" cellspacing="0">
								<tbody><tr>
									<td valign="top">


				                                <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

				                                    <tbody><tr>
				                                        <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
				                                            <a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
				                                            <a href="http://www.facebook.com/carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Facebook</a>
				                                        </td>
				                                    </tr>

				                                </tbody></table>


									<!--[if gte mso 6]>
									</td>
							    	<td align="left" valign="top">
									<![endif]-->


				                                <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

				                                    <tbody><tr>
				                                        <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
				                                            <a href="http://www.twitter.com/clickgarage_in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-96.png" alt="Twitter" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
				                                            <a href="http://www.twitter.com/clickgarage_in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Twitter</a>
				                                        </td>
				                                    </tr>

				                                </tbody></table>


									<!--[if gte mso 6]>
									</td>
							    	<td align="left" valign="top">
									<![endif]-->


				                                <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

				                                    <tbody><tr>
				                                        <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:0; padding-bottom:5px;">
				                                            <a href="http://www.carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
				                                            <a href="http://www.carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Website</a>
				                                        </td>
				                                    </tr>

				                                </tbody></table>


									<!--[if gte mso 6]>
									</td>
							    	<td align="left" valign="top">
									<![endif]-->

									</td>
								</tr>
							</tbody></table>
	                    </td>
	                </tr>
	            </tbody></table>
	        </td>
	    </tr>
	</tbody></table>

	            </td>
	        </tr>
	    </tbody>
	</table></td>
	                                        </tr>
	                                    </table>
	                                    <!-- // END BODY -->
	                                </td>
	                            </tr>
	                            <tr>
	                                <td align="center" valign="top">
	                                    <!-- BEGIN FOOTER // -->
	                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateFooter">
	                                        <tr>
	                                            <td valign="top" class="footerContainer" style="padding-bottom:9px;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
	    <tbody class="mcnTextBlockOuter">
	        <tr>
	            <td valign="top" class="mcnTextBlockInner">

	                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
	                    <tbody><tr>

	                        <td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

	                            <em>Copyright (C) 2015 Sui Generis Innovations, All rights reserved.</em><br>
	Email : sales@carcrew.in | Phone No. : +91-7045996415<br>
	<br>
	W-22, Second Floor, Green Park, New Delhi - 110016
	                        </td>
	                    </tr>
	                </tbody></table>

	            </td>
	        </tr>
	    </tbody>
	</table></td>
	                                        </tr>
	                                    </table>
	                                    <!-- // END FOOTER -->
	                                </td>
	                            </tr>
	                        </table>
	                        <!-- // END TEMPLATE -->
	                    </td>
	                </tr>
	            </table>
	        </center>
	    </body>
	</html>

	"""


	script = MIMEText(html, 'html')

	msg.attach(script)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#     host = smtp_server,
	#     port = smtp_port,
	#     timeout = 30
	# )
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())

def send_cancel_email(to_address,to_name,booking_id_1):

	# me = from_address
	me = "Carcrew <bookings@clickgarage.in>"
	you = to_address
	booking_id = str(booking_id_1)

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Cancelled! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = you

	if 1:
		html = """
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml">
			<head>
				<!-- NAME: 1 COLUMN -->
				<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
				<meta name="viewport" content="width=device-width, initial-scale=1.0">
				<title>*|MC:SUBJECT|*</title>

			<style type="text/css">
				body,#bodyTable,#bodyCell{
					height:100% !important;
					margin:0;
					padding:0;
					width:100% !important;
				}
				table{
					border-collapse:collapse;
				}
				img,a img{
					border:0;
					outline:none;
					text-decoration:none;
				}
				h1,h2,h3,h4,h5,h6{
					margin:0;
					padding:0;
				}
				p{
					margin:1em 0;
					padding:0;
				}
				a{
					word-wrap:break-word;
				}
				.ReadMsgBody{
					width:100%;
				}
				.ExternalClass{
					width:100%;
				}
				.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{
					line-height:100%;
				}
				table,td{
					mso-table-lspace:0pt;
					mso-table-rspace:0pt;
				}
				#outlook a{
					padding:0;
				}
				img{
					-ms-interpolation-mode:bicubic;
				}
				body,table,td,p,a,li,blockquote{
					-ms-text-size-adjust:100%;
					-webkit-text-size-adjust:100%;
				}
				#bodyCell{
					padding:20px;
				}
				.mcnImage{
					vertical-align:bottom;
				}
				.mcnTextContent img{
					height:auto !important;
				}
			/*
			@tab Page
			@section background style
			@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
			*/
				body,#bodyTable{
					/*@editable*/background-color:#F2F2F2;
				}
			/*
			@tab Page
			@section background style
			@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
			*/
				#bodyCell{
					/*@editable*/border-top:0;
				}
			/*
			@tab Page
			@section email border
			@tip Set the border for your email.
			*/
				#templateContainer{
					/*@editable*/border:0;
				}
			/*
			@tab Page
			@section heading 1
			@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
			@style heading 1
			*/
				h1{
					/*@editable*/color:#606060 !important;
					display:block;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:40px;
					/*@editable*/font-style:normal;
					/*@editable*/font-weight:bold;
					/*@editable*/line-height:125%;
					/*@editable*/letter-spacing:-1px;
					margin:0;
					/*@editable*/text-align:left;
				}
			/*
			@tab Page
			@section heading 2
			@tip Set the styling for all second-level headings in your emails.
			@style heading 2
			*/
				h2{
					/*@editable*/color:#404040 !important;
					display:block;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:26px;
					/*@editable*/font-style:normal;
					/*@editable*/font-weight:bold;
					/*@editable*/line-height:125%;
					/*@editable*/letter-spacing:-.75px;
					margin:0;
					/*@editable*/text-align:left;
				}
			/*
			@tab Page
			@section heading 3
			@tip Set the styling for all third-level headings in your emails.
			@style heading 3
			*/
				h3{
					/*@editable*/color:#606060 !important;
					display:block;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:18px;
					/*@editable*/font-style:normal;
					/*@editable*/font-weight:bold;
					/*@editable*/line-height:125%;
					/*@editable*/letter-spacing:-.5px;
					margin:0;
					/*@editable*/text-align:left;
				}
			/*
			@tab Page
			@section heading 4
			@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
			@style heading 4
			*/
				h4{
					/*@editable*/color:#808080 !important;
					display:block;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:16px;
					/*@editable*/font-style:normal;
					/*@editable*/font-weight:bold;
					/*@editable*/line-height:125%;
					/*@editable*/letter-spacing:normal;
					margin:0;
					/*@editable*/text-align:left;
				}
			/*
			@tab Preheader
			@section preheader style
			@tip Set the background color and borders for your email's preheader area.
			*/
				#templatePreheader{
					/*@editable*/background-color:#FFFFFF;
					/*@editable*/border-top:0;
					/*@editable*/border-bottom:0;
				}
			/*
			@tab Preheader
			@section preheader text
			@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
			*/
				.preheaderContainer .mcnTextContent,.preheaderContainer .mcnTextContent p{
					/*@editable*/color:#606060;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:11px;
					/*@editable*/line-height:125%;
					/*@editable*/text-align:left;
				}
			/*
			@tab Preheader
			@section preheader link
			@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
			*/
				.preheaderContainer .mcnTextContent a{
					/*@editable*/color:#606060;
					/*@editable*/font-weight:normal;
					/*@editable*/text-decoration:underline;
				}
			/*
			@tab Header
			@section header style
			@tip Set the background color and borders for your email's header area.
			*/
				#templateHeader{
					/*@editable*/background-color:#ffffff;
					/*@editable*/border-top:0;
					/*@editable*/border-bottom:0;
				}
			/*
			@tab Header
			@section header text
			@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
			*/
				.headerContainer .mcnTextContent,.headerContainer .mcnTextContent p{
					/*@editable*/color:#606060;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:15px;
					/*@editable*/line-height:150%;
					/*@editable*/text-align:left;
				}
			/*
			@tab Header
			@section header link
			@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
			*/
				.headerContainer .mcnTextContent a{
					/*@editable*/color:#6DC6DD;
					/*@editable*/font-weight:normal;
					/*@editable*/text-decoration:underline;
				}
			/*
			@tab Body
			@section body style
			@tip Set the background color and borders for your email's body area.
			*/
				#templateBody{
					/*@editable*/background-color:#fafafa;
					/*@editable*/border-top:0;
					/*@editable*/border-bottom:0;
				}
			/*
			@tab Body
			@section body text
			@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
			*/
				.bodyContainer .mcnTextContent,.bodyContainer .mcnTextContent p{
					/*@editable*/color:#606060;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:15px;
					/*@editable*/line-height:150%;
					/*@editable*/text-align:left;
				}
			/*
			@tab Body
			@section body link
			@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
			*/
				.bodyContainer .mcnTextContent a{
					/*@editable*/color:#6DC6DD;
					/*@editable*/font-weight:normal;
					/*@editable*/text-decoration:underline;
				}
			/*
			@tab Footer
			@section footer style
			@tip Set the background color and borders for your email's footer area.
			*/
				#templateFooter{
					/*@editable*/background-color:#cccccc;
					/*@editable*/border-top:0;
					/*@editable*/border-bottom:0;
				}
			/*
			@tab Footer
			@section footer text
			@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
			*/
				.footerContainer .mcnTextContent,.footerContainer .mcnTextContent p{
					/*@editable*/color:#606060;
					/*@editable*/font-family:Helvetica;
					/*@editable*/font-size:11px;
					/*@editable*/line-height:125%;
					/*@editable*/text-align:left;
				}
			/*
			@tab Footer
			@section footer link
			@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
			*/
				.footerContainer .mcnTextContent a{
					/*@editable*/color:#606060;
					/*@editable*/font-weight:normal;
					/*@editable*/text-decoration:underline;
				}
			@media only screen and (max-width: 480px){
				body,table,td,p,a,li,blockquote{
					-webkit-text-size-adjust:none !important;
				}

		}	@media only screen and (max-width: 480px){
				body{
					width:100% !important;
					min-width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				td[id=bodyCell]{
					padding:10px !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcnTextContentContainer]{
					width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcnBoxedTextContentContainer]{
					width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcpreview-image-uploader]{
					width:100% !important;
					display:none !important;
				}

		}	@media only screen and (max-width: 480px){
				img[class=mcnImage]{
					width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcnImageGroupContentContainer]{
					width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageGroupContent]{
					padding:9px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageGroupBlockInner]{
					padding-bottom:0 !important;
					padding-top:0 !important;
				}

		}	@media only screen and (max-width: 480px){
				tbody[class=mcnImageGroupBlockOuter]{
					padding-bottom:9px !important;
					padding-top:9px !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcnCaptionTopContent],table[class=mcnCaptionBottomContent]{
					width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcnCaptionLeftTextContentContainer],table[class=mcnCaptionRightTextContentContainer],table[class=mcnCaptionLeftImageContentContainer],table[class=mcnCaptionRightImageContentContainer],table[class=mcnImageCardLeftTextContentContainer],table[class=mcnImageCardRightTextContentContainer]{
					width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
					padding-right:18px !important;
					padding-left:18px !important;
					padding-bottom:0 !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageCardBottomImageContent]{
					padding-bottom:9px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageCardTopImageContent]{
					padding-top:18px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
					padding-right:18px !important;
					padding-left:18px !important;
					padding-bottom:0 !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageCardBottomImageContent]{
					padding-bottom:9px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnImageCardTopImageContent]{
					padding-top:18px !important;
				}

		}	@media only screen and (max-width: 480px){
				table[class=mcnCaptionLeftContentOuter] td[class=mcnTextContent],table[class=mcnCaptionRightContentOuter] td[class=mcnTextContent]{
					padding-top:9px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnCaptionBlockInner] table[class=mcnCaptionTopContent]:last-child td[class=mcnTextContent]{
					padding-top:18px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnBoxedTextContentColumn]{
					padding-left:18px !important;
					padding-right:18px !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=mcnTextContent]{
					padding-right:18px !important;
					padding-left:18px !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section template width
			@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.
			*/
				table[id=templateContainer],table[id=templatePreheader],table[id=templateHeader],table[id=templateBody],table[id=templateFooter]{
					/*@tab Mobile Styles
		@section template width
		@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.*/max-width:600px !important;
					/*@editable*/width:100% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section heading 1
			@tip Make the first-level headings larger in size for better readability on small screens.
			*/
				h1{
					/*@editable*/font-size:24px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section heading 2
			@tip Make the second-level headings larger in size for better readability on small screens.
			*/
				h2{
					/*@editable*/font-size:20px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section heading 3
			@tip Make the third-level headings larger in size for better readability on small screens.
			*/
				h3{
					/*@editable*/font-size:18px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section heading 4
			@tip Make the fourth-level headings larger in size for better readability on small screens.
			*/
				h4{
					/*@editable*/font-size:16px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section Boxed Text
			@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
			*/
				table[class=mcnBoxedTextContentContainer] td[class=mcnTextContent],td[class=mcnBoxedTextContentContainer] td[class=mcnTextContent] p{
					/*@editable*/font-size:18px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section Preheader Visibility
			@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
			*/
				table[id=templatePreheader]{
					/*@editable*/display:block !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section Preheader Text
			@tip Make the preheader text larger in size for better readability on small screens.
			*/
				td[class=preheaderContainer] td[class=mcnTextContent],td[class=preheaderContainer] td[class=mcnTextContent] p{
					/*@editable*/font-size:14px !important;
					/*@editable*/line-height:115% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section Header Text
			@tip Make the header text larger in size for better readability on small screens.
			*/
				td[class=headerContainer] td[class=mcnTextContent],td[class=headerContainer] td[class=mcnTextContent] p{
					/*@editable*/font-size:18px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section Body Text
			@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
			*/
				td[class=bodyContainer] td[class=mcnTextContent],td[class=bodyContainer] td[class=mcnTextContent] p{
					/*@editable*/font-size:18px !important;
					/*@editable*/line-height:125% !important;
				}

		}	@media only screen and (max-width: 480px){
			/*
			@tab Mobile Styles
			@section footer text
			@tip Make the body content text larger in size for better readability on small screens.
			*/
				td[class=footerContainer] td[class=mcnTextContent],td[class=footerContainer] td[class=mcnTextContent] p{
					/*@editable*/font-size:14px !important;
					/*@editable*/line-height:115% !important;
				}

		}	@media only screen and (max-width: 480px){
				td[class=footerContainer] a[class=utilityLink]{
					display:block !important;
				}

		}</style></head>
			<body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
				<center>
					<table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
						<tr>
							<td align="center" valign="top" id="bodyCell">
								<!-- BEGIN TEMPLATE // -->
								<table border="0" cellpadding="0" cellspacing="0" width="600" id="templateContainer">
									<tr>
										<td align="center" valign="top">

										</td>
									</tr>
									<tr>
										<td align="center" valign="top">
											<!-- BEGIN HEADER // -->
											<table border="0" cellpadding="0" cellspacing="0" width="600" id="templateHeader">
												<tr>
													<td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock">
			<tbody class="mcnImageBlockOuter">
					<tr>
						<td valign="top" style="padding:9px" class="mcnImageBlockInner">
							<table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer">
								<tbody><tr>
									<td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">


												<img align="center" alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/97fa2077-7dc3-4c2e-92c9-4c5012d536b4.jpg" width="564" style="max-width:1440px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">


									</td>
								</tr>
							</tbody></table>
						</td>
					</tr>
			</tbody>
		</table></td>
												</tr>
											</table>
											<!-- // END HEADER -->
										</td>
									</tr>
									<tr>
										<td align="center" valign="top">
											<!-- BEGIN BODY // -->
											<table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
												<tr>
													<td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
			<tbody class="mcnTextBlockOuter">
				<tr>
					<td valign="top" class="mcnTextBlockInner">

						<table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
							<tbody><tr>

								<td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

									<h1>Appointment Cancelled</h1>

		<h3><br>
		Booking ID #"""+booking_id+"""</h3>
		&nbsp;


		<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Hi """+to_name+""",</span></span></p>
		<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">As requested your Carcrew booking has been cancelled. If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</span></span></p>

		<div>&nbsp;</div>

								</td>
							</tr>
						</tbody></table>

					</td>
				</tr>
			</tbody>
		</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock">
			<tbody class="mcnFollowBlockOuter">
				<tr>
					<td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
						<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer">
			<tbody><tr>
				<td align="center" style="padding-left:9px;padding-right:9px;">
					<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border: 1px solid #EEEEEE;background-color: #FAFAFA;">
						<tbody><tr>
							<td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
								<table border="0" cellpadding="0" cellspacing="0">
									<tbody><tr>
										<td valign="top">


													<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

														<tbody><tr>
															<td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
																<a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
															</td>
														</tr>


														<tr>
															<td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
																<a href="http://www.facebook.com/carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Facebook</a>
															</td>
														</tr>

													</tbody></table>


										<!--[if gte mso 6]>
										</td>
										<td align="left" valign="top">
										<![endif]-->


													<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

														<tbody><tr>
															<td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
																<a href="http://www.twitter.com/clickgarage_in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-96.png" alt="Twitter" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
															</td>
														</tr>


														<tr>
															<td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
																<a href="http://www.twitter.com/clickgarage_in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Twitter</a>
															</td>
														</tr>

													</tbody></table>


										<!--[if gte mso 6]>
										</td>
										<td align="left" valign="top">
										<![endif]-->


													<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

														<tbody><tr>
															<td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:0; padding-bottom:5px;">
																<a href="http://www.carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
															</td>
														</tr>


														<tr>
															<td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
																<a href="http://www.carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Website</a>
															</td>
														</tr>

													</tbody></table>


										<!--[if gte mso 6]>
										</td>
										<td align="left" valign="top">
										<![endif]-->

										</td>
									</tr>
								</tbody></table>
							</td>
						</tr>
					</tbody></table>
				</td>
			</tr>
		</tbody></table>

					</td>
				</tr>
			</tbody>
		</table></td>
												</tr>
											</table>
											<!-- // END BODY -->
										</td>
									</tr>
									<tr>
										<td align="center" valign="top">
											<!-- BEGIN FOOTER // -->
											<table border="0" cellpadding="0" cellspacing="0" width="600" id="templateFooter">
												<tr>
													<td valign="top" class="footerContainer" style="padding-bottom:9px;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
			<tbody class="mcnTextBlockOuter">
				<tr>
					<td valign="top" class="mcnTextBlockInner">

						<table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
							<tbody><tr>

								<td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

									<em>Copyright (C) 2015 Sui Generis Innovations, All rights reserved.</em><br>
		Email : sales@carcrew.in | Phone No. : +91-7045996415<br>
		<br>
		W-22, Second Floor, Green Park, New Delhi - 110016
								</td>
							</tr>
						</tbody></table>

					</td>
				</tr>
			</tbody>
		</table></td>
												</tr>
											</table>
											<!-- // END FOOTER -->
										</td>
									</tr>
								</table>
								<!-- // END TEMPLATE -->
							</td>
						</tr>
					</table>
				</center>
			</body>
		</html>

		"""
	else:
		print 'coming here'
		html = '<html><body>test1</body></html>'





	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)





	script = MIMEText(html, 'html')

	msg.attach(script)


	smtp_port = '25'
	smtp_do_tls = True

	server = smtplib.SMTP(
		host = smtp_server,
		port = smtp_port,
		timeout = 30
	)
	server.set_debuglevel(10)
	server.starttls()
	server.ehlo()
	server.login(smtp_username, smtp_password)
	server.sendmail(me, you, msg.as_string())


	script = MIMEText(html, 'html')
	msg.attach(script)


	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(path_file, "rb").read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; '+'filename=Report_'+booking_id+'.pdf')

	msg.attach(part)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#     host = smtp_server,
	#     port = smtp_port,
	#     timeout = 30
	# )
	#
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())

def send_feedback_report(to_address,to_name,booking_id,path_file,amount):
	me = from_address
	you = to_address
	booking_id = str(booking_id)
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Order Complete! We'd love your feedback! Booking ID :" + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    	<!-- NAME: 1 COLUMN -->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>*|MC:SUBJECT|*</title>

    <style type="text/css">
		body,#bodyTable,#bodyCell{
			height:100% !important;
			margin:0;
			padding:0;
			width:100% !important;
		}
		table{
			border-collapse:collapse;
		}
		img,a img{
			border:0;
			outline:none;
			text-decoration:none;
		}
		h1,h2,h3,h4,h5,h6{
			margin:0;
			padding:0;
		}
		p{
			margin:1em 0;
			padding:0;
		}
		a{
			word-wrap:break-word;
		}
		.ReadMsgBody{
			width:100%;
		}
		.ExternalClass{
			width:100%;
		}
		.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{
			line-height:100%;
		}
		table,td{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}
		#outlook a{
			padding:0;
		}
		img{
			-ms-interpolation-mode:bicubic;
		}
		body,table,td,p,a,li,blockquote{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}
		#bodyCell{
			padding:20px;
		}
		.mcnImage{
			vertical-align:bottom;
		}
		.mcnTextContent img{
			height:auto !important;
		}
	/*
	@tab Page
	@section background style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		body,#bodyTable{
			/*@editable*/background-color:#F2F2F2;
		}
	/*
	@tab Page
	@section background style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		#bodyCell{
			/*@editable*/border-top:0;
		}
	/*
	@tab Page
	@section email border
	@tip Set the border for your email.
	*/
		#templateContainer{
			/*@editable*/border:0;
		}
	/*
	@tab Page
	@section heading 1
	@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
	@style heading 1
	*/
		h1{
			/*@editable*/color:#606060 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:40px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:-1px;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section heading 2
	@tip Set the styling for all second-level headings in your emails.
	@style heading 2
	*/
		h2{
			/*@editable*/color:#404040 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:26px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:-.75px;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section heading 3
	@tip Set the styling for all third-level headings in your emails.
	@style heading 3
	*/
		h3{
			/*@editable*/color:#606060 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:18px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:-.5px;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section heading 4
	@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
	@style heading 4
	*/
		h4{
			/*@editable*/color:#808080 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:normal;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section preheader style
	@tip Set the background color and borders for your email's preheader area.
	*/
		#templatePreheader{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Preheader
	@section preheader text
	@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
	*/
		.preheaderContainer .mcnTextContent,.preheaderContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:11px;
			/*@editable*/line-height:125%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section preheader link
	@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
	*/
		.preheaderContainer .mcnTextContent a{
			/*@editable*/color:#606060;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Header
	@section header style
	@tip Set the background color and borders for your email's header area.
	*/
		#templateHeader{
			/*@editable*/background-color:#ffffff;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Header
	@section header text
	@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
	*/
		.headerContainer .mcnTextContent,.headerContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:15px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Header
	@section header link
	@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
	*/
		.headerContainer .mcnTextContent a{
			/*@editable*/color:#6DC6DD;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Body
	@section body style
	@tip Set the background color and borders for your email's body area.
	*/
		#templateBody{
			/*@editable*/background-color:#fafafa;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Body
	@section body text
	@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
	*/
		.bodyContainer .mcnTextContent,.bodyContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:15px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Body
	@section body link
	@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
	*/
		.bodyContainer .mcnTextContent a{
			/*@editable*/color:#6DC6DD;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Footer
	@section footer style
	@tip Set the background color and borders for your email's footer area.
	*/
		#templateFooter{
			/*@editable*/background-color:#cccccc;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Footer
	@section footer text
	@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
	*/
		.footerContainer .mcnTextContent,.footerContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:11px;
			/*@editable*/line-height:125%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Footer
	@section footer link
	@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
	*/
		.footerContainer .mcnTextContent a{
			/*@editable*/color:#606060;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	@media only screen and (max-width: 480px){
		body,table,td,p,a,li,blockquote{
			-webkit-text-size-adjust:none !important;
		}

}	@media only screen and (max-width: 480px){
		body{
			width:100% !important;
			min-width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		td[id=bodyCell]{
			padding:10px !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnTextContentContainer]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnBoxedTextContentContainer{
			max-width:100% !important;
			min-width:100% !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcpreview-image-uploader]{
			width:100% !important;
			display:none !important;
		}

}	@media only screen and (max-width: 480px){
		img[class=mcnImage]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnImageGroupContentContainer]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageGroupContent]{
			padding:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageGroupBlockInner]{
			padding-bottom:0 !important;
			padding-top:0 !important;
		}

}	@media only screen and (max-width: 480px){
		tbody[class=mcnImageGroupBlockOuter]{
			padding-bottom:9px !important;
			padding-top:9px !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnCaptionTopContent],table[class=mcnCaptionBottomContent]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnCaptionLeftTextContentContainer],table[class=mcnCaptionRightTextContentContainer],table[class=mcnCaptionLeftImageContentContainer],table[class=mcnCaptionRightImageContentContainer],table[class=mcnImageCardLeftTextContentContainer],table[class=mcnImageCardRightTextContentContainer]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
			padding-right:18px !important;
			padding-left:18px !important;
			padding-bottom:0 !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardBottomImageContent]{
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardTopImageContent]{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
			padding-right:18px !important;
			padding-left:18px !important;
			padding-bottom:0 !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardBottomImageContent]{
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardTopImageContent]{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnCaptionLeftContentOuter] td[class=mcnTextContent],table[class=mcnCaptionRightContentOuter] td[class=mcnTextContent]{
			padding-top:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnCaptionBlockInner] table[class=mcnCaptionTopContent]:last-child td[class=mcnTextContent]{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnBoxedTextContentColumn]{
			padding-left:18px !important;
			padding-right:18px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnTextContent]{
			padding-right:18px !important;
			padding-left:18px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section template width
	@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.
	*/
		table[id=templateContainer],table[id=templatePreheader],table[id=templateHeader],table[id=templateBody],table[id=templateFooter]{
			/*@tab Mobile Styles
@section template width
@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.*/max-width:600px !important;
			/*@editable*/width:100% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 1
	@tip Make the first-level headings larger in size for better readability on small screens.
	*/
		h1{
			/*@editable*/font-size:24px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 2
	@tip Make the second-level headings larger in size for better readability on small screens.
	*/
		h2{
			/*@editable*/font-size:20px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 3
	@tip Make the third-level headings larger in size for better readability on small screens.
	*/
		h3{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 4
	@tip Make the fourth-level headings larger in size for better readability on small screens.
	*/
		h4{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Boxed Text
	@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		table[class=mcnBoxedTextContentContainer] td[class=mcnTextContent],td[class=mcnBoxedTextContentContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Visibility
	@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
	*/
		table[id=templatePreheader]{
			/*@editable*/display:block !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Text
	@tip Make the preheader text larger in size for better readability on small screens.
	*/
		td[class=preheaderContainer] td[class=mcnTextContent],td[class=preheaderContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:115% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Header Text
	@tip Make the header text larger in size for better readability on small screens.
	*/
		td[class=headerContainer] td[class=mcnTextContent],td[class=headerContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Body Text
	@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		td[class=bodyContainer] td[class=mcnTextContent],td[class=bodyContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section footer text
	@tip Make the body content text larger in size for better readability on small screens.
	*/
		td[class=footerContainer] td[class=mcnTextContent],td[class=footerContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:115% !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=footerContainer] a[class=utilityLink]{
			display:block !important;
		}

}</style></head>
    <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                <tr>
                    <td align="center" valign="top" id="bodyCell">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateContainer">
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN PREHEADER // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templatePreheader">
                                        <tr>
                                        	<td valign="top" class="preheaderContainer" style="padding-top:9px;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">

            </td>
        </tr>
    </tbody>
</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END PREHEADER -->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN HEADER // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateHeader">
                                        <tr>
                                            <td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">

</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END HEADER -->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN BODY // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
                                        <tr>
                                            <td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/1b38aeca-cbbb-4104-a3ca-e9e7a841f00a.jpg" width="564" style="max-width:603px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 0px 9px; line-height: normal;" width="564">

        </td>
    </tr>
</tbody></table>

<!--Python-->
<table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
	                                        <tr>
	                                            <td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
	    <tbody class="mcnTextBlockOuter">
	        <tr>
	            <td valign="top" class="mcnTextBlockInner">

	                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
	                    <tbody><tr>

	                        <td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

	                            <h1>Order Complete!</h1>

	<h3><br>
	Booking ID #"""+booking_id+"""</h3>
	&nbsp;

	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Hello """+to_name+"""! Your Carcrew booking is complete. Your total amount paid was """+amount+""". Please find attached a detailed service report. It was a pleasure serving you. Kindly spare some time to share your valuable feedback.</span></span></p>
<!--Python-->

<title>Carcrew Feedback</title>
<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Roboto:400,700">

<link href="/static/forms/client/css/251396771-formview_st_ltr.css" type="text/css" rel="stylesheet">
<style type="text/css">
body {
  background-color: rgb(231,238,247);
  background-image: url('//ssl.gstatic.com/docs/forms/themes/images/v1/0AX42CRMsmRFbUy03NTAzM2Q4My03ODU1LTQ2NzItODI2YS1kZmU5YzdiMzZjOGQ/blue-stripe-bg.png');
  background-repeat: repeat;
  background-position: left top;
}

.ss-form-container, .ss-resp-card {
  background-color: rgb(255,255,255);
}

.ss-footer, .ss-response-footer {
  background-color: rgb(255,255,255);
}

.ss-grid-row-odd {
  background-color: rgb(242,242,242);
}

.ss-form-container, .ss-resp-card {
  border-color: rgb(212,212,212);
}

.ss-form-title {
  text-align: left;
}

.ss-form-title[dir="rtl"] {
  text-align: right;
}

.ss-form-desc {
  text-align: left;
}

.ss-form-desc[dir="rtl"] {
  text-align: right;
}

.ss-header-image-container {
  height: 0;
}

.ss-item {
  font-size: 1.080rem;
}

.ss-choices {
  font-size: 1.000rem;
}

body {
  font-family: "Roboto";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-record-username-message {
  font-family: "Roboto";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-form-title {
  font-family: "Raleway";
  color: rgb(80,80,80);
  font-weight: 300;
  font-size: 2.460rem;
  font-style: normal;
}

.ss-confirmation {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 2.460rem;
  font-style: normal;
}

.ss-page-title, .ss-section-title {
  font-family: "Raleway";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.845rem;
  font-style: normal;
}

.ss-form-desc, .ss-page-description, .ss-section-description {
  font-family: "Roboto";
  color: rgb(140,140,140);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-resp-content {
  font-family: "Roboto";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-q-title {
  font-family: "Roboto";
  padding-top:10px;
  color: rgb(80,80,80);
  font-weight: 700;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-embeddable-object-container .ss-q-title {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 700;
  font-size: 1.845rem;
  font-style: normal;
}

.ss-q-help, .ss-q-time-hint {
  font-family: "Roboto";
  color: rgb(140,140,140);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-choice-label, .video-secondary-text, .ss-gridrow-leftlabel, .ss-gridnumber, .ss-scalenumber, .ss-leftlabel, .ss-rightlabel {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.error-message, .required-message, .ss-required-asterisk {
  font-family: "Roboto";
  color: rgb(196,59,29);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-send-email-receipt {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-password-warning {
  font-family: "Arial";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: italic;
}

.disclaimer {
  font-family: "Arial";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 0.850rem;
  font-style: normal;
}

.ss-footer-content {
  font-family: "Arial";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.progress-label {
  font-family: "Roboto";
  color: rgb(140,140,140);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

a:link {
  color: rgb(0,0,238);
}

a:visited {
  color: rgb(85,26,139);
}

a:active {
  color: rgb(252,0,0);
}

input[type='text'], input:not([type]), textarea {
  font-size: 1.000rem;
}

.error, .required, .errorbox-bad {
  border-color: rgb(196,59,29);
}

.jfk-progressBar-nonBlocking .progress-bar-thumb {
  background-color: rgb(140,140,140);
}

.ss-logo-image {
  background-image: url('//ssl.gstatic.com/docs/forms/forms_logo_2_small_dark.png');
  background-size: 108px 21px;
  width: 108px;
  height: 21px;
}

@media screen and (-webkit-device-pixel-ratio: 2) {
.ss-logo-image {
  background-image: url('//ssl.gstatic.com/docs/forms/forms_logo_2_small_dark_2x.png');
}
}

</style>


<link href="/static/forms/client/css/3145455273-mobile_formview_st_ltr.css" type="text/css" rel="stylesheet" media="screen and (max-device-width: 721px)">

<script type="text/javascript">
          /**
 * @license
 *
 * H5F 1.1.1
 * See https://github.com/ryanseddon/H5F/ for details.
 *
 * Copyright (c) 2013 Ryan Seddon
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */
(function(e,t){"function"==typeof define&&define.amd?define(t):"object"==typeof module&&module.exports?module.exports=t():e.H5F=t()})(this,function(){var e,t,a,i,n,r,l,s,o,u,d,c,v,p,f,m,b,h,g,y,w,C,N,A,E,$,x=document,k=x.createElement("input"),q=/^[a-zA-Z0-9.!#$%&'*+-\/=?\^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,M=/[a-z][\-\.+a-z]*:\/\//i,L=/^(input|select|textarea)$/i;return r=function(e,t){var a=!e.nodeType||!1,i={validClass:"valid",invalidClass:"error",requiredClass:"required",placeholderClass:"placeholder",onSubmit:Function.prototype,onInvalid:Function.prototype};if("object"==typeof t)for(var r in i)t[r]===void 0&&(t[r]=i[r]);if(n=t||i,a)for(var s=0,o=e.length;o>s;s++)l(e[s]);else l(e)},l=function(a){var i,r=a.elements,l=r.length,c=!!a.attributes.novalidate;if(g(a,"invalid",o,!0),g(a,"blur",o,!0),g(a,"input",o,!0),g(a,"keyup",o,!0),g(a,"focus",o,!0),g(a,"change",o,!0),g(a,"click",u,!0),g(a,"submit",function(i){return e=!0,t||c||a.checkValidity()?(n.onSubmit.call(a,i),void 0):(w(i),void 0)},!1),!v())for(a.checkValidity=function(){return d(a)};l--;)i=!!r[l].attributes.required,"fieldset"!==r[l].nodeName.toLowerCase()&&s(r[l])},s=function(e){var t=e,a=h(t),n={type:t.getAttribute("type"),pattern:t.getAttribute("pattern"),placeholder:t.getAttribute("placeholder")},r=/^(email|url)$/i,l=/^(input|keyup)$/i,s=r.test(n.type)?n.type:n.pattern?n.pattern:!1,o=p(t,s),u=m(t,"step"),v=m(t,"min"),b=m(t,"max"),g=!(""===t.validationMessage||void 0===t.validationMessage);t.checkValidity=function(){return d.call(this,t)},t.setCustomValidity=function(e){c.call(t,e)},t.validity={valueMissing:a,patternMismatch:o,rangeUnderflow:v,rangeOverflow:b,stepMismatch:u,customError:g,valid:!(a||o||u||v||b||g)},n.placeholder&&!l.test(i)&&f(t)},o=function(e){var t=C(e)||e,a=/^(input|keyup|focusin|focus|change)$/i,r=/^(submit|image|button|reset)$/i,l=/^(checkbox|radio)$/i,u=!0;!L.test(t.nodeName)||r.test(t.type)||r.test(t.nodeName)||(i=e.type,v()||s(t),t.validity.valid&&(""!==t.value||l.test(t.type))||t.value!==t.getAttribute("placeholder")&&t.validity.valid?(A(t,[n.invalidClass,n.requiredClass]),N(t,n.validClass)):a.test(i)?t.validity.valueMissing&&A(t,[n.requiredClass,n.invalidClass,n.validClass]):t.validity.valueMissing?(A(t,[n.invalidClass,n.validClass]),N(t,n.requiredClass)):t.validity.valid||(A(t,[n.validClass,n.requiredClass]),N(t,n.invalidClass)),"input"===i&&u&&(y(t.form,"keyup",o,!0),u=!1))},d=function(t){var a,i,r,l,s,u=!1;if("form"===t.nodeName.toLowerCase()){a=t.elements;for(var d=0,c=a.length;c>d;d++)i=a[d],r=!!i.attributes.disabled,l=!!i.attributes.required,s=!!i.attributes.pattern,"fieldset"!==i.nodeName.toLowerCase()&&!r&&(l||s&&l)&&(o(i),i.validity.valid||u||(e&&i.focus(),u=!0,n.onInvalid.call(t,i)));return!u}return o(t),t.validity.valid},c=function(e){var t=this;t.validationMessage=e},u=function(e){var a=C(e);a.attributes.formnovalidate&&"submit"===a.type&&(t=!0)},v=function(){return E(k,"validity")&&E(k,"checkValidity")},p=function(e,t){if("email"===t)return!q.test(e.value);if("url"===t)return!M.test(e.value);if(t){var i=e.getAttribute("placeholder"),n=e.value;return a=RegExp("^(?:"+t+")$"),n===i?!1:""===n?!1:!a.test(e.value)}return!1},f=function(e){var t={placeholder:e.getAttribute("placeholder")},a=/^(focus|focusin|submit)$/i,r=/^(input|textarea)$/i,l=/^password$/i,s=!!("placeholder"in k);s||!r.test(e.nodeName)||l.test(e.type)||(""!==e.value||a.test(i)?e.value===t.placeholder&&a.test(i)&&(e.value="",A(e,n.placeholderClass)):(e.value=t.placeholder,g(e.form,"submit",function(){i="submit",f(e)},!0),N(e,n.placeholderClass)))},m=function(e,t){var a=parseInt(e.getAttribute("min"),10)||0,i=parseInt(e.getAttribute("max"),10)||!1,n=parseInt(e.getAttribute("step"),10)||1,r=parseInt(e.value,10),l=(r-a)%n;return h(e)||isNaN(r)?"number"===e.getAttribute("type")?!0:!1:"step"===t?e.getAttribute("step")?0!==l:!1:"min"===t?e.getAttribute("min")?a>r:!1:"max"===t?e.getAttribute("max")?r>i:!1:void 0},b=function(e){var t=!!e.attributes.required;return t?h(e):!1},h=function(e){var t=e.getAttribute("placeholder"),a=/^(checkbox|radio)$/i,i=!!e.attributes.required;return!(!i||""!==e.value&&e.value!==t&&(!a.test(e.type)||$(e)))},g=function(e,t,a,i){E(window,"addEventListener")?e.addEventListener(t,a,i):E(window,"attachEvent")&&window.event!==void 0&&("blur"===t?t="focusout":"focus"===t&&(t="focusin"),e.attachEvent("on"+t,a))},y=function(e,t,a,i){E(window,"removeEventListener")?e.removeEventListener(t,a,i):E(window,"detachEvent")&&window.event!==void 0&&e.detachEvent("on"+t,a)},w=function(e){e=e||window.event,e.stopPropagation&&e.preventDefault?(e.stopPropagation(),e.preventDefault()):(e.cancelBubble=!0,e.returnValue=!1)},C=function(e){return e=e||window.event,e.target||e.srcElement},N=function(e,t){var a;e.className?(a=RegExp("(^|\\s)"+t+"(\\s|$)"),a.test(e.className)||(e.className+=" "+t)):e.className=t},A=function(e,t){var a,i,n="object"==typeof t?t.length:1,r=n;if(e.className)if(e.className===t)e.className="";else for(;n--;)a=RegExp("(^|\\s)"+(r>1?t[n]:t)+"(\\s|$)"),i=e.className.match(a),i&&3===i.length&&(e.className=e.className.replace(a,i[1]&&i[2]?" ":""))},E=function(e,t){var a=typeof e[t],i=RegExp("^function|object$","i");return!!(i.test(a)&&e[t]||"unknown"===a)},$=function(e){for(var t=document.getElementsByName(e.name),a=0;t.length>a;a++)if(t[a].checked)return!0;return!1},{setup:r}});

        </script><style type="text/css"></style>
<link rel="alternate" type="text/xml+oembed" href="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/oembed?url=https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform&amp;format=xml">
<meta property="og:title" content="Carcrew Feedback"><meta property="og:type" content="article"><meta property="og:site_name" content="Google Docs"><meta property="og:url" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?usp=embed_facebook"><meta property="og:image" content="https://lh4.googleusercontent.com/igig_iaW1Fqa1ZIV5gv9sOuTqGxBjfjtATYbPWEI5nGulQ2ngH1Sx07ElxUoW7x5NQc=w1200-h630-p"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:description" content="Help us serve you better!"><meta name="twitter:card" content="player"><meta name="twitter:title" content="Carcrew Feedback"><meta name="twitter:url" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?usp=embed_twitter"><meta name="twitter:image" content="https://lh4.googleusercontent.com/igig_iaW1Fqa1ZIV5gv9sOuTqGxBjfjtATYbPWEI5nGulQ2ngH1Sx07ElxUoW7x5NQc=w435-h251-p-b1-c0x00999999"><meta name="twitter:player:width" content="435"><meta name="twitter:player:height" content="251"><meta name="twitter:player" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?embedded=true&amp;usp=embed_twitter"><meta name="twitter:description" content="Help us serve you better!"><meta name="twitter:site" content="@googledocs">
<style id="style-1-cropbar-clipper">/* Copyright 2014 Evernote Corporation. All rights reserved. */
.en-markup-crop-options {
    top: 18px !important;
    left: 50% !important;
    margin-left: -100px !important;
    width: 200px !important;
    border: 2px rgba(255,255,255,.38) solid !important;
    border-radius: 4px !important;
}

.en-markup-crop-options div div:first-of-type {
    margin-left: 0px !important;
}
</style><style type="text/css" id="GINGER_SOFTWARE_style">.GINGER_SOFTWARE_noMark { background : transparent; }  .GINGER_SOFTWARE_wrapper{ position: absolute; overflow: hidden; margin: 0px; padding: 0px; border: 0px solid transparent } .GINGER_SOFTWARE_contour { position : absolute; margin: 0px; }  .GINGER_SOFTWARE_richText { margin : 0px; padding-bottom: 3px; border-width: 0px; border-color: transparent; display: block; color: transparent; -webkit-text-fill-color: transparent; overflow: hidden; white-space: pre-wrap;}  .GINGER_SOFTWARE_inputWrapper .GINGER_SOFTWARE_richText {position: absolute;}  .GINGER_SOFTWARE_canvas { display:none; background-repeat:no-repeat;}  .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark {border-top-left-radius:2px; border-top-right-radius:2px; border-bottom-right-radius:2px; border-bottom-left-radius:2px;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhFQ0Y2OENGMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhFQ0Y2OEQwMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEVDRjY4Q0QzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEVDRjY4Q0UzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5RRxRxAAAAD0lEQVR42mK48+w7QIABAAVbAroowN08AAAAAElFTkSuQmCC)!important;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark.GINGER_SOFTWARE_synonym {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAKT2lDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjanVNnVFPpFj333vRCS4iAlEtvUhUIIFJCi4AUkSYqIQkQSoghodkVUcERRUUEG8igiAOOjoCMFVEsDIoK2AfkIaKOg6OIisr74Xuja9a89+bN/rXXPues852zzwfACAyWSDNRNYAMqUIeEeCDx8TG4eQuQIEKJHAAEAizZCFz/SMBAPh+PDwrIsAHvgABeNMLCADATZvAMByH/w/qQplcAYCEAcB0kThLCIAUAEB6jkKmAEBGAYCdmCZTAKAEAGDLY2LjAFAtAGAnf+bTAICd+Jl7AQBblCEVAaCRACATZYhEAGg7AKzPVopFAFgwABRmS8Q5ANgtADBJV2ZIALC3AMDOEAuyAAgMADBRiIUpAAR7AGDIIyN4AISZABRG8lc88SuuEOcqAAB4mbI8uSQ5RYFbCC1xB1dXLh4ozkkXKxQ2YQJhmkAuwnmZGTKBNA/g88wAAKCRFRHgg/P9eM4Ors7ONo62Dl8t6r8G/yJiYuP+5c+rcEAAAOF0ftH+LC+zGoA7BoBt/qIl7gRoXgugdfeLZrIPQLUAoOnaV/Nw+H48PEWhkLnZ2eXk5NhKxEJbYcpXff5nwl/AV/1s+X48/Pf14L7iJIEyXYFHBPjgwsz0TKUcz5IJhGLc5o9H/LcL//wd0yLESWK5WCoU41EScY5EmozzMqUiiUKSKcUl0v9k4t8s+wM+3zUAsGo+AXuRLahdYwP2SycQWHTA4vcAAPK7b8HUKAgDgGiD4c93/+8//UegJQCAZkmScQAAXkQkLlTKsz/HCAAARKCBKrBBG/TBGCzABhzBBdzBC/xgNoRCJMTCQhBCCmSAHHJgKayCQiiGzbAdKmAv1EAdNMBRaIaTcA4uwlW4Dj1wD/phCJ7BKLyBCQRByAgTYSHaiAFiilgjjggXmYX4IcFIBBKLJCDJiBRRIkuRNUgxUopUIFVIHfI9cgI5h1xGupE7yAAygvyGvEcxlIGyUT3UDLVDuag3GoRGogvQZHQxmo8WoJvQcrQaPYw2oefQq2gP2o8+Q8cwwOgYBzPEbDAuxsNCsTgsCZNjy7EirAyrxhqwVqwDu4n1Y8+xdwQSgUXACTYEd0IgYR5BSFhMWE7YSKggHCQ0EdoJNwkDhFHCJyKTqEu0JroR+cQYYjIxh1hILCPWEo8TLxB7iEPENyQSiUMyJ7mQAkmxpFTSEtJG0m5SI+ksqZs0SBojk8naZGuyBzmULCAryIXkneTD5DPkG+Qh8lsKnWJAcaT4U+IoUspqShnlEOU05QZlmDJBVaOaUt2ooVQRNY9aQq2htlKvUYeoEzR1mjnNgxZJS6WtopXTGmgXaPdpr+h0uhHdlR5Ol9BX0svpR+iX6AP0dwwNhhWDx4hnKBmbGAcYZxl3GK+YTKYZ04sZx1QwNzHrmOeZD5lvVVgqtip8FZHKCpVKlSaVGyovVKmqpqreqgtV81XLVI+pXlN9rkZVM1PjqQnUlqtVqp1Q61MbU2epO6iHqmeob1Q/pH5Z/YkGWcNMw09DpFGgsV/jvMYgC2MZs3gsIWsNq4Z1gTXEJrHN2Xx2KruY/R27iz2qqaE5QzNKM1ezUvOUZj8H45hx+Jx0TgnnKKeX836K3hTvKeIpG6Y0TLkxZVxrqpaXllirSKtRq0frvTau7aedpr1Fu1n7gQ5Bx0onXCdHZ4/OBZ3nU9lT3acKpxZNPTr1ri6qa6UbobtEd79up+6Ynr5egJ5Mb6feeb3n+hx9L/1U/W36p/VHDFgGswwkBtsMzhg8xTVxbzwdL8fb8VFDXcNAQ6VhlWGX4YSRudE8o9VGjUYPjGnGXOMk423GbcajJgYmISZLTepN7ppSTbmmKaY7TDtMx83MzaLN1pk1mz0x1zLnm+eb15vft2BaeFostqi2uGVJsuRaplnutrxuhVo5WaVYVVpds0atna0l1rutu6cRp7lOk06rntZnw7Dxtsm2qbcZsOXYBtuutm22fWFnYhdnt8Wuw+6TvZN9un2N/T0HDYfZDqsdWh1+c7RyFDpWOt6azpzuP33F9JbpL2dYzxDP2DPjthPLKcRpnVOb00dnF2e5c4PziIuJS4LLLpc+Lpsbxt3IveRKdPVxXeF60vWdm7Obwu2o26/uNu5p7ofcn8w0nymeWTNz0MPIQ+BR5dE/C5+VMGvfrH5PQ0+BZ7XnIy9jL5FXrdewt6V3qvdh7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30N/I/9k/3r/0QCngCUBZwOJgUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSFoyOyQrSH355jOkc5pDoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6RJZE3ptnMU85ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4p3iC+N7F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi/RNtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9MYOSkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo1yoHsmdlV2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5sjxxedsK4xUFK4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWFfevc1+1dT1gvWd+1YfqGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTPZtJm6ebeLZ5bDpaql+aXDm4N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJzs07P1SkVPRU+lQ27tLdtWHX+G7R7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HIw6217nU1R3SPVRSj9Yr60cOxx++/p3vdy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rOEH0x92HWcdL2pCmvKaRptTmvtbYlu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2fyz4ydlZ19fi753GDborZ752PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86X23qdOo8/pPTT8e7nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9/XfFt1+cif9zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/pH1jw9DBY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZfyl5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT0Kf7kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADqYAAAOpgAABdvkl/FRgAAABJJREFUeNpi+P9gEwAAAP//AwAFcwKS3d7BnwAAAABJRU5ErkJggg==)!important;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark.GINGER_SOFTWARE_noSuggestion {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhFQ0Y2OENGMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhFQ0Y2OEQwMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEVDRjY4Q0QzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEVDRjY4Q0UzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5RRxRxAAAAD0lEQVR42mK48+w7QIABAAVbAroowN08AAAAAElFTkSuQmCC)!important;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_mark {position:relative; background-image:none!important;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightLeft { position : absolute; left:-2px; top:0px; bottom:0px; width:2px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightRight { position : absolute; right:-2px; top:0px; bottom:0px; width:2px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightTop { position : absolute; left:0px; right:0px; top:-2px; height:3px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightBottom { position : absolute; left:0px; right:0px; bottom:-2px; height:3px;}</style></head>
<body dir="ltr" class="ss-base-body" ginger_software_stylesheet="true" ginger_software_doc="true"><div itemscope="" itemtype="http://schema.org/CreativeWork/FormObject">
<meta itemprop="name" content="Carcrew Feedback">
<meta itemprop="description" content="Help us serve you better!">

<meta itemprop="url" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform">
<meta itemprop="embedUrl" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?embedded=true">
<meta itemprop="faviconUrl" content="https://ssl.gstatic.com/docs/spreadsheets/forms/favicon_qp2.png">



<div class="ss-form-container"><div class="ss-header-image-container"><div class="ss-header-image-image"><div class="ss-header-image-sizer"></div></div></div>
<div class="ss-top-of-page"><div class="ss-form-heading"><h1 class="ss-form-title" dir="ltr">Carcrew Feedback</h1>
<div class="ss-form-desc ss-no-ignore-whitespace" dir="ltr">Help us serve you better!</div>

<div class="ss-required-asterisk" aria-hidden="true">*Required</div></div></div>
<div class="ss-form"><form action="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/formResponse" method="POST" id="ss-form" target="_self" onsubmit=""><ol role="list" class="ss-question-list" style="padding-left: 0">
<div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1026407056"><div class="ss-q-title">Name
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<input type="text" name="entry.1026407056" value='"""+to_name+"""' class="ss-q-short" id="entry_1026407056" dir="auto" aria-label="Name  " aria-required="true" required="" title="" disabled>
<div class="error-message" id="935836896_errorMessage"></div>

</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-checkbox"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1329036029"><div class="ss-q-title" style="padding-top:10px;">Did the driver/ mechanic reach on promised time?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices ss-choices-required" style="list-style:none; padding-top:10px;" role="group" aria-label="Did the driver/ mechanic reach on promised time?  "><li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.1935106486" value="Yes" id="group_1935106486_1" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> <li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.1935106486" value="No" id="group_1935106486_2" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li></ul>
<div class="error-message" id="1329036029_errorMessage"></div>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-checkbox"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1462549280"><div class="ss-q-title" style="padding-top:10px;">Was the staff courteous in receiving the vehicle?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices ss-choices-required" style="list-style:none; padding-top:10px;" role="group" aria-label="Was the staff courteous in receiving the vehicle?  "><li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.949514215" value="Yes" id="group_949514215_1" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> <li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.949514215" value="No" id="group_949514215_2" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li></ul>
<div class="error-message" id="1462549280_errorMessage"></div>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item  ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1630365110"><div class="ss-q-title" style="padding-top:10px;">How would you rate the quality of the washing and cleaning of your vehicle? (if applicable)
</div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_193013796"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How would you rate the quality of the washing and cleaning of your vehicle? (if applicable)  Select a value from a range from 1,Bad, to 10,Excellent,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="1" id="group_193013796_1" role="radio" class="ss-q-radio" aria-label="1"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="2" id="group_193013796_2" role="radio" class="ss-q-radio" aria-label="2"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="3" id="group_193013796_3" role="radio" class="ss-q-radio" aria-label="3"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="4" id="group_193013796_4" role="radio" class="ss-q-radio" aria-label="4"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="5" id="group_193013796_5" role="radio" class="ss-q-radio" aria-label="5"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="6" id="group_193013796_6" role="radio" class="ss-q-radio" aria-label="6"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="7" id="group_193013796_7" role="radio" class="ss-q-radio" aria-label="7"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="8" id="group_193013796_8" role="radio" class="ss-q-radio" aria-label="8"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="9" id="group_193013796_9" role="radio" class="ss-q-radio" aria-label="9"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="10" id="group_193013796_10" role="radio" class="ss-q-radio" aria-label="10"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Excellent</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1663139288"><div class="ss-q-title" style="padding-top:10px;">How do you rate the overall interaction and the experience?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_1618681913"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How do you rate the overall interaction and the experience?  Select a value from a range from 1,Bad, to 10,Excellent,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="1" id="group_1618681913_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="2" id="group_1618681913_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="3" id="group_1618681913_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="4" id="group_1618681913_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="5" id="group_1618681913_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="6" id="group_1618681913_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="7" id="group_1618681913_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="8" id="group_1618681913_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="9" id="group_1618681913_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="10" id="group_1618681913_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Excellent</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1622944453"><div class="ss-q-title" style="padding-top:10px;">How likely are you to recommend Carcrew services to others?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_787110920"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How likely are you to recommend Carcrew services to others?  Select a value from a range from 1,No, Never, to 10,Yes, Definitely,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">No, Never</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="1" id="group_787110920_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="2" id="group_787110920_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="3" id="group_787110920_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="4" id="group_787110920_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="5" id="group_787110920_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="6" id="group_787110920_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="7" id="group_787110920_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="8" id="group_787110920_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="9" id="group_787110920_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="10" id="group_787110920_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Yes, Definitely</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item  ss-paragraph-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1853312704"><div class="ss-q-title" style="padding-top:10px;">Do you have any additional comments, feedback or ideas to help us improve our services?
</div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<textarea name="entry.1853312704" rows="5" cols="50" class="ss-q-long" id="entry_1853312704" dir="auto" aria-label="Do you have any additional comments, feedback or ideas to help us improve our services?  "></textarea>
<div class="error-message" id="1325539642_errorMessage"></div>

</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item  ss-paragraph-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1390039714"><div class="ss-q-title" style="padding-top:10px;">Please write a testimonial for us. :)
</div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<textarea name="entry.1390039714" rows="5" cols="50" class="ss-q-long" id="entry_1390039714" dir="auto" aria-label="Please write a testimonial for us. :)  "></textarea>
<div class="error-message" id="918343290_errorMessage"></div>

</div></div></div>
<input type="hidden" name="draftResponse" value="[,,&quot;-7794270178595494330&quot;]
">
<input type="hidden" name="pageHistory" value="0">

<input type="hidden" name="fvv" value="0">


<input type="hidden" name="fbzx" value="-7794270178595494330">

<div class="ss-item ss-navigate"><table id="navigation-table"><tbody><tr><td class="ss-form-entry goog-inline-block" id="navigation-buttons" dir="ltr">
<input type="submit" name="submit" value="Submit" id="ss-submit" class="jfk-button jfk-button-action ">
<!-- <div class="ss-password-warning ss-secondary-text">Never submit passwords through Google Forms.</div></td> -->
</tr></tbody></table></div></ol></form></div>

<div class="ss-footer"><div class="ss-attribution"></div>
<div class="ss-legal"><div class="disclaimer-separator"></div>


<br>
</div></div></div></div>

<div id="docs-aria-speakable" class="docs-a11y-ariascreenreader-speakable docs-offscreen" aria-live="assertive" role="region" aria-atomic="" aria-relevant="additions"></div></div>


<script type="text/javascript" src="/static/forms/client/js/3675641127-formviewer_prd.js"></script>
<script type="text/javascript">H5F.setup(document.getElementById('ss-form'));
          _initFormViewer(
            "[100,,[]\n]\n");</script></div><script type="text/javascript">(function () {
        return window.SIG_EXT = {};
      })()</script><iframe frameborder="0" scrolling="no" style="border: 0px; display: none; background-color: transparent;"></iframe><div id="GOOGLE_INPUT_CHEXT_FLAG" style="display: none;" input="null" input_stat="{&quot;tlang&quot;:true,&quot;tsbc&quot;:true,&quot;pun&quot;:true,&quot;mk&quot;:false,&quot;ss&quot;:true}"></div><iframe width="0" height="0" frameborder="0" src="about:blank" id="GINGER_SOFTWARE_bubblesIFrame" scrolling="no" style="border: 0px solid; display: none; position: absolute; z-index: 2147483647; height: 0px; width: 0px; background-color: transparent;"></iframe><div id="GingerWidgetInfo" style="display:none;"></div>


            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer">
    <tbody><tr>
        <td align="center" style="padding-left:9px;padding-right:9px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border: 1px solid #EEEEEE;background-color: #FAFAFA;">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
                        <table border="0" cellpadding="0" cellspacing="0">
                            <tbody><tr>
                                <td valign="top">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->


                                            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

                                                <tbody><tr>
                                                    <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
                                                        <a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
                                                        <a href="http://www.facebook.com/carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;text-decoration: none;line-height: 100%;text-align: center;">Facebook</a>
                                                    </td>
                                                </tr>

                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

                                                <tbody><tr>
                                                    <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
                                                        <a href="http://www.twitter.com/theclickgarage" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-96.png" alt="Twitter" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
                                                        <a href="http://www.twitter.com/theclickgarage" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;text-decoration: none;line-height: 100%;text-align: center;">Twitter</a>
                                                    </td>
                                                </tr>

                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

                                                <tbody><tr>
                                                    <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:0; padding-bottom:5px;">
                                                        <a href="http://www.carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
                                                        <a href="http://www.carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;text-decoration: none;line-height: 100%;text-align: center;">Website</a>
                                                    </td>
                                                </tr>

                                            </tbody></table>



                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END BODY -->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN FOOTER // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateFooter">
                                        <tr>
                                            <td valign="top" class="footerContainer" style="padding-bottom:9px;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

                            <div style="text-align: center;"><em>Copyright (C) 2015 Sui Generis Innovations, All rights reserved.</em><br>
Email : sales@carcrew.in | Phone No. : +91-7045996415<br>
<br>
W-22, Second Floor, Green Park, New Delhi - 110016</div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END FOOTER -->
                                </td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>


	"""


	script = MIMEText(html, 'html')
	msg.attach(script)


	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	# part = MIMEBase('application', "octet-stream")
	server.quit()

def send_feedback(to_address,to_name,booking_id):
	me = from_address
	you = to_address
	booking_id = str(booking_id)
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Order Complete! We'd love your feedback! Booking ID :" + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    	<!-- NAME: 1 COLUMN -->
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>*|MC:SUBJECT|*</title>

    <style type="text/css">
		body,#bodyTable,#bodyCell{
			height:100% !important;
			margin:0;
			padding:0;
			width:100% !important;
		}
		table{
			border-collapse:collapse;
		}
		img,a img{
			border:0;
			outline:none;
			text-decoration:none;
		}
		h1,h2,h3,h4,h5,h6{
			margin:0;
			padding:0;
		}
		p{
			margin:1em 0;
			padding:0;
		}
		a{
			word-wrap:break-word;
		}
		.ReadMsgBody{
			width:100%;
		}
		.ExternalClass{
			width:100%;
		}
		.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{
			line-height:100%;
		}
		table,td{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}
		#outlook a{
			padding:0;
		}
		img{
			-ms-interpolation-mode:bicubic;
		}
		body,table,td,p,a,li,blockquote{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}
		#bodyCell{
			padding:20px;
		}
		.mcnImage{
			vertical-align:bottom;
		}
		.mcnTextContent img{
			height:auto !important;
		}
	/*
	@tab Page
	@section background style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		body,#bodyTable{
			/*@editable*/background-color:#F2F2F2;
		}
	/*
	@tab Page
	@section background style
	@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
	*/
		#bodyCell{
			/*@editable*/border-top:0;
		}
	/*
	@tab Page
	@section email border
	@tip Set the border for your email.
	*/
		#templateContainer{
			/*@editable*/border:0;
		}
	/*
	@tab Page
	@section heading 1
	@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
	@style heading 1
	*/
		h1{
			/*@editable*/color:#606060 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:40px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:-1px;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section heading 2
	@tip Set the styling for all second-level headings in your emails.
	@style heading 2
	*/
		h2{
			/*@editable*/color:#404040 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:26px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:-.75px;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section heading 3
	@tip Set the styling for all third-level headings in your emails.
	@style heading 3
	*/
		h3{
			/*@editable*/color:#606060 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:18px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:-.5px;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Page
	@section heading 4
	@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
	@style heading 4
	*/
		h4{
			/*@editable*/color:#808080 !important;
			display:block;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:16px;
			/*@editable*/font-style:normal;
			/*@editable*/font-weight:bold;
			/*@editable*/line-height:125%;
			/*@editable*/letter-spacing:normal;
			margin:0;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section preheader style
	@tip Set the background color and borders for your email's preheader area.
	*/
		#templatePreheader{
			/*@editable*/background-color:#FFFFFF;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Preheader
	@section preheader text
	@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
	*/
		.preheaderContainer .mcnTextContent,.preheaderContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:11px;
			/*@editable*/line-height:125%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Preheader
	@section preheader link
	@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
	*/
		.preheaderContainer .mcnTextContent a{
			/*@editable*/color:#606060;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Header
	@section header style
	@tip Set the background color and borders for your email's header area.
	*/
		#templateHeader{
			/*@editable*/background-color:#ffffff;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Header
	@section header text
	@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
	*/
		.headerContainer .mcnTextContent,.headerContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:15px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Header
	@section header link
	@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
	*/
		.headerContainer .mcnTextContent a{
			/*@editable*/color:#6DC6DD;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Body
	@section body style
	@tip Set the background color and borders for your email's body area.
	*/
		#templateBody{
			/*@editable*/background-color:#fafafa;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Body
	@section body text
	@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
	*/
		.bodyContainer .mcnTextContent,.bodyContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:15px;
			/*@editable*/line-height:150%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Body
	@section body link
	@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
	*/
		.bodyContainer .mcnTextContent a{
			/*@editable*/color:#6DC6DD;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	/*
	@tab Footer
	@section footer style
	@tip Set the background color and borders for your email's footer area.
	*/
		#templateFooter{
			/*@editable*/background-color:#cccccc;
			/*@editable*/border-top:0;
			/*@editable*/border-bottom:0;
		}
	/*
	@tab Footer
	@section footer text
	@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
	*/
		.footerContainer .mcnTextContent,.footerContainer .mcnTextContent p{
			/*@editable*/color:#606060;
			/*@editable*/font-family:Helvetica;
			/*@editable*/font-size:11px;
			/*@editable*/line-height:125%;
			/*@editable*/text-align:left;
		}
	/*
	@tab Footer
	@section footer link
	@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
	*/
		.footerContainer .mcnTextContent a{
			/*@editable*/color:#606060;
			/*@editable*/font-weight:normal;
			/*@editable*/text-decoration:underline;
		}
	@media only screen and (max-width: 480px){
		body,table,td,p,a,li,blockquote{
			-webkit-text-size-adjust:none !important;
		}

}	@media only screen and (max-width: 480px){
		body{
			width:100% !important;
			min-width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		td[id=bodyCell]{
			padding:10px !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnTextContentContainer]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		.mcnBoxedTextContentContainer{
			max-width:100% !important;
			min-width:100% !important;
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcpreview-image-uploader]{
			width:100% !important;
			display:none !important;
		}

}	@media only screen and (max-width: 480px){
		img[class=mcnImage]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnImageGroupContentContainer]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageGroupContent]{
			padding:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageGroupBlockInner]{
			padding-bottom:0 !important;
			padding-top:0 !important;
		}

}	@media only screen and (max-width: 480px){
		tbody[class=mcnImageGroupBlockOuter]{
			padding-bottom:9px !important;
			padding-top:9px !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnCaptionTopContent],table[class=mcnCaptionBottomContent]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnCaptionLeftTextContentContainer],table[class=mcnCaptionRightTextContentContainer],table[class=mcnCaptionLeftImageContentContainer],table[class=mcnCaptionRightImageContentContainer],table[class=mcnImageCardLeftTextContentContainer],table[class=mcnImageCardRightTextContentContainer]{
			width:100% !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
			padding-right:18px !important;
			padding-left:18px !important;
			padding-bottom:0 !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardBottomImageContent]{
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardTopImageContent]{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardLeftImageContent],td[class=mcnImageCardRightImageContent]{
			padding-right:18px !important;
			padding-left:18px !important;
			padding-bottom:0 !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardBottomImageContent]{
			padding-bottom:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnImageCardTopImageContent]{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		table[class=mcnCaptionLeftContentOuter] td[class=mcnTextContent],table[class=mcnCaptionRightContentOuter] td[class=mcnTextContent]{
			padding-top:9px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnCaptionBlockInner] table[class=mcnCaptionTopContent]:last-child td[class=mcnTextContent]{
			padding-top:18px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnBoxedTextContentColumn]{
			padding-left:18px !important;
			padding-right:18px !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=mcnTextContent]{
			padding-right:18px !important;
			padding-left:18px !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section template width
	@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.
	*/
		table[id=templateContainer],table[id=templatePreheader],table[id=templateHeader],table[id=templateBody],table[id=templateFooter]{
			/*@tab Mobile Styles
@section template width
@tip Make the template fluid for portrait or landscape view adaptability. If a fluid layout doesn't work for you, set the width to 300px instead.*/max-width:600px !important;
			/*@editable*/width:100% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 1
	@tip Make the first-level headings larger in size for better readability on small screens.
	*/
		h1{
			/*@editable*/font-size:24px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 2
	@tip Make the second-level headings larger in size for better readability on small screens.
	*/
		h2{
			/*@editable*/font-size:20px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 3
	@tip Make the third-level headings larger in size for better readability on small screens.
	*/
		h3{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section heading 4
	@tip Make the fourth-level headings larger in size for better readability on small screens.
	*/
		h4{
			/*@editable*/font-size:16px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Boxed Text
	@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		table[class=mcnBoxedTextContentContainer] td[class=mcnTextContent],td[class=mcnBoxedTextContentContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Visibility
	@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
	*/
		table[id=templatePreheader]{
			/*@editable*/display:block !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Preheader Text
	@tip Make the preheader text larger in size for better readability on small screens.
	*/
		td[class=preheaderContainer] td[class=mcnTextContent],td[class=preheaderContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:115% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Header Text
	@tip Make the header text larger in size for better readability on small screens.
	*/
		td[class=headerContainer] td[class=mcnTextContent],td[class=headerContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section Body Text
	@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
	*/
		td[class=bodyContainer] td[class=mcnTextContent],td[class=bodyContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:18px !important;
			/*@editable*/line-height:125% !important;
		}

}	@media only screen and (max-width: 480px){
	/*
	@tab Mobile Styles
	@section footer text
	@tip Make the body content text larger in size for better readability on small screens.
	*/
		td[class=footerContainer] td[class=mcnTextContent],td[class=footerContainer] td[class=mcnTextContent] p{
			/*@editable*/font-size:14px !important;
			/*@editable*/line-height:115% !important;
		}

}	@media only screen and (max-width: 480px){
		td[class=footerContainer] a[class=utilityLink]{
			display:block !important;
		}

}</style></head>
    <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
                <tr>
                    <td align="center" valign="top" id="bodyCell">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateContainer">
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN PREHEADER // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templatePreheader">
                                        <tr>
                                        	<td valign="top" class="preheaderContainer" style="padding-top:9px;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END PREHEADER -->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN HEADER // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateHeader">
                                        <tr>
                                            <td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">

</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END HEADER -->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN BODY // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
                                        <tr>
                                            <td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding:9px;">


<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionBottomContent" width="false">
    <tbody><tr>
        <td class="mcnCaptionBottomImageContent" align="center" valign="top" style="padding:0 9px 9px 9px;">



            <img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/1b38aeca-cbbb-4104-a3ca-e9e7a841f00a.jpg" width="564" style="max-width:603px;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 0px 9px; line-height: normal;" width="564">

        </td>
    </tr>
</tbody></table>

<!--Python-->
<table border="0" cellpadding="0" cellspacing="0" width="600" id="templateBody">
	                                        <tr>
	                                            <td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
	    <tbody class="mcnTextBlockOuter">
	        <tr>
	            <td valign="top" class="mcnTextBlockInner">

	                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
	                    <tbody><tr>

	                        <td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

	                            <h1>Order Complete!</h1>

	<h3><br>
	Booking ID #"""+booking_id+"""</h3>
	&nbsp;

	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Hello """+to_name+"""! Your Carcrew booking is complete. It was a pleasure serving you. Kindly spare some time to share your valuable feedback.</span></span></p>
<!--Python-->

<title>Carcrew Feedback</title>
<link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Roboto:400,700">

<link href="/static/forms/client/css/251396771-formview_st_ltr.css" type="text/css" rel="stylesheet">
<style type="text/css">
body {
  background-color: rgb(231,238,247);
  background-image: url('//ssl.gstatic.com/docs/forms/themes/images/v1/0AX42CRMsmRFbUy03NTAzM2Q4My03ODU1LTQ2NzItODI2YS1kZmU5YzdiMzZjOGQ/blue-stripe-bg.png');
  background-repeat: repeat;
  background-position: left top;
}

.ss-form-container, .ss-resp-card {
  background-color: rgb(255,255,255);
}

.ss-footer, .ss-response-footer {
  background-color: rgb(255,255,255);
}

.ss-grid-row-odd {
  background-color: rgb(242,242,242);
}

.ss-form-container, .ss-resp-card {
  border-color: rgb(212,212,212);
}

.ss-form-title {
  text-align: left;
}

.ss-form-title[dir="rtl"] {
  text-align: right;
}

.ss-form-desc {
  text-align: left;
}

.ss-form-desc[dir="rtl"] {
  text-align: right;
}

.ss-header-image-container {
  height: 0;
}

.ss-item {
  font-size: 1.080rem;
}

.ss-choices {
  font-size: 1.000rem;
}

body {
  font-family: "Roboto";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-record-username-message {
  font-family: "Roboto";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-form-title {
  font-family: "Raleway";
  color: rgb(80,80,80);
  font-weight: 300;
  font-size: 2.460rem;
  font-style: normal;
}

.ss-confirmation {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 2.460rem;
  font-style: normal;
}

.ss-page-title, .ss-section-title {
  font-family: "Raleway";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.845rem;
  font-style: normal;
}

.ss-form-desc, .ss-page-description, .ss-section-description {
  font-family: "Roboto";
  color: rgb(140,140,140);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-resp-content {
  font-family: "Roboto";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-q-title {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 700;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-embeddable-object-container .ss-q-title {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 700;
  font-size: 1.845rem;
  font-style: normal;
}

.ss-q-help, .ss-q-time-hint {
  font-family: "Roboto";
  color: rgb(140,140,140);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-choice-label, .video-secondary-text, .ss-gridrow-leftlabel, .ss-gridnumber, .ss-scalenumber, .ss-leftlabel, .ss-rightlabel {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.error-message, .required-message, .ss-required-asterisk {
  font-family: "Roboto";
  color: rgb(196,59,29);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-send-email-receipt {
  font-family: "Roboto";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-password-warning {
  font-family: "Arial";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: italic;
}

.disclaimer {
  font-family: "Arial";
  color: rgb(119,119,119);
  font-weight: 400;
  font-size: 0.850rem;
  font-style: normal;
}

.ss-footer-content {
  font-family: "Arial";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.progress-label {
  font-family: "Roboto";
  color: rgb(140,140,140);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

a:link {
  color: rgb(0,0,238);
}

a:visited {
  color: rgb(85,26,139);
}

a:active {
  color: rgb(252,0,0);
}

input[type='text'], input:not([type]), textarea {
  font-size: 1.000rem;
}

.error, .required, .errorbox-bad {
  border-color: rgb(196,59,29);
}

.jfk-progressBar-nonBlocking .progress-bar-thumb {
  background-color: rgb(140,140,140);
}

.ss-logo-image {
  background-image: url('//ssl.gstatic.com/docs/forms/forms_logo_2_small_dark.png');
  background-size: 108px 21px;
  width: 108px;
  height: 21px;
}

@media screen and (-webkit-device-pixel-ratio: 2) {
.ss-logo-image {
  background-image: url('//ssl.gstatic.com/docs/forms/forms_logo_2_small_dark_2x.png');
}
}

.ss-q-title{
padding-top:10px;}

</style>


<link href="/static/forms/client/css/3145455273-mobile_formview_st_ltr.css" type="text/css" rel="stylesheet" media="screen and (max-device-width: 721px)">

<script type="text/javascript">
          /**
 * @license
 *
 * H5F 1.1.1
 * See https://github.com/ryanseddon/H5F/ for details.
 *
 * Copyright (c) 2013 Ryan Seddon
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */
(function(e,t){"function"==typeof define&&define.amd?define(t):"object"==typeof module&&module.exports?module.exports=t():e.H5F=t()})(this,function(){var e,t,a,i,n,r,l,s,o,u,d,c,v,p,f,m,b,h,g,y,w,C,N,A,E,$,x=document,k=x.createElement("input"),q=/^[a-zA-Z0-9.!#$%&'*+-\/=?\^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/,M=/[a-z][\-\.+a-z]*:\/\//i,L=/^(input|select|textarea)$/i;return r=function(e,t){var a=!e.nodeType||!1,i={validClass:"valid",invalidClass:"error",requiredClass:"required",placeholderClass:"placeholder",onSubmit:Function.prototype,onInvalid:Function.prototype};if("object"==typeof t)for(var r in i)t[r]===void 0&&(t[r]=i[r]);if(n=t||i,a)for(var s=0,o=e.length;o>s;s++)l(e[s]);else l(e)},l=function(a){var i,r=a.elements,l=r.length,c=!!a.attributes.novalidate;if(g(a,"invalid",o,!0),g(a,"blur",o,!0),g(a,"input",o,!0),g(a,"keyup",o,!0),g(a,"focus",o,!0),g(a,"change",o,!0),g(a,"click",u,!0),g(a,"submit",function(i){return e=!0,t||c||a.checkValidity()?(n.onSubmit.call(a,i),void 0):(w(i),void 0)},!1),!v())for(a.checkValidity=function(){return d(a)};l--;)i=!!r[l].attributes.required,"fieldset"!==r[l].nodeName.toLowerCase()&&s(r[l])},s=function(e){var t=e,a=h(t),n={type:t.getAttribute("type"),pattern:t.getAttribute("pattern"),placeholder:t.getAttribute("placeholder")},r=/^(email|url)$/i,l=/^(input|keyup)$/i,s=r.test(n.type)?n.type:n.pattern?n.pattern:!1,o=p(t,s),u=m(t,"step"),v=m(t,"min"),b=m(t,"max"),g=!(""===t.validationMessage||void 0===t.validationMessage);t.checkValidity=function(){return d.call(this,t)},t.setCustomValidity=function(e){c.call(t,e)},t.validity={valueMissing:a,patternMismatch:o,rangeUnderflow:v,rangeOverflow:b,stepMismatch:u,customError:g,valid:!(a||o||u||v||b||g)},n.placeholder&&!l.test(i)&&f(t)},o=function(e){var t=C(e)||e,a=/^(input|keyup|focusin|focus|change)$/i,r=/^(submit|image|button|reset)$/i,l=/^(checkbox|radio)$/i,u=!0;!L.test(t.nodeName)||r.test(t.type)||r.test(t.nodeName)||(i=e.type,v()||s(t),t.validity.valid&&(""!==t.value||l.test(t.type))||t.value!==t.getAttribute("placeholder")&&t.validity.valid?(A(t,[n.invalidClass,n.requiredClass]),N(t,n.validClass)):a.test(i)?t.validity.valueMissing&&A(t,[n.requiredClass,n.invalidClass,n.validClass]):t.validity.valueMissing?(A(t,[n.invalidClass,n.validClass]),N(t,n.requiredClass)):t.validity.valid||(A(t,[n.validClass,n.requiredClass]),N(t,n.invalidClass)),"input"===i&&u&&(y(t.form,"keyup",o,!0),u=!1))},d=function(t){var a,i,r,l,s,u=!1;if("form"===t.nodeName.toLowerCase()){a=t.elements;for(var d=0,c=a.length;c>d;d++)i=a[d],r=!!i.attributes.disabled,l=!!i.attributes.required,s=!!i.attributes.pattern,"fieldset"!==i.nodeName.toLowerCase()&&!r&&(l||s&&l)&&(o(i),i.validity.valid||u||(e&&i.focus(),u=!0,n.onInvalid.call(t,i)));return!u}return o(t),t.validity.valid},c=function(e){var t=this;t.validationMessage=e},u=function(e){var a=C(e);a.attributes.formnovalidate&&"submit"===a.type&&(t=!0)},v=function(){return E(k,"validity")&&E(k,"checkValidity")},p=function(e,t){if("email"===t)return!q.test(e.value);if("url"===t)return!M.test(e.value);if(t){var i=e.getAttribute("placeholder"),n=e.value;return a=RegExp("^(?:"+t+")$"),n===i?!1:""===n?!1:!a.test(e.value)}return!1},f=function(e){var t={placeholder:e.getAttribute("placeholder")},a=/^(focus|focusin|submit)$/i,r=/^(input|textarea)$/i,l=/^password$/i,s=!!("placeholder"in k);s||!r.test(e.nodeName)||l.test(e.type)||(""!==e.value||a.test(i)?e.value===t.placeholder&&a.test(i)&&(e.value="",A(e,n.placeholderClass)):(e.value=t.placeholder,g(e.form,"submit",function(){i="submit",f(e)},!0),N(e,n.placeholderClass)))},m=function(e,t){var a=parseInt(e.getAttribute("min"),10)||0,i=parseInt(e.getAttribute("max"),10)||!1,n=parseInt(e.getAttribute("step"),10)||1,r=parseInt(e.value,10),l=(r-a)%n;return h(e)||isNaN(r)?"number"===e.getAttribute("type")?!0:!1:"step"===t?e.getAttribute("step")?0!==l:!1:"min"===t?e.getAttribute("min")?a>r:!1:"max"===t?e.getAttribute("max")?r>i:!1:void 0},b=function(e){var t=!!e.attributes.required;return t?h(e):!1},h=function(e){var t=e.getAttribute("placeholder"),a=/^(checkbox|radio)$/i,i=!!e.attributes.required;return!(!i||""!==e.value&&e.value!==t&&(!a.test(e.type)||$(e)))},g=function(e,t,a,i){E(window,"addEventListener")?e.addEventListener(t,a,i):E(window,"attachEvent")&&window.event!==void 0&&("blur"===t?t="focusout":"focus"===t&&(t="focusin"),e.attachEvent("on"+t,a))},y=function(e,t,a,i){E(window,"removeEventListener")?e.removeEventListener(t,a,i):E(window,"detachEvent")&&window.event!==void 0&&e.detachEvent("on"+t,a)},w=function(e){e=e||window.event,e.stopPropagation&&e.preventDefault?(e.stopPropagation(),e.preventDefault()):(e.cancelBubble=!0,e.returnValue=!1)},C=function(e){return e=e||window.event,e.target||e.srcElement},N=function(e,t){var a;e.className?(a=RegExp("(^|\\s)"+t+"(\\s|$)"),a.test(e.className)||(e.className+=" "+t)):e.className=t},A=function(e,t){var a,i,n="object"==typeof t?t.length:1,r=n;if(e.className)if(e.className===t)e.className="";else for(;n--;)a=RegExp("(^|\\s)"+(r>1?t[n]:t)+"(\\s|$)"),i=e.className.match(a),i&&3===i.length&&(e.className=e.className.replace(a,i[1]&&i[2]?" ":""))},E=function(e,t){var a=typeof e[t],i=RegExp("^function|object$","i");return!!(i.test(a)&&e[t]||"unknown"===a)},$=function(e){for(var t=document.getElementsByName(e.name),a=0;t.length>a;a++)if(t[a].checked)return!0;return!1},{setup:r}});

        </script><style type="text/css"></style>
<link rel="alternate" type="text/xml+oembed" href="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/oembed?url=https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform&amp;format=xml">
<meta property="og:title" content="Carcrew Feedback"><meta property="og:type" content="article"><meta property="og:site_name" content="Google Docs"><meta property="og:url" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?usp=embed_facebook"><meta property="og:image" content="https://lh4.googleusercontent.com/igig_iaW1Fqa1ZIV5gv9sOuTqGxBjfjtATYbPWEI5nGulQ2ngH1Sx07ElxUoW7x5NQc=w1200-h630-p"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:description" content="Help us serve you better!"><meta name="twitter:card" content="player"><meta name="twitter:title" content="Carcrew Feedback"><meta name="twitter:url" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?usp=embed_twitter"><meta name="twitter:image" content="https://lh4.googleusercontent.com/igig_iaW1Fqa1ZIV5gv9sOuTqGxBjfjtATYbPWEI5nGulQ2ngH1Sx07ElxUoW7x5NQc=w435-h251-p-b1-c0x00999999"><meta name="twitter:player:width" content="435"><meta name="twitter:player:height" content="251"><meta name="twitter:player" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?embedded=true&amp;usp=embed_twitter"><meta name="twitter:description" content="Help us serve you better!"><meta name="twitter:site" content="@googledocs">
<style id="style-1-cropbar-clipper">/* Copyright 2014 Evernote Corporation. All rights reserved. */
.en-markup-crop-options {
    top: 18px !important;
    left: 50% !important;
    margin-left: -100px !important;
    width: 200px !important;
    border: 2px rgba(255,255,255,.38) solid !important;
    border-radius: 4px !important;
}

.en-markup-crop-options div div:first-of-type {
    margin-left: 0px !important;
}
</style><style type="text/css" id="GINGER_SOFTWARE_style">.GINGER_SOFTWARE_noMark { background : transparent; }  .GINGER_SOFTWARE_wrapper{ position: absolute; overflow: hidden; margin: 0px; padding: 0px; border: 0px solid transparent } .GINGER_SOFTWARE_contour { position : absolute; margin: 0px; }  .GINGER_SOFTWARE_richText { margin : 0px; padding-bottom: 3px; border-width: 0px; border-color: transparent; display: block; color: transparent; -webkit-text-fill-color: transparent; overflow: hidden; white-space: pre-wrap;}  .GINGER_SOFTWARE_inputWrapper .GINGER_SOFTWARE_richText {position: absolute;}  .GINGER_SOFTWARE_canvas { display:none; background-repeat:no-repeat;}  .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark {border-top-left-radius:2px; border-top-right-radius:2px; border-bottom-right-radius:2px; border-bottom-left-radius:2px;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhFQ0Y2OENGMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhFQ0Y2OEQwMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEVDRjY4Q0QzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEVDRjY4Q0UzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5RRxRxAAAAD0lEQVR42mK48+w7QIABAAVbAroowN08AAAAAElFTkSuQmCC)!important;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark.GINGER_SOFTWARE_synonym {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAKT2lDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjanVNnVFPpFj333vRCS4iAlEtvUhUIIFJCi4AUkSYqIQkQSoghodkVUcERRUUEG8igiAOOjoCMFVEsDIoK2AfkIaKOg6OIisr74Xuja9a89+bN/rXXPues852zzwfACAyWSDNRNYAMqUIeEeCDx8TG4eQuQIEKJHAAEAizZCFz/SMBAPh+PDwrIsAHvgABeNMLCADATZvAMByH/w/qQplcAYCEAcB0kThLCIAUAEB6jkKmAEBGAYCdmCZTAKAEAGDLY2LjAFAtAGAnf+bTAICd+Jl7AQBblCEVAaCRACATZYhEAGg7AKzPVopFAFgwABRmS8Q5ANgtADBJV2ZIALC3AMDOEAuyAAgMADBRiIUpAAR7AGDIIyN4AISZABRG8lc88SuuEOcqAAB4mbI8uSQ5RYFbCC1xB1dXLh4ozkkXKxQ2YQJhmkAuwnmZGTKBNA/g88wAAKCRFRHgg/P9eM4Ors7ONo62Dl8t6r8G/yJiYuP+5c+rcEAAAOF0ftH+LC+zGoA7BoBt/qIl7gRoXgugdfeLZrIPQLUAoOnaV/Nw+H48PEWhkLnZ2eXk5NhKxEJbYcpXff5nwl/AV/1s+X48/Pf14L7iJIEyXYFHBPjgwsz0TKUcz5IJhGLc5o9H/LcL//wd0yLESWK5WCoU41EScY5EmozzMqUiiUKSKcUl0v9k4t8s+wM+3zUAsGo+AXuRLahdYwP2SycQWHTA4vcAAPK7b8HUKAgDgGiD4c93/+8//UegJQCAZkmScQAAXkQkLlTKsz/HCAAARKCBKrBBG/TBGCzABhzBBdzBC/xgNoRCJMTCQhBCCmSAHHJgKayCQiiGzbAdKmAv1EAdNMBRaIaTcA4uwlW4Dj1wD/phCJ7BKLyBCQRByAgTYSHaiAFiilgjjggXmYX4IcFIBBKLJCDJiBRRIkuRNUgxUopUIFVIHfI9cgI5h1xGupE7yAAygvyGvEcxlIGyUT3UDLVDuag3GoRGogvQZHQxmo8WoJvQcrQaPYw2oefQq2gP2o8+Q8cwwOgYBzPEbDAuxsNCsTgsCZNjy7EirAyrxhqwVqwDu4n1Y8+xdwQSgUXACTYEd0IgYR5BSFhMWE7YSKggHCQ0EdoJNwkDhFHCJyKTqEu0JroR+cQYYjIxh1hILCPWEo8TLxB7iEPENyQSiUMyJ7mQAkmxpFTSEtJG0m5SI+ksqZs0SBojk8naZGuyBzmULCAryIXkneTD5DPkG+Qh8lsKnWJAcaT4U+IoUspqShnlEOU05QZlmDJBVaOaUt2ooVQRNY9aQq2htlKvUYeoEzR1mjnNgxZJS6WtopXTGmgXaPdpr+h0uhHdlR5Ol9BX0svpR+iX6AP0dwwNhhWDx4hnKBmbGAcYZxl3GK+YTKYZ04sZx1QwNzHrmOeZD5lvVVgqtip8FZHKCpVKlSaVGyovVKmqpqreqgtV81XLVI+pXlN9rkZVM1PjqQnUlqtVqp1Q61MbU2epO6iHqmeob1Q/pH5Z/YkGWcNMw09DpFGgsV/jvMYgC2MZs3gsIWsNq4Z1gTXEJrHN2Xx2KruY/R27iz2qqaE5QzNKM1ezUvOUZj8H45hx+Jx0TgnnKKeX836K3hTvKeIpG6Y0TLkxZVxrqpaXllirSKtRq0frvTau7aedpr1Fu1n7gQ5Bx0onXCdHZ4/OBZ3nU9lT3acKpxZNPTr1ri6qa6UbobtEd79up+6Ynr5egJ5Mb6feeb3n+hx9L/1U/W36p/VHDFgGswwkBtsMzhg8xTVxbzwdL8fb8VFDXcNAQ6VhlWGX4YSRudE8o9VGjUYPjGnGXOMk423GbcajJgYmISZLTepN7ppSTbmmKaY7TDtMx83MzaLN1pk1mz0x1zLnm+eb15vft2BaeFostqi2uGVJsuRaplnutrxuhVo5WaVYVVpds0atna0l1rutu6cRp7lOk06rntZnw7Dxtsm2qbcZsOXYBtuutm22fWFnYhdnt8Wuw+6TvZN9un2N/T0HDYfZDqsdWh1+c7RyFDpWOt6azpzuP33F9JbpL2dYzxDP2DPjthPLKcRpnVOb00dnF2e5c4PziIuJS4LLLpc+Lpsbxt3IveRKdPVxXeF60vWdm7Obwu2o26/uNu5p7ofcn8w0nymeWTNz0MPIQ+BR5dE/C5+VMGvfrH5PQ0+BZ7XnIy9jL5FXrdewt6V3qvdh7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30N/I/9k/3r/0QCngCUBZwOJgUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSFoyOyQrSH355jOkc5pDoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6RJZE3ptnMU85ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4p3iC+N7F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi/RNtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9MYOSkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo1yoHsmdlV2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5sjxxedsK4xUFK4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWFfevc1+1dT1gvWd+1YfqGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTPZtJm6ebeLZ5bDpaql+aXDm4N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJzs07P1SkVPRU+lQ27tLdtWHX+G7R7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HIw6217nU1R3SPVRSj9Yr60cOxx++/p3vdy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rOEH0x92HWcdL2pCmvKaRptTmvtbYlu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2fyz4ydlZ19fi753GDborZ752PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86X23qdOo8/pPTT8e7nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9/XfFt1+cif9zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/pH1jw9DBY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZfyl5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT0Kf7kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADqYAAAOpgAABdvkl/FRgAAABJJREFUeNpi+P9gEwAAAP//AwAFcwKS3d7BnwAAAABJRU5ErkJggg==)!important;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark.GINGER_SOFTWARE_noSuggestion {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhFQ0Y2OENGMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhFQ0Y2OEQwMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEVDRjY4Q0QzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEVDRjY4Q0UzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5RRxRxAAAAD0lEQVR42mK48+w7QIABAAVbAroowN08AAAAAElFTkSuQmCC)!important;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_mark {position:relative; background-image:none!important;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightLeft { position : absolute; left:-2px; top:0px; bottom:0px; width:2px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightRight { position : absolute; right:-2px; top:0px; bottom:0px; width:2px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightTop { position : absolute; left:0px; right:0px; top:-2px; height:3px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightBottom { position : absolute; left:0px; right:0px; bottom:-2px; height:3px;}</style></head>
<body dir="ltr" class="ss-base-body" ginger_software_stylesheet="true" ginger_software_doc="true"><div itemscope="" itemtype="http://schema.org/CreativeWork/FormObject">
<meta itemprop="name" content="Carcrew Feedback">
<meta itemprop="description" content="Help us serve you better!">

<meta itemprop="url" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform">
<meta itemprop="embedUrl" content="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/viewform?embedded=true">
<meta itemprop="faviconUrl" content="https://ssl.gstatic.com/docs/spreadsheets/forms/favicon_qp2.png">




<div class="ss-form-container"><div class="ss-header-image-container"><div class="ss-header-image-image"><div class="ss-header-image-sizer"></div></div></div>
<div class="ss-top-of-page"><div class="ss-form-heading"><h1 class="ss-form-title" dir="ltr">Carcrew Feedback</h1>
<div class="ss-form-desc ss-no-ignore-whitespace" dir="ltr">Help us serve you better!</div>

<div class="ss-required-asterisk" aria-hidden="true"></div></div></div>
<div class="ss-form"><form action="https://docs.google.com/forms/d/1__CYdYzqK2NcZvz4JHCEpVqHQR3A9rRYw_guvXOC-xQ/formResponse" method="POST" id="ss-form" target="_self" onsubmit=""><ol role="list" class="ss-question-list" style="padding-left: 0">
<div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1026407056"><div class="ss-q-title">Booking ID #
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<input type="text" name="entry.1026407056" value=' """+booking_id +"""' class="ss-q-short" readonly id="entry_1026407056" dir="auto" aria-label="Booking ID #  " aria-required="true" required="" title="">
<div class="error-message" id="935836896_errorMessage"></div>
<br>

</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item ss-item-required ss-checkbox"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1329036029"><div class="ss-q-title">1. Did the driver reach on promised time?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices ss-choices-required" style="list-style:none;" role="group" aria-label="Did the driver reach on promised time?  "><li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.1935106486" value="Yes" id="group_1935106486_1" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> <li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.1935106486" value="No" id="group_1935106486_2" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li></ul>
<div class="error-message" id="1329036029_errorMessage"></div>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item ss-item-required ss-checkbox"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1462549280"><div class="ss-q-title">2. Was the driver courteous in receiving the car/bike?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices ss-choices-required" role="group" style="list-style:none;" aria-label="Was the driver courteous in receiving the car/bike?  "><li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.949514215" value="Yes" id="group_949514215_1" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> <li class="ss-choice-item"><label><span class="ss-choice-item-control goog-inline-block"><input type="checkbox" name="entry.949514215" value="No" id="group_949514215_2" role="checkbox" class="ss-q-checkbox" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li></ul>
<div class="error-message" id="1462549280_errorMessage"></div>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1630365110"><div class="ss-q-title">3. How would you rate the quality of the washing and cleaning of your car/bike?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_193013796"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_193013796_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How would you rate the quality of the washing and cleaning of your car/bike?  Select a value from a range of 1,Bad, to 10,Excellent,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="1" id="group_193013796_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="2" id="group_193013796_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="3" id="group_193013796_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="4" id="group_193013796_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="5" id="group_193013796_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="6" id="group_193013796_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="7" id="group_193013796_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="8" id="group_193013796_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="9" id="group_193013796_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.193013796" value="10" id="group_193013796_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Excellent</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1663139288"><div class="ss-q-title">4. How do you rate the overall interaction and the experience?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_1618681913"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1618681913_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How do you rate the overall interaction and the experience?  Select a value from a range of 1,Bad, to 10,Excellent,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="1" id="group_1618681913_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="2" id="group_1618681913_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="3" id="group_1618681913_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="4" id="group_1618681913_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="5" id="group_1618681913_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="6" id="group_1618681913_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="7" id="group_1618681913_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="8" id="group_1618681913_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="9" id="group_1618681913_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1618681913" value="10" id="group_1618681913_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Excellent</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1368084842"><div class="ss-q-title">5. How would you rate the overall pickup and drop experience?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_443851258"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_443851258_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How would you rate the overall pickup and drop experience?  Select a value from a range of 1,Bad, to 10,Excellent,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="1" id="group_443851258_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="2" id="group_443851258_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="3" id="group_443851258_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="4" id="group_443851258_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="5" id="group_443851258_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="6" id="group_443851258_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="7" id="group_443851258_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="8" id="group_443851258_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="9" id="group_443851258_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.443851258" value="10" id="group_443851258_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Excellent</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1622944453"><div class="ss-q-title">6. How likely are you to recommend Carcrew services to others?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_787110920"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_787110920_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How likely are you to recommend Carcrew services to others?  Select a value from a range of 1,No, Never, to 10,Yes, Definitely,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">No, Never</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="1" id="group_787110920_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="2" id="group_787110920_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="3" id="group_787110920_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="4" id="group_787110920_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="5" id="group_787110920_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="6" id="group_787110920_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="7" id="group_787110920_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="8" id="group_787110920_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="9" id="group_787110920_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.787110920" value="10" id="group_787110920_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Yes, Definitely</td></tr></tbody></table>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item  ss-paragraph-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1853312704"><div class="ss-q-title">7. Do you have any additional comments, feedback or ideas to help us improve our services?
</div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<textarea name="entry.1853312704" rows="8" cols="0" class="ss-q-long" id="entry_1853312704" dir="auto" aria-label="Do you have any additional comments, feedback or ideas to help us improve our services?  " style="width: 80%;"></textarea>
<div class="error-message" id="1325539642_errorMessage"></div>
<div class="required-message"></div>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<br>
<div dir="auto" class="ss-item  ss-paragraph-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1390039714"><div class="ss-q-title">8. Please write a testimonial for us. :)
</div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<textarea name="entry.1390039714" rows="8" cols="0" class="ss-q-long" id="entry_1390039714" dir="auto" aria-label="Please write a testimonial for us. :)  " style="width: 80%;"></textarea>
<div class="error-message" id="918343290_errorMessage"></div>
</div></div></div>
<input type="hidden" name="draftResponse" value="[,,&quot;-2376870797102009370&quot;]
">
<input type="hidden" name="pageHistory" value="0">

<input type="hidden" name="fvv" value="0">


<input type="hidden" name="fbzx" value="-2376870797102009370">

<div class="ss-item ss-navigate"><table id="navigation-table"><tbody><tr><td class="ss-form-entry goog-inline-block" id="navigation-buttons" dir="ltr">
<input type="submit" name="submit" value="Submit" id="ss-submit" class="jfk-button jfk-button-action ">
</td>
</tr></tbody></table></div></ol></form></div>
<div class="ss-footer"><div class="ss-attribution"></div>
<div class="ss-legal"><div class="disclaimer-separator"></div>


<br>
</div></div></div></div>

<div id="docs-aria-speakable" class="docs-a11y-ariascreenreader-speakable docs-offscreen" aria-live="assertive" role="region" aria-atomic="" aria-relevant="additions"></div></div>


<script type="text/javascript" src="/static/forms/client/js/3675641127-formviewer_prd.js"></script>
<script type="text/javascript">H5F.setup(document.getElementById('ss-form'));
          _initFormViewer(
            "[100,,[]\n]\n");</script></div><script type="text/javascript">(function () {
        return window.SIG_EXT = {};
      })()</script><iframe frameborder="0" scrolling="no" style="border: 0px; display: none; background-color: transparent;"></iframe><div id="GOOGLE_INPUT_CHEXT_FLAG" style="display: none;" input="null" input_stat="{&quot;tlang&quot;:true,&quot;tsbc&quot;:true,&quot;pun&quot;:true,&quot;mk&quot;:false,&quot;ss&quot;:true}"></div><iframe width="0" height="0" frameborder="0" src="about:blank" id="GINGER_SOFTWARE_bubblesIFrame" scrolling="no" style="border: 0px solid; display: none; position: absolute; z-index: 2147483647; height: 0px; width: 0px; background-color: transparent;"></iframe><div id="GingerWidgetInfo" style="display:none;"></div>


            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer">
    <tbody><tr>
        <td align="center" style="padding-left:9px;padding-right:9px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border: 1px solid #EEEEEE;background-color: #FAFAFA;">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
                        <table border="0" cellpadding="0" cellspacing="0">
                            <tbody><tr>
                                <td valign="top">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->


                                            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

                                                <tbody><tr>
                                                    <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
                                                        <a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
                                                        <a href="http://www.facebook.com/carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;text-decoration: none;line-height: 100%;text-align: center;">Facebook</a>
                                                    </td>
                                                </tr>

                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

                                                <tbody><tr>
                                                    <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:10px; padding-bottom:5px;">
                                                        <a href="http://www.twitter.com/theclickgarage" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-96.png" alt="Twitter" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
                                                        <a href="http://www.twitter.com/theclickgarage" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;text-decoration: none;line-height: 100%;text-align: center;">Twitter</a>
                                                    </td>
                                                </tr>

                                            </tbody></table>



                                            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnFollowStacked">

                                                <tbody><tr>
                                                    <td align="center" valign="top" class="mcnFollowIconContent" style="padding-right:0; padding-bottom:5px;">
                                                        <a href="http://www.CarCrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
                                                        <a href="http://www.Carcrew.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;text-decoration: none;line-height: 100%;text-align: center;">Website</a>
                                                    </td>
                                                </tr>

                                            </tbody></table>



                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END BODY -->
                                </td>
                            </tr>
                            <tr>
                                <td align="center" valign="top">
                                    <!-- BEGIN FOOTER // -->
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateFooter">
                                        <tr>
                                            <td valign="top" class="footerContainer" style="padding-bottom:9px;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="600" class="mcnTextContentContainer">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

                            <div style="text-align: center;"><em>Copyright (C) 2015 Sui Generis Innovations, All rights reserved.</em><br>
Email : sales@carcrew.in | Phone No. : +91-7045996415<br>
<br>
W-22, Second Floor, Green Park, New Delhi - 110016</div>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
                                        </tr>
                                    </table>
                                    <!-- // END FOOTER -->
                                </td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>


	"""
	# part.set_payload(open(path_file, "rb").read())
	# Encoders.encode_base64(part)
	# part.add_header('Content-Disposition', 'attachment; '+'filename=Invoice_'+booking_id+'.pdf')
	#
	# msg.attach(part)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	# 	host = smtp_server,
	# 	port = smtp_port,
	# 	timeout = 30
	# )
	#
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())



def send_booking_final(username,useremail,userphone,time_start,date,booking_id,html_script):
	send_booking_details(booking_mail,booking_id,html_script)
	send_booking_email_pick(useremail,username,time_start,date,booking_id)
	send_booking_sms(username, userphone, date, time_start, booking_id)

def send_booking_final_guest(username,useremail,userphone,time_start,date,booking_id,html_script,sms):
	send_booking_details(booking_mail,booking_id,html_script)
	if sms == "Yes" :
		send_booking_email_pick(useremail,username,time_start,date,booking_id)
		send_booking_sms(username, userphone, date, time_start, booking_id)




def send_booking_final_pick(username,useremail,userphone,time_start,date,booking_id,html_script):
	send_booking_details(booking_mail,booking_id,html_script)
	send_booking_email_pick(useremail,username,time_start,date,booking_id)
	send_booking_sms(username, userphone, date, time_start, booking_id)

def send_booking_final_doorstep(username,useremail,userphone,time_start,date,booking_id,html_script):
	send_booking_details(booking_mail,booking_id,html_script)
	send_booking_email_doorstep(useremail,username,time_start,date,booking_id)
	send_booking_sms(username, userphone, date, time_start, booking_id)

def send_cancel_final(username,useremail,booking_id):
	send_cancel_email(useremail,username,booking_id)
	send_booking_details(booking_mail,booking_id,"Booking Cancelled")

def send_order_complete(username,userphone,useremail,booking_id):
	# send_postdrop(username,userphone,booking_id)
	send_feedback(useremail,username,booking_id)

#send_order_complete("Bhuvan","9953008804","bhuvan.batra@gmail.com","001")


# _sms("Rajeev", "8447021642", "29-10-2015", "10:00AM", "0001")
def send_booking_details(to_address,booking_id,html_script):
	me = from_address
	you = to_address
	booking_id = str(booking_id)
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Booking! Booking ID :" + booking_id
	msg['From'] = me
	msg['To'] = ', '.join(you)


	script = MIMEText(html_script, 'html')
	msg.attach(script)

	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	#part = MIMEBase('application', "octet-stream")
	#part.set_payload(open(path_file, "rb").read())
	#Encoders.encode_base64(part)
	#part.add_header('Content-Disposition', 'attachment; '+'filename=details_'+booking_id+'.csv')
	#
	#msg.attach(part)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#     host = smtp_server,
	#     port = smtp_port,
	#     timeout = 30
	# )
	#
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())


def send_contact_mail(name,phone,content):
	me = "info@clickgarage.in"
	you = staffmails
	# booking_id = str(booking_id)
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Contact Mail"
	msg['From'] = me
	msg['To'] = ', '.join(you)

	message = "Name: " + name + " | Phone: " + phone + " | Message : " + content
	script = MIMEText(message, 'html')
	msg.attach(script)

	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	#part = MIMEBase('application', "octet-stream")
	#part.set_payload(open(path_file, "rb").read())
	#Encoders.encode_base64(part)
	#part.add_header('Content-Disposition', 'attachment; '+'filename=details_'+booking_id+'.csv')
	#
	#msg.attach(part)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#     host = smtp_server,
	#     port = smtp_port,
	#     timeout = 30
	# )
	#
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())


def send_signup_mail(name,phone,email_id):
	me = "info@clickgarage.in"
	you = staffmails
	# booking_id = str(booking_id)
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New User SignUp"
	msg['From'] = me
	msg['To'] = ', '.join(you)

	message = "Name: " + name + " | Phone: " + phone + " | Email : " + email_id
	script = MIMEText(message, 'html')
	msg.attach(script)

	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	#part = MIMEBase('application', "octet-stream")
	#part.set_payload(open(path_file, "rb").read())
	#Encoders.encode_base64(part)
	#part.add_header('Content-Disposition', 'attachment; '+'filename=details_'+booking_id+'.csv')
	#
	#msg.attach(part)


	# smtp_port = '25'
	# smtp_do_tls = True
	#
	# server = smtplib.SMTP(
	#     host = smtp_server,
	#     port = smtp_port,
	#     timeout = 30
	# )
	#
	# server.set_debuglevel(10)
	# server.starttls()
	# server.ehlo()
	# server.login(smtp_username, smtp_password)
	# server.sendmail(me, you, msg.as_string())
	# server.quit()
	conn = boto.ses.connect_to_region('us-west-2',aws_access_key_id='AKIAJNAYBONVQTNTSLZQ',aws_secret_access_key='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')
	result = conn.send_raw_email(msg.as_string())


def send_adwords_mail(name,phone,service,definition):
	me = "info@clickgarage.in"
	you = staffmails
	# booking_id = str(booking_id)
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Service Request"
	msg['From'] = me
	msg['To'] = ', '.join(you)

	message = "Name: " + name + " | Phone: " + phone + " | Service : " + service + " | Definition : " + definition
	script = MIMEText(message, 'html')
	msg.attach(script)

	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	#part = MIMEBase('application', "octet-stream")
	#part.set_payload(open(path_file, "rb").read())
	#Encoders.encode_base64(part)
	#part.add_header('Content-Disposition', 'attachment; '+'filename=details_'+booking_id+'.csv')
	#
	#msg.attach(part)


	smtp_port = '25'
	smtp_do_tls = True

	server = smtplib.SMTP(
		host = smtp_server,
		port = smtp_port,
		timeout = 30
	)

	server.set_debuglevel(10)
	server.starttls()
	server.ehlo()
	server.login(smtp_username, smtp_password)
	server.sendmail(me, you, msg.as_string())
	server.quit()


def send_mail(server_name,port,username,password,fromadd,toadd,subject,text):
	msg = 'Subject: %s\n\n%s' % (subject, text)
	#Change according to your settings
	smtp_server = server_name
	smtp_username = username
	smtp_password = password
	smtp_port = port
	smtp_do_tls = True

	server = smtplib.SMTP(
		host = smtp_server,
		port = smtp_port,
		timeout = 30
	)
	server.set_debuglevel(10)
	server.starttls()
	server.ehlo()
	server.login(smtp_username, smtp_password)
	server.sendmail(fromadd, toadd, msg)


def send_mail_coupon(to_address,wash,bike,service):
	me = from_address
	you = to_address

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Carcrew - Your Car and Bike Care Made Hassle Free"
	msg['From'] = me
	msg['To'] = you

	html = """<!doctype html>
	<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
		<head>
			<!-- NAME: 1 COLUMN - BANDED -->
			<!--[if gte mso 15]>
			<xml>
				<o:OfficeDocumentSettings>
				<o:AllowPNG/>
				<o:PixelsPerInch>96</o:PixelsPerInch>
				</o:OfficeDocumentSettings>
			</xml>
			<![endif]-->
			<meta charset="UTF-8">
			<meta http-equiv="X-UA-Compatible" content="IE=edge">
			<meta name="viewport" content="width=device-width, initial-scale=1">
			<title>*|MC:SUBJECT|*</title>

		<style type="text/css">
			p{
				margin:10px 0;
				padding:0;
			}
			table{
				border-collapse:collapse;
			}
			h1,h2,h3,h4,h5,h6{
				display:block;
				margin:0;
				padding:0;
			}
			img,a img{
				border:0;
				height:auto;
				outline:none;
				text-decoration:none;
			}
			body,#bodyTable,#bodyCell{
				height:100%;
				margin:0;
				padding:0;
				width:100%;
			}
			#outlook a{
				padding:0;
			}
			img{
				-ms-interpolation-mode:bicubic;
			}
			table{
				mso-table-lspace:0pt;
				mso-table-rspace:0pt;
			}
			.ReadMsgBody{
				width:100%;
			}
			.ExternalClass{
				width:100%;
			}
			p,a,li,td,blockquote{
				mso-line-height-rule:exactly;
			}
			a[href^=tel],a[href^=sms]{
				color:inherit;
				cursor:default;
				text-decoration:none;
			}
			p,a,li,td,body,table,blockquote{
				-ms-text-size-adjust:100%;
				-webkit-text-size-adjust:100%;
			}
			.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{
				line-height:100%;
			}
			a[x-apple-data-detectors]{
				color:inherit !important;
				text-decoration:none !important;
				font-size:inherit !important;
				font-family:inherit !important;
				font-weight:inherit !important;
				line-height:inherit !important;
			}
			.templateContainer{
				max-width:600px !important;
			}
			a.mcnButton{
				display:block;
			}
			.mcnImage{
				vertical-align:bottom;
			}
			.mcnTextContent{
				word-break:break-word;
			}
			.mcnTextContent img{
				height:auto !important;
			}
			.mcnDividerBlock{
				table-layout:fixed !important;
			}
		/*
		@tab Page
		@section Background Style
		@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
		*/
			body,#bodyTable{
				/*@editable*/background-color:#FAFAFA;
			}
		/*
		@tab Page
		@section Background Style
		@tip Set the background color and top border for your email. You may want to choose colors that match your company's branding.
		*/
			#bodyCell{
				/*@editable*/border-top:0;
			}
		/*
		@tab Page
		@section Heading 1
		@tip Set the styling for all first-level headings in your emails. These should be the largest of your headings.
		@style heading 1
		*/
			h1{
				/*@editable*/color:#202020;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:26px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:normal;
				/*@editable*/text-align:left;
			}
		/*
		@tab Page
		@section Heading 2
		@tip Set the styling for all second-level headings in your emails.
		@style heading 2
		*/
			h2{
				/*@editable*/color:#202020;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:22px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:normal;
				/*@editable*/text-align:left;
			}
		/*
		@tab Page
		@section Heading 3
		@tip Set the styling for all third-level headings in your emails.
		@style heading 3
		*/
			h3{
				/*@editable*/color:#202020;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:20px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:normal;
				/*@editable*/text-align:left;
			}
		/*
		@tab Page
		@section Heading 4
		@tip Set the styling for all fourth-level headings in your emails. These should be the smallest of your headings.
		@style heading 4
		*/
			h4{
				/*@editable*/color:#202020;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:18px;
				/*@editable*/font-style:normal;
				/*@editable*/font-weight:bold;
				/*@editable*/line-height:125%;
				/*@editable*/letter-spacing:normal;
				/*@editable*/text-align:left;
			}
		/*
		@tab Preheader
		@section Preheader Style
		@tip Set the background color and borders for your email's preheader area.
		*/
			#templatePreheader{
				/*@editable*/background-color:#FAFAFA;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
				/*@editable*/padding-top:9px;
				/*@editable*/padding-bottom:9px;
			}
		/*
		@tab Preheader
		@section Preheader Text
		@tip Set the styling for your email's preheader text. Choose a size and color that is easy to read.
		*/
			#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{
				/*@editable*/color:#656565;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:12px;
				/*@editable*/line-height:150%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Preheader
		@section Preheader Link
		@tip Set the styling for your email's preheader links. Choose a color that helps them stand out from your text.
		*/
			#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{
				/*@editable*/color:#656565;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		/*
		@tab Header
		@section Header Style
		@tip Set the background color and borders for your email's header area.
		*/
			#templateHeader{
				/*@editable*/background-color:#FFFFFF;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
				/*@editable*/padding-top:9px;
				/*@editable*/padding-bottom:0;
			}
		/*
		@tab Header
		@section Header Text
		@tip Set the styling for your email's header text. Choose a size and color that is easy to read.
		*/
			#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{
				/*@editable*/color:#202020;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:16px;
				/*@editable*/line-height:150%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Header
		@section Header Link
		@tip Set the styling for your email's header links. Choose a color that helps them stand out from your text.
		*/
			#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{
				/*@editable*/color:#2BAADF;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		/*
		@tab Body
		@section Body Style
		@tip Set the background color and borders for your email's body area.
		*/
			#templateBody{
				/*@editable*/background-color:#FFFFFF;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
				/*@editable*/padding-top:9px;
				/*@editable*/padding-bottom:9px;
			}
		/*
		@tab Body
		@section Body Text
		@tip Set the styling for your email's body text. Choose a size and color that is easy to read.
		*/
			#templateBody .mcnTextContent,#templateBody .mcnTextContent p{
				/*@editable*/color:#202020;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:16px;
				/*@editable*/line-height:150%;
				/*@editable*/text-align:left;
			}
		/*
		@tab Body
		@section Body Link
		@tip Set the styling for your email's body links. Choose a color that helps them stand out from your text.
		*/
			#templateBody .mcnTextContent a,#templateBody .mcnTextContent p a{
				/*@editable*/color:#2BAADF;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		/*
		@tab Footer
		@section Footer Style
		@tip Set the background color and borders for your email's footer area.
		*/
			#templateFooter{
				/*@editable*/background-color:#FAFAFA;
				/*@editable*/border-top:0;
				/*@editable*/border-bottom:0;
				/*@editable*/padding-top:9px;
				/*@editable*/padding-bottom:9px;
			}
		/*
		@tab Footer
		@section Footer Text
		@tip Set the styling for your email's footer text. Choose a size and color that is easy to read.
		*/
			#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{
				/*@editable*/color:#656565;
				/*@editable*/font-family:Helvetica;
				/*@editable*/font-size:12px;
				/*@editable*/line-height:150%;
				/*@editable*/text-align:center;
			}
		/*
		@tab Footer
		@section Footer Link
		@tip Set the styling for your email's footer links. Choose a color that helps them stand out from your text.
		*/
			#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{
				/*@editable*/color:#656565;
				/*@editable*/font-weight:normal;
				/*@editable*/text-decoration:underline;
			}
		@media only screen and (min-width:768px){
			.templateContainer{
				width:600px !important;
			}

	}	@media only screen and (max-width: 480px){
			body,table,td,p,a,li,blockquote{
				-webkit-text-size-adjust:none !important;
			}

	}	@media only screen and (max-width: 480px){
			body{
				width:100% !important;
				min-width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			#bodyCell{
				padding-top:10px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImage{
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnCaptionTopContent,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{
				max-width:100% !important;
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnBoxedTextContentContainer{
				min-width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImageGroupContent{
				padding:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{
				padding-top:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{
				padding-top:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImageCardBottomImageContent{
				padding-bottom:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImageGroupBlockInner{
				padding-top:0 !important;
				padding-bottom:0 !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImageGroupBlockOuter{
				padding-top:9px !important;
				padding-bottom:9px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnTextContent,.mcnBoxedTextContentColumn{
				padding-right:18px !important;
				padding-left:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{
				padding-right:18px !important;
				padding-bottom:0 !important;
				padding-left:18px !important;
			}

	}	@media only screen and (max-width: 480px){
			.mcpreview-image-uploader{
				display:none !important;
				width:100% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Heading 1
		@tip Make the first-level headings larger in size for better readability on small screens.
		*/
			h1{
				/*@editable*/font-size:22px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Heading 2
		@tip Make the second-level headings larger in size for better readability on small screens.
		*/
			h2{
				/*@editable*/font-size:20px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Heading 3
		@tip Make the third-level headings larger in size for better readability on small screens.
		*/
			h3{
				/*@editable*/font-size:18px !important;
				/*@editable*/line-height:125% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Heading 4
		@tip Make the fourth-level headings larger in size for better readability on small screens.
		*/
			h4{
				/*@editable*/font-size:16px !important;
				/*@editable*/line-height:150% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Boxed Text
		@tip Make the boxed text larger in size for better readability on small screens. We recommend a font size of at least 16px.
		*/
			.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{
				/*@editable*/font-size:14px !important;
				/*@editable*/line-height:150% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Preheader Visibility
		@tip Set the visibility of the email's preheader on small screens. You can hide it to save space.
		*/
			#templatePreheader{
				/*@editable*/display:block !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Preheader Text
		@tip Make the preheader text larger in size for better readability on small screens.
		*/
			#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{
				/*@editable*/font-size:14px !important;
				/*@editable*/line-height:150% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Header Text
		@tip Make the header text larger in size for better readability on small screens.
		*/
			#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{
				/*@editable*/font-size:16px !important;
				/*@editable*/line-height:150% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Body Text
		@tip Make the body text larger in size for better readability on small screens. We recommend a font size of at least 16px.
		*/
			#templateBody .mcnTextContent,#templateBody .mcnTextContent p{
				/*@editable*/font-size:16px !important;
				/*@editable*/line-height:150% !important;
			}

	}	@media only screen and (max-width: 480px){
		/*
		@tab Mobile Styles
		@section Footer Text
		@tip Make the footer content text larger in size for better readability on small screens.
		*/
			#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{
				/*@editable*/font-size:14px !important;
				/*@editable*/line-height:150% !important;
			}

	}</style></head>
		<body>
			<center>
				<table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
					<tr>
						<td align="center" valign="top" id="bodyCell">
							<!-- BEGIN TEMPLATE // -->
							<table border="0" cellpadding="0" cellspacing="0" width="100%">
								<tr>
									<td align="center" valign="top" id="templatePreheader">
										<!--[if gte mso 9]>
										<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
										<tr>
										<td align="center" valign="top" width="600" style="width:600px;">
										<![endif]-->
										<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
											<tr>
												<td valign="top" class="preheaderContainer"></td>
											</tr>
										</table>
										<!--[if gte mso 9]>
										</td>
										</tr>
										</table>
										<![endif]-->
									</td>
								</tr>
								<tr>
									<td align="center" valign="top" id="templateHeader">
										<!--[if gte mso 9]>
										<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
										<tr>
										<td align="center" valign="top" width="600" style="width:600px;">
										<![endif]-->
										<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
											<tr>
												<td valign="top" class="headerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
		<tbody class="mcnImageBlockOuter">
				<tr>
					<td valign="top" style="padding:9px" class="mcnImageBlockInner">
						<table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
							<tbody><tr>
								<td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">


											<img align="center" alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/fec934b8-4c3d-411c-99d8-c1cdcf5a11ce.png" width="544" style="max-width:544px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">


								</td>
							</tr>
						</tbody></table>
					</td>
				</tr>
		</tbody>
	</table></td>
											</tr>
										</table>
										<!--[if gte mso 9]>
										</td>
										</tr>
										</table>
										<![endif]-->
									</td>
								</tr>
								<tr>
									<td align="center" valign="top" id="templateBody">
										<!--[if gte mso 9]>
										<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
										<tr>
										<td align="center" valign="top" width="600" style="width:600px;">
										<![endif]-->
										<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
											<tr>
												<td valign="top" class="bodyContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
		<tbody class="mcnTextBlockOuter">
			<tr>
				<td valign="top" class="mcnTextBlockInner">

					<table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnTextContentContainer">
						<tbody><tr>

							<td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

								<h1><span style="font-size:18px">Carcrew</span></h1>

	<p style="box-sizing: border-box;margin: 0px 0px 27px;color: #565656;font-family: 'Source Sans Pro', sans-serif;font-size: 14px;line-height: 23.1px;"><span style="box-sizing:border-box">We are an online one-stop-shop which you can go to for any car or bike related&nbsp;service, be it regular maintenance, exterior detailing, repairs, or roadside assistance. You can select from, both authorized as well our&nbsp;standardized multi-brand workshops.<br>
	<br>
	<span style="color:#000000"><span style="font-size:18px"><strong>How you can book?</strong></span></span><br>
	Go to our android app&nbsp;or website&nbsp;and follow 3 easy steps:</span></p>

	<ol style="box-sizing: border-box;margin-top: 0px;margin-bottom: 27px;color: #565656;font-family: 'Source Sans Pro', sans-serif;font-size: 14px;line-height: 23.1px;">
		<li style="box-sizing: border-box;"><span style="box-sizing:border-box">Browse through our services/products and select what you need</span></li>
		<li style="box-sizing: border-box;"><span style="box-sizing:border-box">Compare vendors and their prices and select the one that fits your need the best</span></li>
		<li style="box-sizing: border-box;"><span style="box-sizing:border-box">Book a time slot as per your convenience. Then sit back and relax</span></li>
	</ol>

							</td>
						</tr>
					</tbody></table>

				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnButtonBlock" style="min-width:100%;">
		<tbody class="mcnButtonBlockOuter">
			<tr>
				<td style="padding-top:0; padding-right:18px; padding-bottom:18px; padding-left:18px;" valign="top" align="center" class="mcnButtonBlockInner">
					<table border="0" cellpadding="0" cellspacing="0" class="mcnButtonContentContainer" style="border-collapse: separate !important;border-radius: 3px;background-color: #2BAADF;">
						<tbody>
							<tr>
								<td align="center" valign="middle" class="mcnButtonContent" style="font-family: Arial; font-size: 16px; padding: 15px;">
									<a class="mcnButton " title="Book Now" href="http://www.carcrew.in" target="_blank" style="font-weight: bold;letter-spacing: normal;line-height: 100%;text-align: center;text-decoration: none;color: #FFFFFF;">Book Now</a>
								</td>
							</tr>
						</tbody>
					</table>
				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
		<tbody class="mcnImageBlockOuter">
				<tr>
					<td valign="top" style="padding:9px" class="mcnImageBlockInner">
						<table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
							<tbody><tr>
								<td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">

										<a href="https://play.google.com/store/apps/details?id=innovations.generis.sui.clickgarage" title="" class="" target="_blank">
											<img align="center" alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/485b9e78-9bd8-4841-8714-f5b09a207c6f.png" width="183" style="max-width:183px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">
										</a>

								</td>
							</tr>
						</tbody></table>
					</td>
				</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
		<tbody class="mcnDividerBlockOuter">
			<tr>
				<td class="mcnDividerBlockInner" style="min-width:100%; padding:18px;">
					<table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top-width: 2px;border-top-style: solid;border-top-color: #EAEAEA;">
						<tbody><tr>
							<td>
								<span></span>
							</td>
						</tr>
					</tbody></table>
	<!--
					<td class="mcnDividerBlockInner" style="padding: 18px;">
					<hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
	-->
				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock">
		<tbody class="mcnImageCardBlockOuter">
			<tr>
				<td class="mcnImageCardBlockInner" valign="top" style="padding-top:9px; padding-right:18px; padding-bottom:9px; padding-left:18px;">

	<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;">
		<tbody><tr>
			<td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top:0px; padding-right:0px; padding-bottom:0; padding-left:0px;">


				<a href="http://www.carcrew.in" title="" class="" target="_blank">


				<img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/e5129954-b32c-4e65-8c75-bb5d23c446e5.jpg" width="564" style="max-width:640px;" class="mcnImage">
				</a>

			</td>
		</tr>
		<tr>
			<td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;" width="546">
				<span style="font-size:12px">Use coupon code '"""+ wash +"""' to avail the discount. That too done at your doorstep.</span>
			</td>
		</tr>
	</tbody></table>




				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock">
		<tbody class="mcnImageCardBlockOuter">
			<tr>
				<td class="mcnImageCardBlockInner" valign="top" style="padding-top:9px; padding-right:18px; padding-bottom:9px; padding-left:18px;">

	<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;">
		<tbody><tr>
			<td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top:0px; padding-right:0px; padding-bottom:0; padding-left:0px;">



				<img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/a21a0abd-767a-456d-ba58-f4ffcff807e7.jpg" width="564" style="max-width:2667px;" class="mcnImage">


			</td>
		</tr>
		<tr>
			<td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;" width="546">
				<span style="font-size:12px">Bike servicing at your preferred service center with Free Pick up and Drop. Use coupon code '"""+ bike +"""' to avail the discount.</span>
			</td>
		</tr>
	</tbody></table>




				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock">
		<tbody class="mcnImageCardBlockOuter">
			<tr>
				<td class="mcnImageCardBlockInner" valign="top" style="padding-top:9px; padding-right:18px; padding-bottom:9px; padding-left:18px;">

	<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;">
		<tbody><tr>
			<td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top:0px; padding-right:0px; padding-bottom:0; padding-left:0px;">



				<img alt="" src="https://gallery.mailchimp.com/2cf3731a4f89990fe68c1bf2a/images/3a2f77ba-b256-4404-a8d9-f5047e957111.jpg" width="564" style="max-width:2663px;" class="mcnImage">


			</td>
		</tr>
		<tr>
			<td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;" width="546">
				<span style="font-size:13px">Car servicing at Quality carcrew workshop. Use '""" +service+"""' to avail the discount.</span>
			</td>
		</tr>
	</tbody></table>




				</td>
			</tr>
		</tbody>
	</table></td>
											</tr>
										</table>
										<!--[if gte mso 9]>
										</td>
										</tr>
										</table>
										<![endif]-->
									</td>
								</tr>
								<tr>
									<td align="center" valign="top" id="templateFooter">
										<!--[if gte mso 9]>
										<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
										<tr>
										<td align="center" valign="top" width="600" style="width:600px;">
										<![endif]-->
										<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
											<tr>
												<td valign="top" class="footerContainer"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock" style="min-width:100%;">
		<tbody class="mcnFollowBlockOuter">
			<tr>
				<td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
					<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer" style="min-width:100%;">
		<tbody><tr>
			<td align="center" style="padding-left:9px;padding-right:9px;">
				<table border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnFollowContent">
					<tbody><tr>
						<td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
							<table align="center" border="0" cellpadding="0" cellspacing="0">
								<tbody><tr>
									<td align="center" valign="top">
										<!--[if mso]>
										<table align="center" border="0" cellspacing="0" cellpadding="0">
										<tr>
										<![endif]-->

											<!--[if mso]>
											<td align="center" valign="top">
											<![endif]-->


												<table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
													<tbody><tr>
														<td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
															<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
																<tbody><tr>
																	<td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
																		<table align="left" border="0" cellpadding="0" cellspacing="0" width="">
																			<tbody><tr>

																					<td align="center" valign="middle" width="24" class="mcnFollowIconContent">
																						<a href="http://www.twitter.com/theCarCrew" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display:block;" height="24" width="24" class=""></a>
																					</td>


																			</tr>
																		</tbody></table>
																	</td>
																</tr>
															</tbody></table>
														</td>
													</tr>
												</tbody></table>

											<!--[if mso]>
											</td>
											<![endif]-->

											<!--[if mso]>
											<td align="center" valign="top">
											<![endif]-->


												<table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
													<tbody><tr>
														<td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
															<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
																<tbody><tr>
																	<td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
																		<table align="left" border="0" cellpadding="0" cellspacing="0" width="">
																			<tbody><tr>

																					<td align="center" valign="middle" width="24" class="mcnFollowIconContent">
																						<a href="http://www.facebook.com/carcrew.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display:block;" height="24" width="24" class=""></a>
																					</td>


																			</tr>
																		</tbody></table>
																	</td>
																</tr>
															</tbody></table>
														</td>
													</tr>
												</tbody></table>

											<!--[if mso]>
											</td>
											<![endif]-->

											<!--[if mso]>
											<td align="center" valign="top">
											<![endif]-->


												<table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
													<tbody><tr>
														<td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
															<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
																<tbody><tr>
																	<td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
																		<table align="left" border="0" cellpadding="0" cellspacing="0" width="">
																			<tbody><tr>

																					<td align="center" valign="middle" width="24" class="mcnFollowIconContent">
																						<a href="http://instagram.com/theclickgarage" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-instagram-48.png" style="display:block;" height="24" width="24" class=""></a>
																					</td>


																			</tr>
																		</tbody></table>
																	</td>
																</tr>
															</tbody></table>
														</td>
													</tr>
												</tbody></table>

											<!--[if mso]>
											</td>
											<![endif]-->

											<!--[if mso]>
											<td align="center" valign="top">
											<![endif]-->


												<table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
													<tbody><tr>
														<td valign="top" style="padding-right:0; padding-bottom:9px;" class="mcnFollowContentItemContainer">
															<table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
																<tbody><tr>
																	<td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
																		<table align="left" border="0" cellpadding="0" cellspacing="0" width="">
																			<tbody><tr>

																					<td align="center" valign="middle" width="24" class="mcnFollowIconContent">
																						<a href="http://www.yourwebsite.com" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display:block;" height="24" width="24" class=""></a>
																					</td>


																			</tr>
																		</tbody></table>
																	</td>
																</tr>
															</tbody></table>
														</td>
													</tr>
												</tbody></table>

											<!--[if mso]>
											</td>
											<![endif]-->

										<!--[if mso]>
										</tr>
										</table>
										<![endif]-->
									</td>
								</tr>
							</tbody></table>
						</td>
					</tr>
				</tbody></table>
			</td>
		</tr>
	</tbody></table>

				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
		<tbody class="mcnDividerBlockOuter">
			<tr>
				<td class="mcnDividerBlockInner" style="min-width: 100%; padding: 10px 18px 25px;">
					<table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top-width: 2px;border-top-style: solid;border-top-color: #EEEEEE;">
						<tbody><tr>
							<td>
								<span></span>
							</td>
						</tr>
					</tbody></table>
	<!--
					<td class="mcnDividerBlockInner" style="padding: 18px;">
					<hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
	-->
				</td>
			</tr>
		</tbody>
	</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
		<tbody class="mcnTextBlockOuter">
			<tr>
				<td valign="top" class="mcnTextBlockInner">

					<table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnTextContentContainer">
						<tbody><tr>

							<td valign="top" class="mcnTextContent" style="padding-top:9px; padding-right: 18px; padding-bottom: 9px; padding-left: 18px;">

								<em>Copyright - 2015 Carcrew TechnologyPvt. Ltd., All rights reserved.</em><br>
	<br>
	<strong>Our mailing address is:</strong><br>
	sales@carcrew.in<br>
	<br>
	<strong>Contact:</strong><br>
	+91-7045996415<br>
	&nbsp;
							</td>
						</tr>
					</tbody></table>

				</td>
			</tr>
		</tbody>
	</table></td>
											</tr>
										</table>
										<!--[if gte mso 9]>
										</td>
										</tr>
										</table>
										<![endif]-->
									</td>
								</tr>
							</table>
							<!-- // END TEMPLATE -->
						</td>
					</tr>
				</table>
			</center>
		</body>
	</html>"""


	script = MIMEText(html, 'html')

	msg.attach(script)


	smtp_port = '25'
	smtp_do_tls = True

	server = smtplib.SMTP(
		host = smtp_server,
		port = smtp_port,
		timeout = 30
	)
	server.set_debuglevel(10)
	server.starttls()
	server.ehlo()
	server.login(smtp_username, smtp_password)
	server.sendmail(me, you, msg.as_string())
	server.quit()


# <<<<------ Website revamp ------>>>>>
region ='us-west-2'
aws_access='AKIAJNAYBONVQTNTSLZQ'
aws_secret='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'

cgpoc = "Saurabh - 9953083005 "

import requests
import json


# "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to"=+to+"&msg="+message+"&msg_type=TEXT&userid=2000177606&auth_scheme=plain&password=DgQTlzCg5&v=1.1&format=text

def send_promo_campaign_cg(to,message):
	# url = "http://2factor.in/API/V1/e5fd3098-a453-11e6-a40f-00163ef91450/ADDON_SERVICES/SEND/PSMS"
	# payload = {
	# 	"From": "CARCRW",
	# 	"To": to	,
	# 	"Msg" :message
	# }
	# response = requests.request("GET", url, data = json.dumps(payload))
	# print(response.text)
	message = message.replace(" ", "+")
	# url  = "http://api.msg91.com/api/sendhttp.php?route=4&country=IN&flash=0&unicode=0&campaign=viaSOCKET&authkey=151673AJzvZcNCte59758f85&mobiles=" + to +"&message=" + message + "&sender=CARCRW"
	url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to="+to+"&msg="+message+"&msg_type=TEXT&userid=2000177606&auth_scheme=plain&password=DgQTlzCg5&v=1.1&override_dnd=true&format=text"
	# url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message=" + message + "&sendername=" + sendername + "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)



def send_promo_campaign_agent(to,message):
	# url = "http://2factor.in/API/V1/e5fd3098-a453-11e6-a40f-00163ef91450/ADDON_SERVICES/SEND/PSMS"
	# payload = {
	# 	"From": "EZYGRG",
	# 	"To": to	,
	# 	"Msg" :message
	# }
	# response = requests.request("GET", url, data = json.dumps(payload))
	# print(response.text)
	message = message.replace(" ", "+")
	url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to="+to+"&msg="+message+"&msg_type=TEXT&userid=2000177606&auth_scheme=plain&password=DgQTlzCg5&v=1.1&override_dnd=true&format=text"

	# url  = "http://api.msg91.com/api/sendhttp.php?route=4&country=IN&flash=0&unicode=0&campaign=viaSOCKET&authkey=151673AJzvZcNCte59758f85&mobiles=" + to +"&message=" + message + "&sender=EZYGRG"
	# url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message=" + message + "&sendername=" + sendername + "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)





def send_sms_2factor(to,message):
	# 2 Factor

	# url = "http://2factor.in/API/V1/e5fd3098-a453-11e6-a40f-00163ef91450/ADDON_SERVICES/SEND/TSMS"
	# payload = {
	# 	"From":"CARCRW",
	# 	"To": to	   ,
	# 	"Msg":message
	# }
	# response = requests.request("GET", url, data = json.dumps(payload))
	# print(response.text)

	# Message 91
	message = message.replace(" ", "+")
	# url  = "http://api.msg91.com/api/sendhttp.php?route=4&country=IN&flash=0&unicode=0&campaign=viaSOCKET&authkey=151673AJzvZcNCte59758f85&mobiles=" + to +"&message=" + message + "&sender=CARCRW"
	url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to="+to+"&msg="+message+"&msg_type=TEXT&userid=2000177606&auth_scheme=plain&password=DgQTlzCg5&v=1.1&override_dnd=true&format=text"

	# url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message=" + message + "&sendername=" + sendername + "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)

def send_sms_msg91(to,message):
	message = message.replace(" ", "+")
	url  = "http://api.msg91.com/api/sendhttp.php?route=4&country=IN&flash=0&unicode=0&campaign=viaSOCKET&authkey=151673AJzvZcNCte59758f85&mobiles=" + to +"&message=" + message + "&sender=CARCRW"
	# url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message=" + message + "&sendername=" + sendername + "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)



def send_sms_2factor_EZY(to,message):
	# 2 Factor

	# url = "http://2factor.in/API/V1/e5fd3098-a453-11e6-a40f-00163ef91450/ADDON_SERVICES/SEND/TSMS"
	# payload = {
	# 	"From":"EZYGRG",
	# 	"To": to	   ,
	# 	"Msg":message
	# }
    #
	# response = requests.request("GET", url, data = json.dumps(payload))
	# print(response.text)

	# Message 91
	message = message.replace(" ", "+")
	# url = "http://api.msg91.com/api/sendhttp.php?route=4&country=IN&flash=0&unicode=0&campaign=viaSOCKET&authkey=151673AJzvZcNCte59758f85&mobiles=" + to + "&message=" + message + "&sender=EZYGRG"
	url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=SendMessage&send_to="+to+"&msg="+message+"&msg_type=TEXT&userid=2000177606&auth_scheme=plain&password=DgQTlzCg5&v=1.1&override_dnd=true&format=text"

	# url = "http://sms.hspsms.com/sendSMS?username=clickgarage&message=" + message + "&sendername=" + sendername + "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)


def send_otp(to,message):
	send_sms_2factor(to,message)

def send_message(firstname,lastname,number,email,message):
	me = "info@clickgarage.in"
	you = staffmails
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Contact Mail"
	msg['From'] = me
	msg['To'] = ', '.join(you)

	message = "Name: " + firstname + " " + lastname + " | Phone: " + number+ " | Email: " + email + " | Message : " + message
	script = MIMEText(message, 'html')
	msg.attach(script)

	conn = boto.ses.connect_to_region(region,aws_access_key_id=aws_access,aws_secret_access_key=aws_secret)
	result = conn.send_raw_email(msg.as_string())

def send_lead(firstname,lastname, number,email, car_bike, make, model, fuel_type, additional, service_category,locality,address,date_requested,time_requested):
	me = "bookings@clickgarage.in"
	you = staffmails
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Lead"
	msg['From'] = me
	msg['To'] = ', '.join(you)

	message = "Name: " + firstname + " " + lastname + " | Phone: " + number+ " | Email: " + email +" | Car/Bike : " + car_bike+ " | Vehicle : " + make + " " + model + " " + fuel_type + " | Additional :" + additional + " | Service Category : " + service_category + " | Locality : " + locality + " | Address : "+address+" | Date :" + date_requested +" | Time :" + time_requested
	script = MIMEText(message, 'html')
	msg.attach(script)

	conn = boto.ses.connect_to_region(region,aws_access_key_id=aws_access,aws_secret_access_key=aws_secret)
	result = conn.send_raw_email(msg.as_string())
def send_booking(firstname,lastname, number,email, car_bike, make, model, fuel_type, locality,address,date_requested,time_requested):
	me = "bookings@clickgarage.in"
	you = "bookings@clickgarage.in"
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "New Lead/Booking"
	msg['From'] = me
	msg['To'] = you

	message = "Name: " + firstname + " " + lastname + " | Phone: " + number+ " | Email: " + email +" | Car/Bike : " + car_bike+ " | Vehicle : " + make + " " + model + " " + fuel_type  + " | Locality : " + locality + " | Address : "+address+" | Date :" + date_requested +" | Time :" + time_requested
	script = MIMEText(message, 'html')
	msg.attach(script)

	conn = boto.ses.connect_to_region(region,aws_access_key_id=aws_access,aws_secret_access_key=aws_secret)
	result = conn.send_raw_email(msg.as_string())


def send_booking_confirm(email,name,booking_id,number,service_list,car_bike):
	# print email
	me = from_address
	you = email
	# cgpoc = "Amit - 9560059744 "
	# cgpoc = "Shubham - 8800249924 "
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Confirmation! Booking ID: " + str(booking_id)
	msg['From'] = me
	msg['To'] = you

	html = html_to_send(name, booking_id, service_list, car_bike)

	# html = "Hi "+name+"Your booking with ClickGarage has been confirmed. Pick up time selected by you is "+time+" on "+date+"For further details please contact "+helpline_number+" and quote your booking reference id :"+str(booking_id)+"."
	booking = Bookings.objects.filter(booking_id=booking_id)[0]
	script = MIMEText(html, 'html')
	msg.attach(script)
	conn = boto.ses.connect_to_region(region,aws_access_key_id=aws_access,aws_secret_access_key=aws_secret)
	# print email
	if email == "--":
		print "check"
		None
	else:
		if booking.clickgarage_flag == True:
			result = conn.send_raw_email(msg.as_string())

	print booking.agent
	if booking.agent != "":
		agent = CGUserNew.objects.filter(id = booking.agent)[0]
		agent_name = agent.first_name
		full_agent_name = agent.first_name + ' ' + agent.last_name
		agent_num = agent.contact_no

	if booking.clickgarage_flag == True and booking.status != "Lead":
		if booking.cust_vehicle_type == "Car":
			message = "Hi " + name + "! Your Carcrew order has been placed. You will recieve a call shortly to confirm the order. For further assistance, please contact your relationship manager " + cgpoc + " and quote your booking ID: " + str(booking_id)
		else:
			message = "Hi " + name + "! Currently our bike operations are on hold for improvements. Apologies for the inconvinience caused. Happy Motoring, Team Carcrew!"
		send_sms_2factor(number, message)
	elif booking.clickgarage_flag == True and booking.status == "Lead":
		message = "Hi " + name + "! Thank you for visiting Carcrew! Your relationship manager will get in touch with you shortly to understand your requirements. Happy Motoring! Team Carcrew."
		send_sms_2factor(number, message)
	else:
		message = "Hi " + name + "! Your booking with " + full_agent_name + " has been confirmed for " + str(booking.time_booking) + " on " + str(booking.date_booking) + ".  For further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(
			booking_id) + ". Booking tracking link: https://www.carcrew.in/track/" + booking.id + "/details"
		# print message
		send_sms_2factor_EZY(number, message)



def send_bill_estimate(dataid,bill_estimate):
	me = from_address
	booking = Bookings.objects.filter(id = dataid)[0]
	email = booking.cust_email
	serviceitems = booking.service_items
	name = booking.cust_name
	booking_id = booking.booking_id
	price_total = booking.price_total

	you = email
	msg = MIMEMultipart('alternative')
	if bill_estimate == "Bill":
		msg['Subject'] = "Job Completed! Booking ID: " + str(booking_id)
	elif bill_estimate == "Estimate":
		msg['Subject'] = "Job Estimate! Booking ID: " + str(booking_id)
	msg['From'] = me
	msg['To'] = you

	html = html_to_send_bill_estimate(name=name, booking_id=booking_id, bill_estimate= bill_estimate, total_amount=price_total , service_list=serviceitems, data_id=dataid)
	script = MIMEText(html, 'html')
	msg.attach(script)

	if bill_estimate == "Bill":
		bill_id = booking.bill_id
		bill = Bills.objects.filter(id = bill_id)[0]
		filename = bill.file_name
		part = MIMEApplication(open(filename, 'rb').read())
		part.add_header('Content-Disposition', 'attachment', filename='Invoice.pdf')
		msg.attach(part)

	conn = boto.ses.connect_to_region(region,aws_access_key_id=aws_access,aws_secret_access_key=aws_secret)
	print email
	if email == "--":
		print "check"
		None
	else:
		if booking.clickgarage_flag == True:
			result = conn.send_raw_email(msg.as_string())




def send_sms_customer_manual(dataid,message):
	booking = Bookings.objects.filter(id=dataid)[0]
	customer_number = booking.cust_number
	if booking.clickgarage_flag:
		message = "Hello " + booking.cust_name + "," + message + " Happy Motoring, Team Carcrew!"
		send_sms_2factor(customer_number, message)
	else:
		message = "Hello " + booking.cust_name + "," + message
		send_sms_2factor_EZY(customer_number, message)


def send_sms_customer(name,number,booking_id,date,time,agent_details = None,estimate=None, status=None, status2=None):
	booking = Bookings.objects.filter(booking_id = booking_id)[0]
	# cgpoc = "Amit - 9560059744 "
	if booking.agent != "":
		agent = CGUserNew.objects.filter(id = booking.agent)[0]
		agent_name = agent.first_name
		full_agent_name = agent.first_name + ' ' + agent.last_name
		agent_num = agent.contact_no
		agent_details = agent_name + " - " + agent_num

	if status =="Confirmed":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! Your Carcrew order has been confirmed for "+ str(time) + " on " + str(date) +". You will recieve the engineer details shortly. For further assistance, please contact your relationship manager " + cgpoc + " and quote your booking ID: " + str(
				booking_id)
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! Your booking with"+ full_agent_name +" has been confirmed for " + str(time) + " on " + str(date) + ".  For further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(booking_id) + ". Booking tracking link: https://www.carcrew.in/track/" + booking.id + "/details"
			send_sms_2factor_EZY(number, message)
	if status == "Assigned":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! Carcrew Service engineer "+full_agent_name+ " has been assigned for your order. For further assistance, please contact your relationship manager " + cgpoc + " and quote your booking ID: " + str(booking_id)  + ".For driver details and other relevant info. use our Booking tracking link: https://www.carcrew.in/track/" + booking.id + "/details"
			send_sms_2factor(number, message)
	if status =="Engineer Left":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! Our engineer " + str(agent_details) + " has left and is on his way for your booking. For further assistance, please contact us on " + cgpoc + " and quote your booking ID: " + str(
				booking_id)
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! Our engineer has left and is on his way for your booking. For further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(
				booking_id)
			send_sms_2factor_EZY(number, message)

	if status == "Reached Workshop":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! Your vehicle has reached the workshop. You will recieve and updated estimate post inspection. For further assistance, please contact us on " + cgpoc + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! Your vehicle has reached the workshop. You will recieve and updated estimate post inspection. For further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(
				booking_id) + "."
			print "2"
			send_sms_2factor_EZY(number, message)
	if status == "Estimate Shared":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! We have done the complete inspection. Your updated estimate post inspection is Rs." + str(
				estimate) + ". if there is any discrepency or for any further assistance, please contact us on " + cgpoc + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! We have done the complete inspection. Your updated estimate post inspection is Rs." + str(
				estimate) + ". if there is any discrepency or for any further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor_EZY(number, message)

	if status == "Job Complete" and status2=="Escalation":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! Your order is complete. We apologize for the incovenience caused. If you require any further assistance, please contact us on " + cgpoc + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! Your order is complete. We apologize for the incovenience caused. If you require any further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor_EZY(number, message)

	if status =="Job Complete" and status2==None:
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! Your order is complete. If you require any further assistance, please contact us on " + cgpoc + " and quote your booking ID: " + str(booking_id) + ". For any escalations please contact: " + str(escalation_number)
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! Your order is complete. If you require any further assistance, please contact us on " + agent_num + " and quote your booking ID: " + str(booking_id) + "."
			send_sms_2factor_EZY(number, message)

	if status == "Escalation":
		if booking.clickgarage_flag == True:
			message = "Hi " + name + "! We apologize for the inconvenience caused. We are taking necessary action to solve the issue. If you require any further assistance, directly call our escaltion number : " + str(escalation_number) + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor(number, message)
		else:
			message = "Hi " + name + "! We apologize for the inconvenience caused. We are taking necessary action to solve the issue. If you require any further assistance, directly call our escaltion number : " + str(agent_num) + " and quote your booking ID: " + str(
				booking_id) + "."
			send_sms_2factor_EZY(number, message)

def send_sms_agent(agent_name, agent_num, cust_num,date,time,booking_id,cust_name, comments, total, address,vehicle ):
	booking = Bookings.objects.filter(booking_id = booking_id)[0]
	booking_data_id = booking.id
	message = "Carcrew Booking ID:"+str(booking_id)+" | Date:" + str(date) + " | Time: " + str(time) + "| Name:"+ cust_name + "("+cust_num+")| Vehicle:"+ vehicle
	# i = 1
	# for comment in comments:
	# 	message += str(i) + ") "+ comment['Job']
	# 	i = i + 1
	message +=  " | Address: "+str(address)
	message += " | Link: https://www.carcrew.in/adminpanel/bookings/single/" + str(booking_data_id)
	print message
	# message = message.replace(" ", "+")
	send_sms_2factor(agent_num, message)

def html_to_send(name, booking_id, service_list,car_bike):

	doorstep_list = []
	category_list = []
	# doorstep = "1"
	# service_cat = "Cleaning"
	summary_html2 = "<table style = 'border: 1px solid; width: 100%; border-collapse: collapse;'><tr style = 'border: 1px solid;'><th>Job name</th><th>Amount</th></tr>"
	for serv in service_list:
		if serv['category']:
			category_list.append(str(serv['category']))
		try:
			if serv['doorstep']:
				doorstep_list.append(str(serv['doorstep']))
		except:
			None

		summary_html2 = summary_html2 + "<tr><td>" + serv['job_name'] + "</td><td>Rs. &nbsp;" + str(serv['price_total']) + "</td></tr>"

	# print doorstep_list
	# print category_list
	service_cat = "Other"
	if "0" in doorstep_list:
		doorstep = "0"
		if "Servicing" in category_list or "Repairing" in category_list or "Denting" in category_list or "Emergency" in category_list:
			service_cat = "Other"
		elif "Cleaning" in category_list:
			service_cat = "Cleaning"
		elif "Subscription" in category_list:
			service_cat = "Subscription"
	else:
		doorstep = "1"
		if "Cleaning" in category_list:
			service_cat = "Cleaning"
		else:
			service_cat = "Other"

	summary_html2 = summary_html2 + "</table>"
	summary_html = str(summary_html2)
	# print summary_html
	# print doorstep
	# print service_cat
	booking_id = str(booking_id)
	html = ""
	if car_bike == "Car":
		if doorstep == "1" and service_cat == "Cleaning":
			# html = "1 Cleaning"
			html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <!--<![endif]-->

  <!--[if (gte mso 9)|(IE)]><style type="text/css">
  table {border-collapse: collapse;}
  table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
  img {-ms-interpolation-mode: bicubic;}
  </style>
  <![endif]-->
  <style type="text/css">
  body {
    color: #000000;
  }
  body a {
    color: #1188e6;
    text-decoration: none;
  }
  p { margin: 0; padding: 0; }
  table[class="wrapper"] {
    width:100% !important;
    table-layout: fixed;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  img[class="max-width"] {
    max-width: 100% !important;
  }
  @media screen and (max-width:480px) {
    .preheader .rightColumnContent,
    .footer .rightColumnContent {
        text-align: left !important;
    }
    .preheader .rightColumnContent div,
    .preheader .rightColumnContent span,
    .footer .rightColumnContent div,
    .footer .rightColumnContent span {
      text-align: left !important;
    }
    .preheader .rightColumnContent,
    .preheader .leftColumnContent {
      font-size: 80% !important;
      padding: 5px 0;
    }
    table[class="wrapper-mobile"] {
      width: 100% !important;
      table-layout: fixed;
    }
    img[class="max-width"] {
      height: auto !important;
    }
    a[class="bulletproof-button"] {
      display: block !important;
      width: auto !important;
      font-size: 80%;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    // 2 columns
    #templateColumns{
        width:100% !important;
    }

    .templateColumnContainer{
        display:block !important;
        width:100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
  }
  </style>
  <style>
  body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
  <center class="wrapper">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
      <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
      <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
          <![endif]-->
            <table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td>
                    <!--[if (gte mso 9)|(IE)]>
                      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <![endif]-->
                              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
                                <tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
                                  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
  <tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="600" valign="top">
<![endif]-->


<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Booking (ID: """+booking_id+""") has been placed. We will call you shortly to confirm the pick-up time.&nbsp;</div> </td>
</tr>
</table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A16%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 16px 0px;" bgcolor="#ffffff"></td></tr></table>

"""+summary_html+"""
<!-- <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A2%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>Test1</div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: right;">Test2</div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%2C%22linecolor%22%3A%22%23000000%22%2C%22height%22%3A5%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff">
  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="5"  style="font-size: 5px; line-height: 5px;">
    <tr><td bgcolor="#000000">&nbsp;</td></tr>
  </table>
</td></tr></table> -->
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%227%2C0%2C6%2C0%22%2C%22containerbackground%22%3A%22%2309a2dc%22%7D'>
<tr><td role="module-content" style="padding: 7px 0px 6px 0px;" bgcolor="#09a2dc"><div style="text-align: center;"><span style="color:#FFFFFF;"><strong>How it works?</strong></span></div> </td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A18%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 18px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A3%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/1d92b75b2550e6ccc6203c39a146b5f62f858e7228b3802abec61c6f437a526b62ec0d3bc9a095bdf93bdd7fdc7a0876060745a23542e3049ae3fd10b307149e.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/1d92b75b2550e6ccc6203c39a146b5f62f858e7228b3802abec61c6f437a526b62ec0d3bc9a095bdf93bdd7fdc7a0876060745a23542e3049ae3fd10b307149e.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Carcrewcleaning experts drop by at the location, equipped with machines</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/ec61f78aabe6c9ef7c0d4c6ab0b05351c6a4420134709a36c78bc0e0e2204a71b285e3879cbfdaaf9ed198103ecd8227d99554eb20ef5b393d726613a7da1978.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/ec61f78aabe6c9ef7c0d4c6ab0b05351c6a4420134709a36c78bc0e0e2204a71b285e3879cbfdaaf9ed198103ecd8227d99554eb20ef5b393d726613a7da1978.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Requested cleaning services will be done at the doorstep itself</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-2" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Make payments through multiple payment options avaialble</span></div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">

        <td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi | To unsubscribe click: <a href="[Unsubscribe]">here</a></div> </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>

      </tr>
    </table>
  </td></tr>
</table>

                                </tr></td>
                              </table>
                            <!--[if (gte mso 9)|(IE)]>
                          </td>
                        </td>
                      </table>
                    <![endif]-->
                    </td>
                  </tr>
                </table></td>
              </tr>
            </table>
          <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
      </table>
      <![endif]-->
      </tr></td>
      </table>
    </div>
  </center>
</body>
</html>"""
		elif doorstep == "0" and service_cat == "Cleaning":
			# html = "0 Cleaning"
			html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <!--<![endif]-->

  <!--[if (gte mso 9)|(IE)]><style type="text/css">
  table {border-collapse: collapse;}
  table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
  img {-ms-interpolation-mode: bicubic;}
  </style>
  <![endif]-->
  <style type="text/css">
  body {
    color: #000000;
  }
  body a {
    color: #1188e6;
    text-decoration: none;
  }
  p { margin: 0; padding: 0; }
  table[class="wrapper"] {
    width:100% !important;
    table-layout: fixed;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  img[class="max-width"] {
    max-width: 100% !important;
  }
  @media screen and (max-width:480px) {
    .preheader .rightColumnContent,
    .footer .rightColumnContent {
        text-align: left !important;
    }
    .preheader .rightColumnContent div,
    .preheader .rightColumnContent span,
    .footer .rightColumnContent div,
    .footer .rightColumnContent span {
      text-align: left !important;
    }
    .preheader .rightColumnContent,
    .preheader .leftColumnContent {
      font-size: 80% !important;
      padding: 5px 0;
    }
    table[class="wrapper-mobile"] {
      width: 100% !important;
      table-layout: fixed;
    }
    img[class="max-width"] {
      height: auto !important;
    }
    a[class="bulletproof-button"] {
      display: block !important;
      width: auto !important;
      font-size: 80%;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    // 2 columns
    #templateColumns{
        width:100% !important;
    }

    .templateColumnContainer{
        display:block !important;
        width:100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
  }
  </style>
  <style>
  body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
  <center class="wrapper">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
      <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
      <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
          <![endif]-->
            <table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td>
                    <!--[if (gte mso 9)|(IE)]>
                      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <![endif]-->
                              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
                                <tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
                                  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
  <tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="600" valign="top">
<![endif]-->


<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Booking (ID:"""+booking_id+""" ) has been placed. We will call you shortly to confirm the pick-up time.&nbsp;</div> </td>
</tr>
</table>
"""+summary_html+"""
<!-- <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A16%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 16px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A2%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>Test1</div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: right;">Test2</div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table> -->
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%2C%22linecolor%22%3A%22%23000000%22%2C%22height%22%3A5%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff">
  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="5"  style="font-size: 5px; line-height: 5px;">
    <tr><td bgcolor="#000000">&nbsp;</td></tr>
  </table>
</td></tr></table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%227%2C0%2C6%2C0%22%2C%22containerbackground%22%3A%22%2309a2dc%22%7D'>
<tr><td role="module-content" style="padding: 7px 0px 6px 0px;" bgcolor="#09a2dc"><div style="text-align: center;"><span style="color:#FFFFFF;"><strong>How it works?</strong></span></div> </td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A18%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 18px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A3%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/1d92b75b2550e6ccc6203c39a146b5f62f858e7228b3802abec61c6f437a526b62ec0d3bc9a095bdf93bdd7fdc7a0876060745a23542e3049ae3fd10b307149e.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Carcrewexperts drop by at the location to pick the vehicle</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/ec61f78aabe6c9ef7c0d4c6ab0b05351c6a4420134709a36c78bc0e0e2204a71b285e3879cbfdaaf9ed198103ecd8227d99554eb20ef5b393d726613a7da1978.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/ec61f78aabe6c9ef7c0d4c6ab0b05351c6a4420134709a36c78bc0e0e2204a71b285e3879cbfdaaf9ed198103ecd8227d99554eb20ef5b393d726613a7da1978.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Requested cleaning services will be done at the workshop</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-2" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Make payments through multiple payment options avaialble</span></div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">

        <td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi | To unsubscribe click: <a href="[Unsubscribe]">here</a></div> </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>

      </tr>
    </table>
  </td></tr>
</table>

                                </tr></td>
                              </table>
                            <!--[if (gte mso 9)|(IE)]>
                          </td>
                        </td>
                      </table>
                    <![endif]-->
                    </td>
                  </tr>
                </table></td>
              </tr>
            </table>
          <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
      </table>
      <![endif]-->
      </tr></td>
      </table>
    </div>
  </center>
</body>
</html>"""
		elif doorstep == "1":
			# html = "1 Other"
			html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <!--<![endif]-->

  <!--[if (gte mso 9)|(IE)]><style type="text/css">
  table {border-collapse: collapse;}
  table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
  img {-ms-interpolation-mode: bicubic;}
  </style>
  <![endif]-->
  <style type="text/css">
  body {
    color: #000000;
  }
  body a {
    color: #1188e6;
    text-decoration: none;
  }
  p { margin: 0; padding: 0; }
  table[class="wrapper"] {
    width:100% !important;
    table-layout: fixed;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  img[class="max-width"] {
    max-width: 100% !important;
  }
  @media screen and (max-width:480px) {
    .preheader .rightColumnContent,
    .footer .rightColumnContent {
        text-align: left !important;
    }
    .preheader .rightColumnContent div,
    .preheader .rightColumnContent span,
    .footer .rightColumnContent div,
    .footer .rightColumnContent span {
      text-align: left !important;
    }
    .preheader .rightColumnContent,
    .preheader .leftColumnContent {
      font-size: 80% !important;
      padding: 5px 0;
    }
    table[class="wrapper-mobile"] {
      width: 100% !important;
      table-layout: fixed;
    }
    img[class="max-width"] {
      height: auto !important;
    }
    a[class="bulletproof-button"] {
      display: block !important;
      width: auto !important;
      font-size: 80%;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    // 2 columns
    #templateColumns{
        width:100% !important;
    }

    .templateColumnContainer{
        display:block !important;
        width:100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
  }
  </style>
  <style>
  body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
  <center class="wrapper">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
      <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
      <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
          <![endif]-->
            <table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td>
                    <!--[if (gte mso 9)|(IE)]>
                      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <![endif]-->
                              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
                                <tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
                                  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
  <tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="600" valign="top">
<![endif]-->


<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Booking (ID: """+booking_id+""") has been placed. We will call you shortly to confirm the pick-up time.&nbsp;</div> </td>
</tr>
</table>
"""+summary_html+"""
<!-- <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A16%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 16px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A2%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>Test1</div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: right;">Test2</div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table>
 -->
 <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%2C%22linecolor%22%3A%22%23000000%22%2C%22height%22%3A5%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff">
  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="5"  style="font-size: 5px; line-height: 5px;">
    <tr><td bgcolor="#000000">&nbsp;</td></tr>
  </table>
</td></tr></table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%227%2C0%2C6%2C0%22%2C%22containerbackground%22%3A%22%2309a2dc%22%7D'>
<tr><td role="module-content" style="padding: 7px 0px 6px 0px;" bgcolor="#09a2dc"><div style="text-align: center;"><span style="color:#FFFFFF;"><strong>How it works?</strong></span></div> </td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A18%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 18px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A3%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Carcrew experts will drop by at the location, equipped with necessary equipment</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/1b4d8b4136d64f9409faf669c7c17e25f9ef8fe11ba5ae96d173f84254f3af4c6f33e243c45bb8715bf981d370d2c3c2f12093e81a0bf5eb70822526ba835877.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/1b4d8b4136d64f9409faf669c7c17e25f9ef8fe11ba5ae96d173f84254f3af4c6f33e243c45bb8715bf981d370d2c3c2f12093e81a0bf5eb70822526ba835877.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Post inspection job will be performed at the location</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-2" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Make payments through multiple payment options avaialble</span></div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">

        <td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi | To unsubscribe click: <a href="[Unsubscribe]">here</a></div> </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>

      </tr>
    </table>
  </td></tr>
</table>

                                </tr></td>
                              </table>
                            <!--[if (gte mso 9)|(IE)]>
                          </td>
                        </td>
                      </table>
                    <![endif]-->
                    </td>
                  </tr>
                </table></td>
              </tr>
            </table>
          <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
      </table>
      <![endif]-->
      </tr></td>
      </table>
    </div>
  </center>
</body>
</html>"""
		elif doorstep == "0":
			# html = "0 Other"
			html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <!--<![endif]-->

  <!--[if (gte mso 9)|(IE)]><style type="text/css">
  table {border-collapse: collapse;}
  table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
  img {-ms-interpolation-mode: bicubic;}
  </style>
  <![endif]-->
  <style type="text/css">
  body {
    color: #000000;
  }
  body a {
    color: #1188e6;
    text-decoration: none;
  }
  p { margin: 0; padding: 0; }
  table[class="wrapper"] {
    width:100% !important;
    table-layout: fixed;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  img[class="max-width"] {
    max-width: 100% !important;
  }
  @media screen and (max-width:480px) {
    .preheader .rightColumnContent,
    .footer .rightColumnContent {
        text-align: left !important;
    }
    .preheader .rightColumnContent div,
    .preheader .rightColumnContent span,
    .footer .rightColumnContent div,
    .footer .rightColumnContent span {
      text-align: left !important;
    }
    .preheader .rightColumnContent,
    .preheader .leftColumnContent {
      font-size: 80% !important;
      padding: 5px 0;
    }
    table[class="wrapper-mobile"] {
      width: 100% !important;
      table-layout: fixed;
    }
    img[class="max-width"] {
      height: auto !important;
    }
    a[class="bulletproof-button"] {
      display: block !important;
      width: auto !important;
      font-size: 80%;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    // 2 columns
    #templateColumns{
        width:100% !important;
    }

    .templateColumnContainer{
        display:block !important;
        width:100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
  }
  </style>
  <style>
  body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
  <center class="wrapper">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
      <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
      <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
          <![endif]-->
            <table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td>
                    <!--[if (gte mso 9)|(IE)]>
                      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <![endif]-->
                              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
                                <tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
                                  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
  <tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="600" valign="top">
<![endif]-->


<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Booking (ID: """+booking_id+""" ) has been placed. We will call you shortly to confirm the pick-up time.&nbsp;</div> </td>
</tr>
</table>
"""+summary_html+"""
<!-- <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A16%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 16px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A2%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>Test1</div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: right;">Test2</div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table> -->
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%2C%22linecolor%22%3A%22%23000000%22%2C%22height%22%3A5%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff">
  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="5"  style="font-size: 5px; line-height: 5px;">
    <tr><td bgcolor="#000000">&nbsp;</td></tr>
  </table>
</td></tr></table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%227%2C0%2C6%2C0%22%2C%22containerbackground%22%3A%22%2309a2dc%22%7D'>
<tr><td role="module-content" style="padding: 7px 0px 6px 0px;" bgcolor="#09a2dc"><div style="text-align: center;"><span style="color:#FFFFFF;"><strong>How it works?</strong></span></div> </td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A18%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 18px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A3%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Post inspection, the vehicle will be picked up by the mechanic</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/1b4d8b4136d64f9409faf669c7c17e25f9ef8fe11ba5ae96d173f84254f3af4c6f33e243c45bb8715bf981d370d2c3c2f12093e81a0bf5eb70822526ba835877.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/1b4d8b4136d64f9409faf669c7c17e25f9ef8fe11ba5ae96d173f84254f3af4c6f33e243c45bb8715bf981d370d2c3c2f12093e81a0bf5eb70822526ba835877.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Car will be delivered post servicing</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-2" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Make payments through multiple payment options avaialble</span></div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">

        <td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi | To unsubscribe click: <a href="[Unsubscribe]">here</a></div> </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>

      </tr>
    </table>
  </td></tr>
</table>

                                </tr></td>
                              </table>
                            <!--[if (gte mso 9)|(IE)]>
                          </td>
                        </td>
                      </table>
                    <![endif]-->
                    </td>
                  </tr>
                </table></td>
              </tr>
            </table>
          <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
      </table>
      <![endif]-->
      </tr></td>
      </table>
    </div>
  </center>
</body>
</html>"""
		else:
			# html=  "0 Other"
			html = """"""
	if car_bike == "Bike":
		# html = "1 Other"
		html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
  <!--[if !mso]><!-->
  <meta http-equiv="X-UA-Compatible" content="IE=Edge" />
  <!--<![endif]-->

  <!--[if (gte mso 9)|(IE)]><style type="text/css">
  table {border-collapse: collapse;}
  table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
  img {-ms-interpolation-mode: bicubic;}
  </style>
  <![endif]-->
  <style type="text/css">
  body {
    color: #000000;
  }
  body a {
    color: #1188e6;
    text-decoration: none;
  }
  p { margin: 0; padding: 0; }
  table[class="wrapper"] {
    width:100% !important;
    table-layout: fixed;
    -webkit-font-smoothing: antialiased;
    -webkit-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
  }
  img[class="max-width"] {
    max-width: 100% !important;
  }
  @media screen and (max-width:480px) {
    .preheader .rightColumnContent,
    .footer .rightColumnContent {
        text-align: left !important;
    }
    .preheader .rightColumnContent div,
    .preheader .rightColumnContent span,
    .footer .rightColumnContent div,
    .footer .rightColumnContent span {
      text-align: left !important;
    }
    .preheader .rightColumnContent,
    .preheader .leftColumnContent {
      font-size: 80% !important;
      padding: 5px 0;
    }
    table[class="wrapper-mobile"] {
      width: 100% !important;
      table-layout: fixed;
    }
    img[class="max-width"] {
      height: auto !important;
    }
    a[class="bulletproof-button"] {
      display: block !important;
      width: auto !important;
      font-size: 80%;
      padding-left: 0 !important;
      padding-right: 0 !important;
    }
    // 2 columns
    #templateColumns{
        width:100% !important;
    }

    .templateColumnContainer{
        display:block !important;
        width:100% !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
  }
  </style>
  <style>
  body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
  <center class="wrapper">
    <div class="webkit">
      <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
      <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
      <!--[if (gte mso 9)|(IE)]>
      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td>
          <![endif]-->
            <table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
              <tr>
                <td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
                  <tr>
                    <td>
                    <!--[if (gte mso 9)|(IE)]>
                      <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                          <td>
                            <![endif]-->
                              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
                                <tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
                                  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
  <tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="600" valign="top">
<![endif]-->


<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Booking (ID: """+booking_id+""" ) has been placed. We will call you shortly to confirm the pick-up time.&nbsp;</div> </td>
</tr>
</table>
"""+summary_html+"""
<!-- <table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A16%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 16px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A2%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>Test1</div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="50%" height="100%" class="templateColumnContainer column-drop-area ">
  <table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: right;">Test2</div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table> -->
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="divider" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%2C%22linecolor%22%3A%22%23000000%22%2C%22height%22%3A5%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff">
  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" height="5"  style="font-size: 5px; line-height: 5px;">
    <tr><td bgcolor="#000000">&nbsp;</td></tr>
  </table>
</td></tr></table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%227%2C0%2C6%2C0%22%2C%22containerbackground%22%3A%22%2309a2dc%22%7D'>
<tr><td role="module-content" style="padding: 7px 0px 6px 0px;" bgcolor="#09a2dc"><div style="text-align: center;"><span style="color:#FFFFFF;"><strong>How it works?</strong></span></div> </td></tr></table>
<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A18%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 18px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" role="module" data-type="columns" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A3%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22cellpadding%22%3A0%2C%22containerbackground%22%3A%22%22%7D'>
  <tr><td style="padding: 0px 0px 0px 0px;" bgcolor="">
    <table class="columns--container-table" border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">
        <td style="padding: 0px 0px 0px 0px" role="column-0" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/053f97d2e85838a5153c372de959b8db51bda14a450df439ce1209206ae437f66a0d9ae9e3786472a3ffab4cddcc75729188e0f18619105453fdf8544fcc2436.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">The mechanic will come at your doorstep to service the bike</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-1" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/6208f848e060459d8872150c747fff02076140624262ccd194a717da3ba377033820fbbc8e550ccee1fd72a69d65f1cf93c0b97abe185e33991c1fded2d8d780.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/6208f848e060459d8872150c747fff02076140624262ccd194a717da3ba377033820fbbc8e550ccee1fd72a69d65f1cf93c0b97abe185e33991c1fded2d8d780.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Bike will be delivered post-servicing</span></div> </td>
</tr>
</table>

</td><td style="padding: 0px 0px 0px 0px" role="column-2" align="center" valign="top" width="33.333333333333336%" height="100%" class="templateColumnContainer column-drop-area ">
  <table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%2264%22%2C%22height%22%3A%2264%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22center%22%2C%22responsive%22%3Atrue%7D'>
<tr>
  <td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="center" role="module-content"><!--[if mso]>
<center>
<table width="64" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
  <tr>
    <td width="64" valign="top">
<![endif]-->

  <img class="max-width"  width="64"   height=""  src="https://marketing-image-production.s3.amazonaws.com/uploads/55b10b7fd6a9126ce4fed75b853ab45cab0e8ab8b21105981058d15459ee14576a4be83cc2c55fce010ab66d1ef0b1a82240346a230ef2533c24b18c7ef1e9cc.png" alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 64px !important; width: 100% !important; height: auto !important; " />

<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%227%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 7px 0px 0px 0px;" bgcolor="#ffffff"><div style="text-align: center;"><span style="font-size:14px;">Make payments through multiple payment options avaialble</span></div> </td>
</tr>
</table>

</td>
      </tr>
    </table>
  </td></tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
    <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
      <tr role="module-content">

        <td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
          <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
            <tr>
              <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>
  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi | To unsubscribe click: <a href="[Unsubscribe]">here</a></div> </td>
</tr>
</table>
</td>
            </tr>
          </table>
        </td>

      </tr>
    </table>
  </td></tr>
</table>

                                </tr></td>
                              </table>
                            <!--[if (gte mso 9)|(IE)]>
                          </td>
                        </td>
                      </table>
                    <![endif]-->
                    </td>
                  </tr>
                </table></td>
              </tr>
            </table>
          <!--[if (gte mso 9)|(IE)]>
          </td>
        </tr>
      </table>
      <![endif]-->
      </tr></td>
      </table>
    </div>
  </center>
</body>
</html>"""

	return html




def html_to_send_bill_estimate(name, booking_id, bill_estimate, total_amount, service_list,data_id):
	summary_html2 = ""
	confirmed = False
	if booking_id != "":
		booking = Bookings.objects.filter(booking_id = booking_id)[0]
		confirmed = booking.booking_flag
		reg_number = booking.cust_regnumber
		car_name = booking.cust_make + " " + booking.cust_model

	else:
		booking = None
		reg_number = ""
		car_name = ""
		confirmed = False
	summary_html2 = "<table style = 'border: 1px solid; width: 100%; border-collapse: collapse;'><tr style = 'border: 1px solid;'><th>Item name</th><th>Units</th><th>Unit Cost</th><th>Amount</th></tr>"
	for serv in service_list:
		summary_html2 += "<tr><td>" + serv['name'] + "</td><td>" + str(serv['quantity']) + "</td><td>Rs. &nbsp;" + str(serv['unit_price']) + "</td><td>Rs. &nbsp;" + str(serv['price']) + "</td></tr>"


	summary_html2 += "</table>"
	if bill_estimate == "Estimate":
		summary_html = str(summary_html2)
	else:
		summary_html= ""
	booking_id = str(booking_id)
	html = ""
	html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=Edge" />
<!--<![endif]-->

<!--[if (gte mso 9)|(IE)]><style type="text/css">
table {border-collapse: collapse;}
table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
img {-ms-interpolation-mode: bicubic;}
</style>
<![endif]-->
<style type="text/css">
body {
color: #000000;
}
body a {
color: #1188e6;
text-decoration: none;
}
p { margin: 0; padding: 0; }
table[class="wrapper"] {
width:100% !important;
table-layout: fixed;
-webkit-font-smoothing: antialiased;
-webkit-text-size-adjust: 100%;
-moz-text-size-adjust: 100%;
-ms-text-size-adjust: 100%;
}
img[class="max-width"] {
max-width: 100% !important;
}
@media screen and (max-width:480px) {
.preheader .rightColumnContent,
.footer .rightColumnContent {
	text-align: left !important;
}
.preheader .rightColumnContent div,
.preheader .rightColumnContent span,
.footer .rightColumnContent div,
.footer .rightColumnContent span {
  text-align: left !important;
}
.preheader .rightColumnContent,
.preheader .leftColumnContent {
  font-size: 80% !important;
  padding: 5px 0;
}
table[class="wrapper-mobile"] {
  width: 100% !important;
  table-layout: fixed;
}
img[class="max-width"] {
  height: auto !important;
}
a[class="bulletproof-button"] {
  display: block !important;
  width: auto !important;
  font-size: 80%;
  padding-left: 0 !important;
  padding-right: 0 !important;
}
// 2 columns
#templateColumns{
	width:100% !important;
}

.templateColumnContainer{
	display:block !important;
	width:100% !important;
	padding-left: 0 !important;
	padding-right: 0 !important;
}
}
</style>
<style>
body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
<center class="wrapper">
<div class="webkit">
  <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
  <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
  <!--[if (gte mso 9)|(IE)]>
  <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
	<tr>
	  <td>
	  <![endif]-->
		<table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
		  <tr>
			<td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
			  <tr>
				<td>
				<!--[if (gte mso 9)|(IE)]>
				  <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
					<tr>
					  <td>
						<![endif]-->
						  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
							<tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
							  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
<tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
<td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
<tr>
<td width="600" valign="top">
<![endif]-->
<img class="max-width"  width="600"   height=""  src='"""
	if bill_estimate == "Bill":
		html += """https://www.carcrew.in/static/revamp/img/bill_email.jpg"""
	elif bill_estimate == "Estimate":
		html += """https://www.carcrew.in/static/revamp/img/estimate_email.jpg"""
	html += """' alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 600px !important; width: 100% !important; height: auto !important; " />
<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>"""
	if bill_estimate == "Bill":
		if booking_id != "":
			html += """<td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Thank you for using Carcrew. Your order of Booking ID: """+booking_id+""" is complete. Your total due amount is Rs."""+total_amount + """ Please find attached your bill with the email. &nbsp;</div> </td>"""
		else:
			html += """<td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """ + name + """<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Thank you for using Carcrew. Your total due amount is  Rs.""" + total_amount + """ Please find attached your bill with the email. The bill summary is as follows: &nbsp;</div> </td>"""
	elif bill_estimate == "Estimate" and confirmed:
		html += """<td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Your vehicle inspection is complete for the booking ID: """+booking_id+""". The total estimated amount is Rs."""+total_amount + """. Detailed breakup of the jobs is as follows.&nbsp;</div> </td>"""
	elif bill_estimate == "Estimate":
		html += """<td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """ + name + """<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>The total estimated amount for your request is Rs.""" + total_amount + """. Detailed breakup of the jobs is as follows.&nbsp;</div> </td>"""

	html += """</tr><tr><br>"""

	if car_name != "":
		html += """Vehicle Name: """ + car_name + """<br>"""
	if reg_number != "":
		html += """Registration Number: """ + reg_number + """<br><br>"""

	html +="""</tr></table>
	<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A16%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	<tr><td role="module-content" style="padding: 0px 0px 16px 0px;" bgcolor="#ffffff"></td></tr></table>

	"""+summary_html+"""

<br>"""
	if bill_estimate == "Estimate" and confirmed:
		html += """<div><a style="display: block;
    width: 115px;
    height: 25px;
    background: #4a148c;
    padding: 10px;
    text-align: center;
    border-radius: 5px;
    color: white;
    text-decoration: none;
    line-height: 25px;
    width:100%;
    font-weight: bold;" href='https://www.carcrew.in/track/""" + data_id + """/estimate'>Approve Items</a></div>"""
	html +="""<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
	<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
		<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
		  <tr role="module-content">

			<td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
			  <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
				<tr>
				  <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	<tr>
	  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi</div> </td>
	</tr>
	</table>
	</td>
				</tr>
			  </table>
			</td>

		  </tr>
		</table>
	  </td></tr>
	</table>

									</tr></td>
								  </table>
								<!--[if (gte mso 9)|(IE)]>
							  </td>
							</td>
						  </table>
						<![endif]-->
						</td>
					  </tr>
					</table></td>
				  </tr>
				</table>
			  <!--[if (gte mso 9)|(IE)]>
			  </td>
			</tr>
		  </table>
		  <![endif]-->
		  </tr></td>
		  </table>
		</div>
	  </center>
	</body>
	</html>"""
	return html

def html_to_send_report(name, booking_id):
	summary_html2 = ""
	confirmed = False
	if booking_id != "":
		booking = Bookings.objects.filter(booking_id = booking_id)[0]
		confirmed = booking.booking_flag
		reg_number = booking.cust_regnumber
		car_name = booking.cust_make + " " + booking.cust_model

	else:
		booking = None
		reg_number = ""
		car_name = ""
		confirmed = False


	booking_id = str(booking_id)
	html = ""
	html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" data-dnd="true">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1" />
<!--[if !mso]><!-->
<meta http-equiv="X-UA-Compatible" content="IE=Edge" />
<!--<![endif]-->

<!--[if (gte mso 9)|(IE)]><style type="text/css">
table {border-collapse: collapse;}
table, td {mso-table-lspace: 0pt;mso-table-rspace: 0pt;}
img {-ms-interpolation-mode: bicubic;}
</style>
<![endif]-->
<style type="text/css">
body {
color: #000000;
}
body a {
color: #1188e6;
text-decoration: none;
}
p { margin: 0; padding: 0; }
table[class="wrapper"] {
width:100% !important;
table-layout: fixed;
-webkit-font-smoothing: antialiased;
-webkit-text-size-adjust: 100%;
-moz-text-size-adjust: 100%;
-ms-text-size-adjust: 100%;
}
img[class="max-width"] {
max-width: 100% !important;
}
@media screen and (max-width:480px) {
.preheader .rightColumnContent,
.footer .rightColumnContent {
	text-align: left !important;
}
.preheader .rightColumnContent div,
.preheader .rightColumnContent span,
.footer .rightColumnContent div,
.footer .rightColumnContent span {
  text-align: left !important;
}
.preheader .rightColumnContent,
.preheader .leftColumnContent {
  font-size: 80% !important;
  padding: 5px 0;
}
table[class="wrapper-mobile"] {
  width: 100% !important;
  table-layout: fixed;
}
img[class="max-width"] {
  height: auto !important;
}
a[class="bulletproof-button"] {
  display: block !important;
  width: auto !important;
  font-size: 80%;
  padding-left: 0 !important;
  padding-right: 0 !important;
}
// 2 columns
#templateColumns{
	width:100% !important;
}

.templateColumnContainer{
	display:block !important;
	width:100% !important;
	padding-left: 0 !important;
	padding-right: 0 !important;
}
}
</style>
<style>
body, p, div { font-family: arial,sans-serif; }
</style>

</head>
<body yahoofix="true" style="min-width: 100%; margin: 0; padding: 0; font-size: 14pxpx; font-family: arial,sans-serif; color: #000000; background-color: #FFFFFF; color: #000000;" data-attributes='%7B%22dropped%22%3Atrue%2C%22bodybackground%22%3A%22%23FFFFFF%22%2C%22bodyfontname%22%3A%22arial%2Csans-serif%22%2C%22bodytextcolor%22%3A%22%23000000%22%2C%22bodylinkcolor%22%3A%22%231188e6%22%2C%22bodyfontsize%22%3A%2214px%22%7D'>
<center class="wrapper">
<div class="webkit">
  <table cellpadding="0" cellspacing="0" border="0" width="100%" class="wrapper" bgcolor="#FFFFFF">
  <tr><td valign="top" bgcolor="#FFFFFF" width="100%">
  <!--[if (gte mso 9)|(IE)]>
  <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
	<tr>
	  <td>
	  <![endif]-->
		<table width="100%" role="content-container" class="outer" data-attributes='%7B%22dropped%22%3Atrue%2C%22containerpadding%22%3A%220%2C0%2C0%2C0%22%2C%22containerwidth%22%3A600%2C%22containerbackground%22%3A%22%23FFFFFF%22%7D' align="center" cellpadding="0" cellspacing="0" border="0">
		  <tr>
			<td width="100%"><table width="100%" cellpadding="0" cellspacing="0" border="0">
			  <tr>
				<td>
				<!--[if (gte mso 9)|(IE)]>
				  <table width="600" align="center" cellpadding="0" cellspacing="0" border="0">
					<tr>
					  <td>
						<![endif]-->
						  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="width: 100%; max-width:600px;" align="center">
							<tr><td role="modules-container" style="padding: 0px 0px 0px 0px; color: #000000; text-align: left;" bgcolor="#FFFFFF" width="100%" align="left">
							  <table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" style="display:none !important; visibility:hidden; opacity:0; color:transparent; height:0; width:0;" class="module preheader preheader-hide" role="module" data-type="preheader">
<tr><td role="module-content"><p></p></td></tr>
</table>
<table class="module" role="module" data-type="wysiwyg" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div>

</div></td></tr></table>
<table role="module" data-type="image" border="0" align="center" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" class="wrapper" data-attributes='%7B%22child%22%3Afalse%2C%22link%22%3A%22%22%2C%22width%22%3A%22600%22%2C%22height%22%3A%22107%22%2C%22imagebackground%22%3A%22%23FFFFFF%22%2C%22url%22%3A%22https%3A//marketing-image-production.s3.amazonaws.com/uploads/bb5c8b37fb8b5c18fa56b1adbdf4ea31daedb73c1df75bc47974c47504873b3b58f73a89ce248498a65fd30bb1dbf308b456ef84787f9c516588b95bb4e21728.jpg%22%2C%22alt_text%22%3A%22%22%2C%22dropped%22%3Atrue%2C%22imagemargin%22%3A%220%2C0%2C0%2C0%22%2C%22alignment%22%3A%22%22%2C%22responsive%22%3Atrue%7D'>
<tr>
<td style="font-size:6px;line-height:10px;background-color:#FFFFFF;padding: 0px 0px 0px 0px;" valign="top" align="" role="module-content"><!--[if mso]>
<center>
<table width="600" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed;">
<tr>
<td width="600" valign="top">
<![endif]-->
<img class="max-width"  width="600"   height=""  src='"""
	# html += """https://www.carcrew.in/static/revamp/img/bill_email.jpg"""
	html += """' alt="" border="0" style="display: block; color: #000; text-decoration: none; font-family: Helvetica, arial, sans-serif; font-size: 16px;  max-width: 600px !important; width: 100% !important; height: auto !important; " />
<!--[if mso]>
</td></tr></table>
</center>
<![endif]--></td>
</tr>
</table><table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
<table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C12%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
<tr>"""
	if booking_id != "":
		html += """<td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """+name+"""<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Thank you for using Carcrew. Your vehicle inspection is complete (Booking ID: """+booking_id+""").  Please find attached your vehicle inspection report in the email. &nbsp;</div> </td>"""
	else:
		html += """<td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 12px 0px;" bgcolor="#ffffff"><div>Hi """ + name + """<span style="color: rgb(116, 120, 126); font-family: Arial, &quot;Helvetica Neue&quot;, Helvetica, sans-serif; font-size: 16px; font-style: normal; font-variant-ligatures: normal; font-variant-caps: normal; font-weight: normal; background-color: rgb(255, 255, 255);">,</span></div>  <div>&nbsp;</div>  <div>&nbsp;</div>  <div>Your vehicle inspection is complete. Thank you for using Carcrew. Please find attached your vehicle inspection report in the email. &nbsp;</div> </td>"""

	html += """</tr><tr><br>"""

	if car_name != "":
		html += """Vehicle Name: """ + car_name + """<br>"""
	if reg_number != "":
		html += """Registration Number: """ + reg_number + """<br><br>"""


	html +="""<table class="module" role="module" data-type="spacer" border="0" cellpadding="0" cellspacing="0" width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22spacing%22%3A30%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	<tr><td role="module-content" style="padding: 0px 0px 30px 0px;" bgcolor="#ffffff"></td></tr></table>
	<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%" class="module footer" role="module" data-type="footer" data-attributes='%7B%22dropped%22%3Atrue%2C%22columns%22%3A1%2C%22padding%22%3A%2210%2C5%2C10%2C5%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	  <tr><td style="padding: 10px 5px 10px 5px;" bgcolor="#ffffff">
		<table border="0" cellpadding="0" cellspacing="0" align="center" width="100%">
		  <tr role="module-content">

			<td align="center" valign="top" width="100%" height="100%" class="templateColumnContainer">
			  <table border="0" cellpadding="0" cellspacing="0" width="100%" height="100%">
				<tr>
				  <td class="leftColumnContent" role="column-one" height="100%" style="height:100%;"><table class="module" role="module" data-type="text" border="0" cellpadding="0" cellspacing="0"  width="100%" style="table-layout: fixed;" data-attributes='%7B%22dropped%22%3Atrue%2C%22child%22%3Afalse%2C%22padding%22%3A%220%2C0%2C0%2C0%22%2C%22containerbackground%22%3A%22%23ffffff%22%7D'>
	<tr>
	  <td role="module-content"  valign="top" height="100%" style="padding: 0px 0px 0px 0px;" bgcolor="#ffffff"><div style="font-size:12px;line-height:150%;margin:0;text-align:center;">This email was sent by: Carcrew(Carcrew Technology Private Limited), &nbsp;W-22, Green Park, New Delhi</div> </td>
	</tr>
	</table>
	</td>
				</tr>
			  </table>
			</td>

		  </tr>
		</table>
	  </td></tr>
	</table>

									</tr></td>
								  </table>
								<!--[if (gte mso 9)|(IE)]>
							  </td>
							</td>
						  </table>
						<![endif]-->
						</td>
					  </tr>
					</table></td>
				  </tr>
				</table>
			  <!--[if (gte mso 9)|(IE)]>
			  </td>
			</tr>
		  </table>
		  <![endif]-->
		  </tr></td>
		  </table>
		</div>
	  </center>
	</body>
	</html>"""
	return html


def send_bill(cust_name,booking_id,cust_email,price_total,serviceitems,cust_number,filename):
	me = from_address
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')

	# booking = Bookings.objects.filter(id = dataid)[0]
	# name = booking.cust_name
	# booking_id = booking.booking_id
	# price_total = booking.price_total
	# serviceitems = booking.service_items
	# cust_email = booking.cust_email
	bill_estimate = "Bill"
	msg['From'] = me
	msg['To'] = cust_email

	#
	if booking_id != "":
		msg['Subject'] = "Job Completed! Booking ID: " + str(booking_id)
	else:
		msg['Subject'] = "Carcrew| Bill"

	html = html_to_send_bill_estimate(name=cust_name, booking_id=booking_id, bill_estimate=bill_estimate,total_amount=price_total, service_list=serviceitems,data_id= "")
	script = MIMEText(html, 'html')
	msg.attach(script)

	#

	script = MIMEText(html, 'html')
	msg.attach(script)
	part = MIMEApplication(open(filename, 'rb').read())
	part.add_header('Content-Disposition', 'attachment', filename='Invoice.pdf')
	msg.attach(part)

	conn = boto.ses.connect_to_region(region, aws_access_key_id=aws_access, aws_secret_access_key=aws_secret)
	result = conn.send_raw_email(msg.as_string())



# the attachment
def send_report(cust_name,booking_id,cust_email,filename):
	me = from_address
	msg = MIMEMultipart('alternative')

	bill_estimate = "Report"
	msg['From'] = me
	msg['To'] = cust_email

	#
	if booking_id != "":
		msg['Subject'] = "Inspection Report! Booking ID: " + str(booking_id)
	else:
		msg['Subject'] = "Carcrew | Inspection Report"

	html = html_to_send_report(name=cust_name, booking_id=booking_id)

	script = MIMEText(html, 'html')
	msg.attach(script)

	script = MIMEText(html, 'html')
	msg.attach(script)
	part = MIMEApplication(open(filename, 'rb').read())
	part.add_header('Content-Disposition', 'attachment', filename='Report.pdf')
	msg.attach(part)

	conn = boto.ses.connect_to_region(region, aws_access_key_id=aws_access, aws_secret_access_key=aws_secret)
	result = conn.send_raw_email(msg.as_string())



def bill_html(agent_name,agent_address,invoice_number,booking_id,created_date,tin_number,cin_number,stax_number,cust_name,cust_address,cust_locality,cust_city,cust_reg,cust_veh,service_items,vat_part_percent,vat_lube_percent,vat_consumable_percent,stax_percent,vat_part,vat_lube,vat_consumable,stax_amount,total,recommendation,logo,amount_paid,gst_number,gst_part_percent,gst_lube_percent,gst_consumable_percent,gst_service_percent,gst_18,gst_28,cust_odo,gst_type,state_of_supply,cust_gst):
	html = """<!DOCTYPE html>
<html id="bill-data" lang="en"><head>
	<style>
/* ==========================================================================
   Insert Your Bill Styles Below. All styles located in this file will
   override existing main.css stylesheets.
   ========================================================================== */
.actionables{
    /*background: #eaeaea;*/
    /*padding: 4%;*/
    margin-bottom: 2%;
    /*width: 100%;*/
    background: #FFF;
    /*height: 5%;*/
}

.button-row{
    padding: 3%;
}
.bill-btn{
    width: 300px;
    margin: 5px;

}

.view-pdf-box{
    /*border:1px solid #4a148c;*/
    /*width:100px;*/
    /*margin-left:50%;*/
    /*left:50px;*/

}
.invoice-box{
    max-width:800px;
    margin:auto;
    padding:30px;
    /*border:1px solid #eee;*/
    /*box-shadow:0 0 10px rgba(0, 0, 0, .15);*/
    font-size:16px;
    line-height:24px;
    font-family:'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    color:#555;
}

.invoice-box .company-name{
    font-size:16px!important;
    color:#555!important;
    line-height: 20px!important;
}

.invoice-box .bill-details{
    font-size:16px!important;
    color:#555!important;
    line-height: 10px!important;

}



.tax{
    font-size: 10px;
    line-height: 5px;
}


.invoice-box table{
    width:100%;
    line-height:inherit;
    text-align:left;
}

.invoice-box table td{
    padding:5px;
    vertical-align:top;
}

.invoice-box table tr td:nth-child(2){
    text-align:right;
}


body {
  background: rgb(204,204,204);
}

page {
  background: white;
  display: block;
  margin: 0 auto;
  margin-bottom: 0.5cm;
}
page[size="A4"] {
  width: 21cm;
  /*height: 29.7cm;*/
}
page[size="A4"][layout="portrait"] {
  width: 29.7cm;
  height: 21cm;
}
page[size="A3"] {
  width: 29.7cm;
  height: 42cm;
}
page[size="A3"][layout="portrait"] {
  width: 42cm;
  height: 29.7cm;
}
page[size="A5"] {
  width: 14.8cm;
  height: 21cm;
}
page[size="A5"][layout="portrait"] {
  width: 21cm;
  height: 14.8cm;
}
@media print {
  body, page {
    margin: 0;
    box-shadow: 0;
  }
}


.invoice-box .information tr td {
     text-align:left!important;
}
.invoice-box table tr.top table td{
    padding-bottom:0px;
    padding: 0px;
    line-height: 20px;
}

.invoice-box .customer-details td{
    padding: 0px!important;;
    padding-bottom: 0px!important;
    text-align: left!important;
}
.invoice-box table tr.top table td.title{
    font-size:45px;
    line-height:45px;
    color:#333;
}

.invoice-box table tr.information table td{
    padding-bottom:0px;
}

.invoice-box .agent-details td:nth-child(1){
    width: 50%;
}
.invoice-box .agent-details td:nth-child(2){
    width: 50%;
}

.invoice-box .information-cust td:nth-child(1){
    width: 50%;
}
.invoice-box .information-cust td:nth-child(2){
    width: 50%;
}
.invoice-box .information-cust .customer-details td:nth-child(1){
    width: 40%;
}
.invoice-box .information-cust .customer-details td:nth-child(2){
    width: 60%;
}

.invoice-box table thead.heading td{
    background:#eee;
    border-bottom:1px solid #ddd;
    font-weight:bold;
}

.invoice-box .parts-table td:nth-child(1){
    width: 40%;
}
.invoice-box .parts-table td:nth-child(2){
    width: 20%;
    text-align: center;
}
.invoice-box .parts-table td:nth-child(3){
    width: 20%;
    text-align: center;

}
.row{
    margin-bottom:5px;
}
.recommendation{
    margin-left: 10px;
}
.invoice-box .parts-table td:nth-child(4){
    width: 20%;
    text-align: right;

}

.invoice-box .summary td{
    text-align: right;
}

.invoice-box table tr.details td{
    padding-bottom:20px;
}

.invoice-box table tr.item td{
    border-bottom:1px solid #eee;
}

.invoice-box table tr.item.last td{
    border-bottom:none;
}


.invoice-box .summary{
    border-top:2px solid #eee;
}
.invoice-box table tr.total td:nth-child(1){
    border-top:2px solid #eee;
    font-weight:bold;
}

@media only screen and (max-width: 600px) {
    .invoice-box table tr.top table td{
        width:100%;
        display:block;
        text-align:center;
    }

    .invoice-box table tr.information table td{
        width:100%;
        display:block;
        text-align:center;
    }
}
	</style>
</head>
<body class="bill-page">
<page id="bill" class="" style="" size="">
	<div class="invoice-box">
		<!--<table cellpadding="0" cellspacing="0">-->
		<!--<tr class="top">-->
		<!--<td colspan="2">-->
		<table class="agent-details">
			<tr>
				<td class="title company-name">"""
	if logo:
		html += """<img id="bill-logo" src="https://www.carcrew.in/static/revamp/img/Bill%20Logos/Carcrew.png" style="width:100%; max-width:150px;"><br>"""
	else:
		html += """<img id="bill-logo" src="https://www.carcrew.in/static/revamp/img/Bill%20Logos/""" + string.replace(agent_name, ' ', '%20') + """.png" style="width:100%; max-width:150px;"><br>"""

	html += """<span id="agent-name">"""+ agent_name +"""</span><br>
					<span id="agent-address">"""+ agent_address +"""</span><br>
				</td>

				<td>
					<table class="bill-details">
						<tr class="reciept"><td>Invoice #: </td><td><span id="bill-number">"""+ str(invoice_number) +"""</span></td></tr>"""
	if booking_id !="":
		html += """<tr><td>Booking #: </td><td><span id="booking-id">"""+str(booking_id)+"""</span></td></tr>"""
	if created_date != "":
		html += """<tr><td>Created: </td><td><span id="bill-date">""" + str(created_date) +"""</span></td></tr>"""
	# if tin_number != "":
	# 	html += """<tr class="reciept tin"><td>TIN : </td><td><span id = "agent-tin">"""+tin_number+"""</span></td></tr>"""
	if cin_number != "":
		html += """<tr class="reciept cin"><td>CIN : </td><td><span id = "agent-cin">"""+cin_number+"""</span></td></tr>"""

	if gst_number != "":
		html += """<tr class="reciept cin"><td>GST : </td><td><span id = "agent-cin">"""+gst_number+"""</span></td></tr>"""

	# if stax_number != "":
	# 	html += """<tr class="reciept stax"><td>Service Tax : </td><td><span id = "agent-stax">"""+stax_number+"""</span></td></tr>"""

	html += """</table>
				</td>
			</tr>
		</table>
		<!--</td>-->
		<!--</tr>-->
		<table class="information information-cust">
			<tr>
				<!--<td colspan="2">-->
				<!--<table class="">-->
				<!--<tr>-->
				<td>
					<b>Customer Details:  </b><br>
					<table class="customer-details">
						<tr><td>&nbsp;&nbsp;Name </td><td><span id="cust-name">"""+cust_name+"""</span></td></tr>
						<tr><td>&nbsp;&nbsp;Address </td><td><span id="cust-address">"""+cust_address+"""</span>, <span id="cust-locality">"""+cust_locality+"""</span>, <span id="cust-city">"""+cust_city+"""</span></td></tr>
						<tr><td>&nbsp;&nbsp;State of Supply </td><td><span id="cust-city">"""+state_of_supply+"""</span></td></tr>"""
	if cust_gst != "" and cust_gst != None:
		html += """<tr><td>&nbsp;&nbsp;Customer GST </td><td><span id="cust-gst">"""+cust_gst+"""</span></td></tr>"""

	html +=				"""</table>
				</td>
				<td>
					<b>Vehicle Details: </b><br>
					<table class="customer-details">"""
	if cust_reg != "":
		html +="""<tr><td>&nbsp;&nbsp;Registration </td><td><span id="veh-reg">"""+str(cust_reg)+"""</span></td></tr>"""

	if cust_odo != "":
		html +="""<tr><td>&nbsp;&nbsp;Odometer </td><td><span id="veh-reg">"""+str(cust_odo)+"""</span></td></tr>"""

	if cust_veh != "":
		html += """<tr><td>&nbsp;&nbsp;Vehicle Name </td><td><span id="veh-name">"""+str(cust_veh)+"""</span></td></tr>"""

	html += """</table>
				</td>

			</tr>
		</table>
		<!--</td>-->
		<!--</tr>-->
		<!--</table>-->"""
	marker = 0
	if len(service_items):
		html2 = ''
		html3 = ''
		html4 = ''
		html2 += """<table class="parts-table">
			<thead class="heading">
			<td>
				Parts
			</td>
			<td>
				Units
			</td>
			<td>
				Unit Price
			</td>
			<td>
				Price
			</td>
			</thead>
			<tbody class="parts-list">"""

		for part in service_items:
			if (part['type'] == "Part" or part['type'] == "Lube" or part['type'] == "Consumable" or part['type'] == "Part18" or part['type'] == "Part28" or part['type'] == "Lube18" or part['type'] == "Lube28") and float(part['unit_price'])>0 :
				marker = 1
				html3 += """<tr class="item"><td>"""+part['name']+"""</td><td>"""+str(part['quantity'])+"""</td><td>"""+str(round((float(part['pre_tax_price'])/float(part['quantity'])),2))+"""</td><td>Rs. """+str(part['pre_tax_price'])+"""</td></tr>"""
		html4 += """</tbody></table>"""

	if marker ==1 :
		html += html2
		html += html3
		html += html4

	html += """<br>"""

	marker2 = 0
	if len(service_items):
		html5 = ''
		html6 = ''
		html7 = ''
		html5 += """<table class="service-table">
			<thead class="heading">
			<td>
				Services/Labour
			</td>
			<td>
				Price
			</td>
			</thead>

			<tbody class="service-list">"""

		for service in service_items:
			if (service['type'] == "Labour") and float(service['pre_tax_price']) > 0:
				marker2 = 1
				html6 += """<tr class="item"><td>"""+service['name']+"""</td><td>Rs. """+str(service['pre_tax_price'])+"""</td></tr>"""
		html7+="""</tbody></table>"""

	if marker2 == 1:
		html += html5
		html += html6
		html += html7

	if len(service_items):
		Discount = 0
		for service in service_items:
			if (service['type'] == "Discount"):
				Discount = Discount + float(service['pre_tax_price'])

	marker3 = 0

	if len(service_items):
		html8 = ''
		html9 = ''
		html10 = ''
		marker3 = 0
		html8 += """<table class="service-table">
			<thead class="heading">
			<td>
				Other Jobs Performed/Parts Replaced
			</td>
			</thead>
			<tbody class="service-list">"""
		for service in service_items:
			if float(service['pre_tax_price']) == 0:
				marker3 = 1
				html9 += """<tr class="item"><td>"""+service['name']+"""</td></tr>"""
		html10+="""</tbody></table>"""
	if marker3 == 1:
		html += html8
		html += html9
		html += html10
	html+="""<br>"""



	html+="""<table class="summary">"""
	# if tin_number != "":
	# 	html+="""<tr class="tax reciept">
	# 			<td>
	# 				VAT (Parts) @ <span id="vat-part-percent">"""+str(vat_part_percent)+"""</span>%: Rs. <span class="vat-part-amount">"""+str(vat_part)+"""</span>
	# 			</td>
	# 		</tr>
	# 		<tr class="tax reciept">
	# 			<td>
	# 				VAT (Lubes) @ <span id="vat-lube-percent">"""+str(vat_lube_percent)+"""</span>%: Rs. <span class="vat-lube-amount">"""+str(vat_lube)+"""</span>
	# 			</td>
	# 		</tr>
	# 		<tr class="tax reciept">
	# 			<td>
	# 				VAT (Consumables) @ <span id="vat-consumable-percent">"""+str(vat_consumable_percent)+"""</span>%: Rs. <span class="vat-consumable-amount">"""+str(vat_consumable)+"""</span>
	# 			</td>
	# 		</tr>"""
	# if stax_number != "":
	# 	html += """<tr class="tax reciept stax">
	# 			<td>
	# 				Service Tax + Krishi Kalyan Cess + Swachha Bharat Cess @ <span id="stax-percent">"""+str(stax_percent)+"""</span>%: Rs. <span class="stax-amount">"""+str(stax_amount)+"""</span>
	# 			</td>
	# 		</tr>"""

	if gst_number != "":
		if gst_type == "S":
			html += """<tr class="tax reciept">
							<td>
								CGST  @ <span id="vat-part-percent">""" + str(float(gst_part_percent)/2) + """</span>%: Rs. <span class="vat-part-amount">""" + str((float(gst_28))/2) + """</span>
							</td>
						</tr>
						<tr class="tax reciept">
							<td>
								CGST @ <span id="vat-lube-percent">""" + str(float(gst_lube_percent)/2) + """</span>%: Rs. <span class="vat-lube-amount">""" + str((float(gst_18))/2) + """</span>
							</td>
						</tr>"""
						# <tr class="tax reciept">
						# 	<td>
						# 		CGST  @ <span id="vat-consumable-percent">""" + str(float(gst_consumable_percent)/2) + """</span>%: Rs. <span class="vat-consumable-amount">""" + str(float(gst_consumable)/2) + """</span>
						# 	</td>
						# </tr>"""
						# <tr class="tax reciept">
						# 	<td>
						# 		CGST (Service) @ <span id="vat-lube-percent">""" + str(float(gst_service_percent)/2) + """</span>%: Rs. <span class="vat-lube-amount">""" + str(float(gst_service)/2) + """</span>
						# 	</td>
						# </tr>"""

			html += """<tr class="tax reciept">
									<td>
								SGST  @ <span id="vat-part-percent">""" + str(float(gst_part_percent)/2) + """</span>%: Rs. <span class="vat-part-amount">""" + str((float(gst_28))/2) + """</span>
									</td>
								</tr>
						<tr class="tax reciept">
							<td>
								SGST @ <span id="vat-lube-percent">""" + str(float(gst_lube_percent)/2) + """</span>%: Rs. <span class="vat-lube-amount">""" + str((float(gst_18))/2) + """</span>
							</td>
						</tr>"""
		else:
			html += """<tr class="tax reciept">
		    							<td>
		    								IGST  @ <span id="vat-part-percent">""" + str(
				float(gst_part_percent)) + """</span>%: Rs. <span class="vat-part-amount">""" + str(
				(float(gst_28))) + """</span>
		    							</td>
		    						</tr>
		    						<tr class="tax reciept">
		    							<td>
		    								IGST @ <span id="vat-lube-percent">""" + str(
				float(gst_lube_percent)) + """</span>%: Rs. <span class="vat-lube-amount">""" + str(
				(float(gst_18))) + """</span>
		    							</td>
		    						</tr>"""

		#     			<tr class="tax reciept">
			#     				<td>
			#     					SGST  @ <span id="vat-consumable-percent">""" + str(
			# float(gst_consumable_percent) / 2) + """</span>%: Rs. <span class="vat-consumable-amount">""" + str(
			# float(gst_consumable) / 2) + """</span>
			#     				</td>
			#     			</tr>"""
			# 				<tr class="tax reciept">
			#     				<td>
			#     					SGST (Service) @ <span id="vat-lube-percent">""" + str(
			# float(gst_service_percent) / 2) + """</span>%: Rs. <span class="vat-lube-amount">""" + str(
			# float(gst_service) / 2) + """</span>
			#     				</td>
			#     			</tr>"""


	html += """<tr class="total">
					<td>
						Total Amount: Rs.  <span id="cust-total">""" + str(round((float(total)+float(Discount)), 0)) + """</span>
					</td>
				</tr>"""

	if Discount > 0:
		html += """<tr class="total-2">
	    			<td>
	    				<b>Discount Amount: Rs.  <span id="cust-total">""" + str(round(float(Discount), 0)) + """ ("""+str(round((float(Discount)/(float(total)+float(Discount)))*100, 2))+"""%)</span></b>
	    			</td>
	    		</tr>"""

	html += """<tr class="total">
				<td>
					Final Amount: Rs.  <span id="cust-total">"""+str(round(float(total),0))+"""</span>
				</td>
			</tr>"""
	if float(amount_paid) != 0:
		print amount_paid
		# html +="""<hr>"""
		html += """<tr class="total-2">
					<td>
						Paid Amount: Rs.  <span id="cust-total">""" + str(round(float(amount_paid), 0)) + """</span>
					</td>
				</tr>"""

		html += """<tr class="total">
					<td>
						Due Amount: Rs.  <span id="cust-total">""" + str(round((float(total)-float(amount_paid)), 0)) + """</span>
					</td>
				</tr>"""
	html +="""</table>"""
	if recommendation != "" and recommendation != "null":
		html+="""<div class="recommendations">
			<div class="row">
				<b>Recommendations:</b>
			</div>
			<div class="row">
				<span class="recommendation">"""+recommendation+"""</span>
			</div>
		</div>"""
	html +="""<div style="text-align:center">This is a computer generated invoice and does not require any stamp or signature</div>"""
	html+="""</div>
</page>

</body>
</html>"""
	return html

def report_html(agent_name,agent_address,booking_id,created_date,cust_name,cust_address,cust_locality,cust_city,cust_reg,cust_veh,service_items,logo,cust_odo):
	html = """<!DOCTYPE html>
<html id="bill-data" lang="en"><head>
	<style>
/* ==========================================================================
   Insert Your Bill Styles Below. All styles located in this file will
   override existing main.css stylesheets.
   ========================================================================== */
.actionables{
    /*background: #eaeaea;*/
    /*padding: 4%;*/
    margin-bottom: 2%;
    /*width: 100%;*/
    background: #FFF;
    /*height: 5%;*/
}

.button-row{
    padding: 3%;
}
.bill-btn{
    width: 300px;
    margin: 5px;

}

.view-pdf-box{
    /*border:1px solid #4a148c;*/
    /*width:100px;*/
    /*margin-left:50%;*/
    /*left:50px;*/

}
.invoice-box{
    max-width:800px;
    margin:auto;
    padding:30px;
    /*border:1px solid #eee;*/
    /*box-shadow:0 0 10px rgba(0, 0, 0, .15);*/
    font-size:16px;
    line-height:24px;
    font-family:'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    color:#555;
}

.invoice-box .company-name{
    font-size:16px!important;
    color:#555!important;
    line-height: 20px!important;
}

.invoice-box .bill-details{
    font-size:16px!important;
    color:#555!important;
    line-height: 10px!important;

}



.tax{
    font-size: 10px;
    line-height: 5px;
}


.invoice-box table{
    width:100%;
    line-height:inherit;
    text-align:left;
}

.invoice-box table td{
    padding:5px;
    vertical-align:top;
}

.invoice-box table tr td:nth-child(2){
    text-align:right;
}


body {
  background: rgb(204,204,204);
}

page {
  background: white;
  display: block;
  margin: 0 auto;
  margin-bottom: 0.5cm;
}
page[size="A4"] {
  width: 21cm;
  /*height: 29.7cm;*/
}
page[size="A4"][layout="portrait"] {
  width: 29.7cm;
  height: 21cm;
}
page[size="A3"] {
  width: 29.7cm;
  height: 42cm;
}
page[size="A3"][layout="portrait"] {
  width: 42cm;
  height: 29.7cm;
}
page[size="A5"] {
  width: 14.8cm;
  height: 21cm;
}
page[size="A5"][layout="portrait"] {
  width: 21cm;
  height: 14.8cm;
}
@media print {
  body, page {
    margin: 0;
    box-shadow: 0;
  }
}


.invoice-box .information tr td {
     text-align:left!important;
}
.invoice-box table tr.top table td{
    padding-bottom:0px;
    padding: 0px;
    line-height: 20px;
}

.invoice-box .customer-details td{
    padding: 0px!important;;
    padding-bottom: 0px!important;
    text-align: left!important;
}
.invoice-box table tr.top table td.title{
    font-size:45px;
    line-height:45px;
    color:#333;
}

.invoice-box table tr.information table td{
    padding-bottom:0px;
}

.invoice-box .agent-details td:nth-child(1){
    width: 50%;
}
.invoice-box .agent-details td:nth-child(2){
    width: 50%;
}

.invoice-box .information-cust td:nth-child(1){
    width: 50%;
}
.invoice-box .information-cust td:nth-child(2){
    width: 50%;
}
.invoice-box .information-cust .customer-details td:nth-child(1){
    width: 40%;
}
.invoice-box .information-cust .customer-details td:nth-child(2){
    width: 60%;
}

.invoice-box table thead.heading td{
    background:#eee;
    border-bottom:1px solid #ddd;
    font-weight:bold;
}

.invoice-box .parts-table td:nth-child(1){
    width: 40%;
}
.invoice-box .parts-table td:nth-child(2){
    width: 20%;
    text-align: center;
}
.invoice-box .parts-table td:nth-child(3){
    width: 20%;
    text-align: center;

}
.row{
    margin-bottom:5px;
}
.recommendation{
    margin-left: 10px;
}
.invoice-box .parts-table td:nth-child(4){
    width: 20%;
    text-align: right;

}

.invoice-box .summary td{
    text-align: right;
}

.invoice-box table tr.details td{
    padding-bottom:20px;
}

.invoice-box table tr.item td{
    border-bottom:1px solid #eee;
}

.invoice-box table tr.item.last td{
    border-bottom:none;
}


.invoice-box .summary{
    border-top:2px solid #eee;
}
.invoice-box table tr.total td:nth-child(1){
    border-top:2px solid #eee;
    font-weight:bold;
}

@media only screen and (max-width: 600px) {
    .invoice-box table tr.top table td{
        width:100%;
        display:block;
        text-align:center;
    }

    .invoice-box table tr.information table td{
        width:100%;
        display:block;
        text-align:center;
    }
}
	</style>
</head>
<body class="bill-page">
<page id="bill" class="" style="" size="">
	<div class="invoice-box">
		<!--<table cellpadding="0" cellspacing="0">-->
		<!--<tr class="top">-->
		<!--<td colspan="2">-->
		<table class="agent-details">
			<tr>
				<td class="title company-name">"""
	if logo:
		html += """<img id="bill-logo" src="https://www.carcrew.in/static/revamp/img/Bill%20Logos/ClickGarage.png" style="width:100%; max-width:150px;"><br>"""
	else:
		html += """<img id="bill-logo" src="https://www.carcrew.in/static/revamp/img/Bill%20Logos/""" + string.replace(agent_name, ' ', '%20') + """.png" style="width:100%; max-width:150px;"><br>"""

	html += """<span id="agent-name">"""+ agent_name +"""</span><br>
					<span id="agent-address">"""+ agent_address +"""</span><br>
				</td>

				<td>
					<table class="bill-details">"""
	if booking_id !="":
		html += """<tr><td>Booking #: </td><td><span id="booking-id">"""+str(booking_id)+"""</span></td></tr>"""
	if created_date != "":
		html += """<tr><td>Created: </td><td><span id="bill-date">""" + str(created_date) +"""</span></td></tr>"""
	# if tin_number != "":
	# 	html += """<tr class="reciept tin"><td>TIN : </td><td><span id = "agent-tin">"""+tin_number+"""</span></td></tr>"""

	# if stax_number != "":
	# 	html += """<tr class="reciept stax"><td>Service Tax : </td><td><span id = "agent-stax">"""+stax_number+"""</span></td></tr>"""

	html += """</table>
				</td>
			</tr>
		</table>
		<!--</td>-->
		<!--</tr>-->
		<table class="information information-cust">
			<tr>
				<!--<td colspan="2">-->
				<!--<table class="">-->
				<!--<tr>-->
				<td>
					<b>Customer Details:  </b><br>
					<table class="customer-details">
						<tr><td>&nbsp;&nbsp;Name </td><td><span id="cust-name">"""+cust_name+"""</span></td></tr>
						<tr><td>&nbsp;&nbsp;Address </td><td><span id="cust-address">"""+cust_address+"""</span>, <span id="cust-locality">"""+cust_locality+"""</span>, <span id="cust-city">"""+cust_city+"""</span></td></tr>
					</table>
				</td>
				<td>
					<b>Vehicle Details: </b><br>
					<table class="customer-details">"""
	if cust_reg != "":
		html +="""<tr><td>&nbsp;&nbsp;Registration </td><td><span id="veh-reg">"""+str(cust_reg)+"""</span></td></tr>"""

	if cust_odo != "":
		html +="""<tr><td>&nbsp;&nbsp;Odometer </td><td><span id="veh-reg">"""+str(cust_odo)+"""</span></td></tr>"""

	if cust_veh != "":
		html += """<tr><td>&nbsp;&nbsp;Vehicle Name </td><td><span id="veh-name">"""+str(cust_veh)+"""</span></td></tr>"""

	html += """</table>
				</td>

			</tr>
		</table>
		<!--</td>-->
		<!--</tr>-->
		<!--</table>-->"""
	if len(service_items):
		html += """<table class="parts-table">
			<thead class="heading">
			<td>
				Check List Item
			</td>
			<td>
				Vehicle Inspection Status
			</td>
			</thead>
			<tbody class="parts-list">"""

		for part in service_items:
			if (part['Preok']):
				html += """<tr class="item"><td>"""+part['Job']+"""</td><td style="background: green;"></td></tr>"""
			else:
				html += """<tr class="item"><td>""" + part['Job'] + """</td><td style="background:red;"></td></tr>"""
		html += """</tbody></table>"""

	html += """<br>"""





	html+="""</div>
</page>

</body>
</html>"""
	return html
