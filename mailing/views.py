# Create your views here.


import requests
import smtplib
import urllib2
from datetime import datetime

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEBase import MIMEBase
from email import Encoders

helpline_number = "09953008804"
key = "ab33f626-fba5-4bff-9a2b-68a7e9eed43c"
sendername = "CLKGRG"


def send_sms(type,to,message):
	url = "http://sms.hspsms.com:8090/sendSMS?username=clickgarage&message="+ message + "&sendername=" + sendername+ "&smstype=" + type + "&numbers=" + to + "&apikey=" + key
	r = urllib2.urlopen(url)

def send_booking_sms(to_name, to, date, pick_time_start, booking_id):
	message = "Hi "+ to_name +"! Your ClickGarage appointment has been confirmed. Appointment date: " +date + ", Pick up time: "  + pick_time_start  + ". For further assistance, please contact us on " + helpline_number + " and quote your booking ID: " + booking_id + "."
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def send_cancel_sms(to_name, to, booking_id):
	message = "Hi "+ to_name +"! Your ClickGarage appointment for booking id :#"+booking_id+"has been cancelled."
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
	message = "Hi "+to_name+", your car was dropped by our driver. It was a pleasure serving you. Kindly share your valuable feedback on our website www.clickgarage.in/feedback.html"
	message = message.replace(" ","+")
	send_sms("TRANS",to,message)

def prompt(prompt):
    return raw_input(prompt).strip()


import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = 'email-smtp.us-west-2.amazonaws.com'
smtp_username = 'AKIAJ4U5VOXPWBT37X4A'
smtp_password = 'AkJxDBO/FOsxkF1Ucd1EhblV5DTAVLpFfqWQv/KI2gn7'
from_address = "bookings@clickgarage.in"
helpline_number = "09717353148"


def send_booking_email(to_address,to_name,time_start,date,booking_id):
	me = from_address
	you = to_address

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Confirmation! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """\
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
	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Your ClickGarage booking has been confirmed. Pick up time chosen by you is """+ time_start +""" on """+ date +""". If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</span></span></p>

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
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>
				                                    
				                                    
				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Facebook</a>
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
				                                            <a href="http://www.clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>
				                                    
				                                    
				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
				                                            <a href="http://www.clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Website</a>
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
	Email : info@clickgarage.in | Phone No. : +91-9717353148<br>
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

#send_booking(to_address="y.shashwat@gmail.com",to_name="Shashwat",service="Servicing",time_start="9:00AM",time_end="10:00AM",date="16-Aug-2015",booking_id="0001")

def send_booking_email(to_address,to_name,time_start,date,booking_id):
	me = from_address
	you = to_address

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Confirmation! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = you

	html = """\
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
	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Your ClickGarage booking has been confirmed. Pick up time chosen by you is """+ time_start +""" on """+ date +""". If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</span></span></p>

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
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Facebook</a>
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
				                                            <a href="http://www.clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
				                                            <a href="http://www.clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Website</a>
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
	Email : info@clickgarage.in | Phone No. : +91-9717353148<br>
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

def send_cancel_email(to_address,to_name,booking_id):
	me = from_address
	you = to_address


	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Booking Cancelled! Booking ID: " + booking_id
	msg['From'] = me
	msg['To'] = ', '.join(you)

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

	                            <h1>Appointment Cancelled</h1>

	<h3><br>
	Booking ID #"""+booking_id+"""</h3>
	&nbsp;


	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Hi """+to_name+""",</span></span></p>
	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">As requested your ClickGarage booking has been cancelled. If further assistance is needed, please contact us on """+helpline_number+""" and quote your booking confirmation number """+booking_id+""".</span></span></p>

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
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Facebook</a>
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
				                                            <a href="http://www.clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>


				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
				                                            <a href="http://www.clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Website</a>
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
	Email : info@clickgarage.in | Phone No. : +91-9717353148<br>
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

def send_feedback_bill(to_address,to_name,service,booking_id,path_file,amount):
	me = from_address
	you = to_address

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
	                        
	                            <h1>Order Complete!</h1>

	<h3><br>
	Booking ID #"""+booking_id+"""</h3>
	&nbsp;

	<p dir="ltr" style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"><span id="docs-internal-guid-a5acf9b5-2d61-8cb0-61dd-92f1d4247aeb"><span style="background-color: transparent;color: #000000;font-family: arial;font-size: 14.6666666666667px;vertical-align: baseline;white-space: pre-wrap;">Hello """+to_name+"""! Your ClickGarage booking for """+service+""" is complete. Your total bill amount was """+amount+""". It was a pleasure serving you. Kindly spare some time to share your valuable feedback.</span></span></p>
<title>ClickGarage Feedback</title>
<link rel="stylesheet" type="text/css" href="./ClickGarage Feedback - Google_files/css">

<link href="./ClickGarage Feedback - Google_files/3565662838-formview_st_ltr.css" type="text/css" rel="stylesheet">
<style type="text/css">
body {
  background-color: rgb(231,238,247);
  background-image: url('https://lh6.googleusercontent.com/oTFrRPWA3IYPhWvtqzovZe6JtZwolemRuswfUJd-pygIazb3NjD2Y-8sKbVLe1cDZa9VEA');
  background-repeat: repeat;
  background-position: center top;
}

.ss-form-container, .ss-resp-card {
  background-color: rgb(234,234,234);
}

.ss-footer, .ss-response-footer {
  background-color: rgb(234,234,234);
}

.ss-grid-row-odd {
  background-color: rgb(221,221,221);
}

.ss-form-container, .ss-resp-card {
  border-color: rgb(77,91,148);
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
  height: auto;
  text-align: left;
}

.ss-header-image-image {
  background-image: url('https://lh3.googleusercontent.com/dLRTwOgdY65Sy5fcX35J1XVwsVEl8Hdupp5GEQ_CEd_-5sP6AWPWto-6dv5invyr0h42CA');
}

.ss-header-image-sizer {
  padding-top: 33.333%;
}

.ss-item {
  font-size: 1.080rem;
}

.ss-choices {
  font-size: 1.000rem;
}

body {
  font-family: "Roboto";
  color: rgb(106,106,106);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-record-username-message {
  font-family: "Roboto";
  color: rgb(106,106,106);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-form-title {
  font-family: "Raleway";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 2.460rem;
  font-style: normal;
}

.ss-confirmation {
  font-family: "Raleway";
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
  color: rgb(106,106,106);
  font-weight: 400;
  font-size: 1.080rem;
  font-style: normal;
}

.ss-q-title {
  font-family: "Lato";
  color: rgb(80,80,80);
  font-weight: 700;
  font-size: 1.080rem;
  font-style: normal;
  padding-top: 10px;
}

.ss-embeddable-object-container .ss-q-title {
  font-family: "Lato";
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
  font-family: "Lato";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.error-message, .required-message, .ss-required-asterisk {
  font-family: "Roboto";
  color: rgb(195,55,19);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-send-email-receipt {
  font-family: "Lato";
  color: rgb(80,80,80);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: normal;
}

.ss-password-warning {
  font-family: "Arial";
  color: rgb(106,106,106);
  font-weight: 400;
  font-size: 1.000rem;
  font-style: italic;
}

.disclaimer {
  font-family: "Arial";
  color: rgb(106,106,106);
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
  color: rgb(247,0,0);
}

input[type='text'], input:not([type]), textarea {
  font-size: 1.000rem;
}

.error, .required, .errorbox-bad {
  border-color: rgb(195,55,19);
}

.jfk-progressBar-nonBlocking .progress-bar-thumb {
  background-color: rgb(140,140,140);
}

.ss-logo-image {
  background-image: url('//ssl.gstatic.com/docs/forms/forms_logo_small_dark.png');
  background-size: 108px 21px;
  width: 108px;
  height: 21px;
}

@media screen and (-webkit-device-pixel-ratio: 2) {
.ss-logo-image {
  background-image: url('//ssl.gstatic.com/docs/forms/forms_logo_small_dark_2x.png');
}
}

</style>


<link href="./ClickGarage Feedback - Google_files/3145455273-mobile_formview_st_ltr.css" type="text/css" rel="stylesheet" media="screen and (max-device-width: 721px)">

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
<link rel="alternate" type="text/xml+oembed" href="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/oembed?url=https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/viewform&format=xml">
<meta property="og:title" content="ClickGarage Feedback"><meta property="og:type" content="article"><meta property="og:site_name" content="Google Docs"><meta property="og:url" content="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/viewform?usp=embed_facebook"><meta property="og:image" content="https://lh5.googleusercontent.com/U3FRsGPiMtRSKmrp7WbuUpo6ekPESXFGLenkB541SCKOyt_GDNKXV9PKGmp5KQz9YgI=w1200-h630-p"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="player"><meta name="twitter:title" content="ClickGarage Feedback"><meta name="twitter:url" content="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/viewform?usp=embed_twitter"><meta name="twitter:image" content="https://lh5.googleusercontent.com/U3FRsGPiMtRSKmrp7WbuUpo6ekPESXFGLenkB541SCKOyt_GDNKXV9PKGmp5KQz9YgI=w435-h251-p-b1-c0x00999999"><meta name="twitter:player:width" content="435"><meta name="twitter:player:height" content="251"><meta name="twitter:player" content="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/viewform?embedded=true&amp;usp=embed_twitter"><meta name="twitter:description" content="Google Drive"><meta name="twitter:site" content="@googledocs">
<script type="text/javascript" src="chrome-extension://bfbmjmiodbnnpllbbbfblcplfjjepjdn/js/injected.js"></script><style type="text/css" id="GINGER_SOFTWARE_style">.GINGER_SOFTWARE_noMark { background : transparent; }  .GINGER_SOFTWARE_wrapper{ position: absolute; overflow: hidden; margin: 0px; padding: 0px; border: 0px solid transparent } .GINGER_SOFTWARE_contour { position : absolute; margin: 0px; }  .GINGER_SOFTWARE_richText { margin : 0px; padding-bottom: 3px; border-width: 0px; border-color: transparent; display: block; color: transparent; -webkit-text-fill-color: transparent; overflow: hidden; white-space: pre-wrap;}  .GINGER_SOFTWARE_inputWrapper .GINGER_SOFTWARE_richText {position: absolute;}  .GINGER_SOFTWARE_canvas { display:none; background-repeat:no-repeat;}  .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark {border-top-left-radius:2px; border-top-right-radius:2px; border-bottom-right-radius:2px; border-bottom-left-radius:2px;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhFQ0Y2OENGMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhFQ0Y2OEQwMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEVDRjY4Q0QzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEVDRjY4Q0UzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5RRxRxAAAAD0lEQVR42mK48+w7QIABAAVbAroowN08AAAAAElFTkSuQmCC)!important;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling.GINGER_SOFTWARE_synonym, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark.GINGER_SOFTWARE_synonym {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAKT2lDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjanVNnVFPpFj333vRCS4iAlEtvUhUIIFJCi4AUkSYqIQkQSoghodkVUcERRUUEG8igiAOOjoCMFVEsDIoK2AfkIaKOg6OIisr74Xuja9a89+bN/rXXPues852zzwfACAyWSDNRNYAMqUIeEeCDx8TG4eQuQIEKJHAAEAizZCFz/SMBAPh+PDwrIsAHvgABeNMLCADATZvAMByH/w/qQplcAYCEAcB0kThLCIAUAEB6jkKmAEBGAYCdmCZTAKAEAGDLY2LjAFAtAGAnf+bTAICd+Jl7AQBblCEVAaCRACATZYhEAGg7AKzPVopFAFgwABRmS8Q5ANgtADBJV2ZIALC3AMDOEAuyAAgMADBRiIUpAAR7AGDIIyN4AISZABRG8lc88SuuEOcqAAB4mbI8uSQ5RYFbCC1xB1dXLh4ozkkXKxQ2YQJhmkAuwnmZGTKBNA/g88wAAKCRFRHgg/P9eM4Ors7ONo62Dl8t6r8G/yJiYuP+5c+rcEAAAOF0ftH+LC+zGoA7BoBt/qIl7gRoXgugdfeLZrIPQLUAoOnaV/Nw+H48PEWhkLnZ2eXk5NhKxEJbYcpXff5nwl/AV/1s+X48/Pf14L7iJIEyXYFHBPjgwsz0TKUcz5IJhGLc5o9H/LcL//wd0yLESWK5WCoU41EScY5EmozzMqUiiUKSKcUl0v9k4t8s+wM+3zUAsGo+AXuRLahdYwP2SycQWHTA4vcAAPK7b8HUKAgDgGiD4c93/+8//UegJQCAZkmScQAAXkQkLlTKsz/HCAAARKCBKrBBG/TBGCzABhzBBdzBC/xgNoRCJMTCQhBCCmSAHHJgKayCQiiGzbAdKmAv1EAdNMBRaIaTcA4uwlW4Dj1wD/phCJ7BKLyBCQRByAgTYSHaiAFiilgjjggXmYX4IcFIBBKLJCDJiBRRIkuRNUgxUopUIFVIHfI9cgI5h1xGupE7yAAygvyGvEcxlIGyUT3UDLVDuag3GoRGogvQZHQxmo8WoJvQcrQaPYw2oefQq2gP2o8+Q8cwwOgYBzPEbDAuxsNCsTgsCZNjy7EirAyrxhqwVqwDu4n1Y8+xdwQSgUXACTYEd0IgYR5BSFhMWE7YSKggHCQ0EdoJNwkDhFHCJyKTqEu0JroR+cQYYjIxh1hILCPWEo8TLxB7iEPENyQSiUMyJ7mQAkmxpFTSEtJG0m5SI+ksqZs0SBojk8naZGuyBzmULCAryIXkneTD5DPkG+Qh8lsKnWJAcaT4U+IoUspqShnlEOU05QZlmDJBVaOaUt2ooVQRNY9aQq2htlKvUYeoEzR1mjnNgxZJS6WtopXTGmgXaPdpr+h0uhHdlR5Ol9BX0svpR+iX6AP0dwwNhhWDx4hnKBmbGAcYZxl3GK+YTKYZ04sZx1QwNzHrmOeZD5lvVVgqtip8FZHKCpVKlSaVGyovVKmqpqreqgtV81XLVI+pXlN9rkZVM1PjqQnUlqtVqp1Q61MbU2epO6iHqmeob1Q/pH5Z/YkGWcNMw09DpFGgsV/jvMYgC2MZs3gsIWsNq4Z1gTXEJrHN2Xx2KruY/R27iz2qqaE5QzNKM1ezUvOUZj8H45hx+Jx0TgnnKKeX836K3hTvKeIpG6Y0TLkxZVxrqpaXllirSKtRq0frvTau7aedpr1Fu1n7gQ5Bx0onXCdHZ4/OBZ3nU9lT3acKpxZNPTr1ri6qa6UbobtEd79up+6Ynr5egJ5Mb6feeb3n+hx9L/1U/W36p/VHDFgGswwkBtsMzhg8xTVxbzwdL8fb8VFDXcNAQ6VhlWGX4YSRudE8o9VGjUYPjGnGXOMk423GbcajJgYmISZLTepN7ppSTbmmKaY7TDtMx83MzaLN1pk1mz0x1zLnm+eb15vft2BaeFostqi2uGVJsuRaplnutrxuhVo5WaVYVVpds0atna0l1rutu6cRp7lOk06rntZnw7Dxtsm2qbcZsOXYBtuutm22fWFnYhdnt8Wuw+6TvZN9un2N/T0HDYfZDqsdWh1+c7RyFDpWOt6azpzuP33F9JbpL2dYzxDP2DPjthPLKcRpnVOb00dnF2e5c4PziIuJS4LLLpc+Lpsbxt3IveRKdPVxXeF60vWdm7Obwu2o26/uNu5p7ofcn8w0nymeWTNz0MPIQ+BR5dE/C5+VMGvfrH5PQ0+BZ7XnIy9jL5FXrdewt6V3qvdh7xc+9j5yn+M+4zw33jLeWV/MN8C3yLfLT8Nvnl+F30N/I/9k/3r/0QCngCUBZwOJgUGBWwL7+Hp8Ib+OPzrbZfay2e1BjKC5QRVBj4KtguXBrSFoyOyQrSH355jOkc5pDoVQfujW0Adh5mGLw34MJ4WHhVeGP45wiFga0TGXNXfR3ENz30T6RJZE3ptnMU85ry1KNSo+qi5qPNo3ujS6P8YuZlnM1VidWElsSxw5LiquNm5svt/87fOH4p3iC+N7F5gvyF1weaHOwvSFpxapLhIsOpZATIhOOJTwQRAqqBaMJfITdyWOCnnCHcJnIi/RNtGI2ENcKh5O8kgqTXqS7JG8NXkkxTOlLOW5hCepkLxMDUzdmzqeFpp2IG0yPTq9MYOSkZBxQqohTZO2Z+pn5mZ2y6xlhbL+xW6Lty8elQfJa7OQrAVZLQq2QqboVFoo1yoHsmdlV2a/zYnKOZarnivN7cyzytuQN5zvn//tEsIS4ZK2pYZLVy0dWOa9rGo5sjxxedsK4xUFK4ZWBqw8uIq2Km3VT6vtV5eufr0mek1rgV7ByoLBtQFr6wtVCuWFfevc1+1dT1gvWd+1YfqGnRs+FYmKrhTbF5cVf9go3HjlG4dvyr+Z3JS0qavEuWTPZtJm6ebeLZ5bDpaql+aXDm4N2dq0Dd9WtO319kXbL5fNKNu7g7ZDuaO/PLi8ZafJzs07P1SkVPRU+lQ27tLdtWHX+G7R7ht7vPY07NXbW7z3/T7JvttVAVVN1WbVZftJ+7P3P66Jqun4lvttXa1ObXHtxwPSA/0HIw6217nU1R3SPVRSj9Yr60cOxx++/p3vdy0NNg1VjZzG4iNwRHnk6fcJ3/ceDTradox7rOEH0x92HWcdL2pCmvKaRptTmvtbYlu6T8w+0dbq3nr8R9sfD5w0PFl5SvNUyWna6YLTk2fyz4ydlZ19fi753GDborZ752PO32oPb++6EHTh0kX/i+c7vDvOXPK4dPKy2+UTV7hXmq86X23qdOo8/pPTT8e7nLuarrlca7nuer21e2b36RueN87d9L158Rb/1tWeOT3dvfN6b/fF9/XfFt1+cif9zsu72Xcn7q28T7xf9EDtQdlD3YfVP1v+3Njv3H9qwHeg89HcR/cGhYPP/pH1jw9DBY+Zj8uGDYbrnjg+OTniP3L96fynQ89kzyaeF/6i/suuFxYvfvjV69fO0ZjRoZfyl5O/bXyl/erA6xmv28bCxh6+yXgzMV70VvvtwXfcdx3vo98PT+R8IH8o/2j5sfVT0Kf7kxmTk/8EA5jz/GMzLdsAAAAgY0hSTQAAeiUAAICDAAD5/wAAgOkAAHUwAADqYAAAOpgAABdvkl/FRgAAABJJREFUeNpi+P9gEwAAAP//AwAFcwKS3d7BnwAAAABJRU5ErkJggg==)!important;} .GINGER_SOFTWARE_control .GINGER_SOFTWARE_correct.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_SpellingCorrect.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_spelling.GINGER_SOFTWARE_noSuggestion, .GINGER_SOFTWARE_control .GINGER_SOFTWARE_mark.GINGER_SOFTWARE_noSuggestion {background-image:url(data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyBpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMC1jMDYwIDYxLjEzNDc3NywgMjAxMC8wMi8xMi0xNzozMjowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNSBXaW5kb3dzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjhFQ0Y2OENGMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjhFQ0Y2OEQwMzE5OTExRTI4NjMxOTExNTUyMDhEMDMwIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6OEVDRjY4Q0QzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6OEVDRjY4Q0UzMTk5MTFFMjg2MzE5MTE1NTIwOEQwMzAiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5RRxRxAAAAD0lEQVR42mK48+w7QIABAAVbAroowN08AAAAAElFTkSuQmCC)!important;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_correct, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_SpellingCorrect, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_spelling, .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_mark {position:relative; background-image:none!important;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightLeft { position : absolute; left:-2px; top:0px; bottom:0px; width:2px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightRight { position : absolute; right:-2px; top:0px; bottom:0px; width:2px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightTop { position : absolute; left:0px; right:0px; top:-2px; height:3px;} .GINGER_SOFTWARE_richText .GINGER_SOFTWARE_markHighlightBottom { position : absolute; left:0px; right:0px; bottom:-2px; height:3px;}</style></head>
<body dir="ltr" class="ss-base-body" ginger_software_stylesheet="true" ginger_software_doc="true"><div itemscope="" itemtype="http://schema.org/CreativeWork/FormObject"><meta itemprop="name" content="ClickGarage Feedback">


<meta itemprop="url" content="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/viewform">
<meta itemprop="embedUrl" content="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/viewform?embedded=true">
<meta itemprop="faviconUrl" content="https://ssl.gstatic.com/docs/spreadsheets/forms/favicon_jfk2.png">




<div class="ss-form-container"><div class="ss-header-image-container"><div class="ss-header-image-image"><div class="ss-header-image-sizer"></div></div></div>
<div class="ss-top-of-page"><div class="ss-form-heading"><h1 class="ss-form-title" dir="ltr">ClickGarage Feedback</h1>


<div class="ss-required-asterisk" aria-hidden="true">*Required</div></div></div>
<div class="ss-form"><form action="https://docs.google.com/forms/d/1Re8S1yri4Dwg211xxGd5WJXP_OeZKGGy6PP38VGdflg/formResponse" method="POST" id="ss-form" target="_self" onsubmit=""><ol role="list" class="ss-question-list" style="padding-left: 0">
<div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_171841266"><div class="ss-q-title" style="padding-top:10px;">Booking ID
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<input type="text" name="entry.171841266" value="""+booking_id+""" readonly class="ss-q-short" id="entry_171841266" dir="auto" aria-label="Booking ID  " aria-required="true" required="" title="">
<div class="error-message" id="1783234593_errorMessage"></div>
<div class="required-message"></div>
</div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-radio"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1646158373"><div class="ss-q-title"  style="padding-top:10px;">1. Did the driver reach on promised time?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices" role="radiogroup" aria-label="Did the driver reach on promised time?  "style="list-style-type: none; padding-top:10px;">
<li class="ss-choice-item"  style="display:inline-block;"><label><span class="ss-choice-item-control goog-inline-block"><input type="radio" name="entry.881079079" value="Yes" id="group_881079079_1" role="radio" class="ss-q-radio" aria-label="Yes" required="" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> 
<li class="ss-choice-item" style="display:inline-block; margin-left:40px;"><label><span class="ss-choice-item-control goog-inline-block"><input type="radio" name="entry.881079079" value="No" id="group_881079079_2" role="radio" class="ss-q-radio" aria-label="No" required="" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li>
</ul>
<div class="error-message" id="1646158373_errorMessage"></div>
<div class="required-message"></div></div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-radio"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1454398340"><div class="ss-q-title"  style="padding-top:10px;">2. Was the driver courteous in receiving the car?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices" role="radiogroup" aria-label="Was the driver courteous in receiving the car?  " style="list-style-type: none; padding-top:10px;">
<li class="ss-choice-item" style="display:inline-block;"><label><span class="ss-choice-item-control goog-inline-block"><input type="radio" name="entry.2009686381" value="Yes" id="group_2009686381_1" role="radio" class="ss-q-radio" aria-label="Yes" required="" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> 
<li class="ss-choice-item" style="display:inline-block; margin-left:40px;"><label><span class="ss-choice-item-control goog-inline-block"><input type="radio" name="entry.2009686381" value="No" id="group_2009686381_2" role="radio" class="ss-q-radio" aria-label="No" required="" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li>
</ul>
<div class="error-message" id="1454398340_errorMessage"></div>
<div class="required-message"></div></div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_511078146"><div class="ss-q-title"  style="padding-top:10px;">3. How would you rate the quality of the washing and cleaning of your car?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_1942041656"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1942041656_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How would you rate the quality of the washing and cleaning of your car?  Select a value from a range from 1,Bad, to 10,Very Good,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="1" id="group_1942041656_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="2" id="group_1942041656_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="3" id="group_1942041656_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="4" id="group_1942041656_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="5" id="group_1942041656_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="6" id="group_1942041656_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="7" id="group_1942041656_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="8" id="group_1942041656_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="9" id="group_1942041656_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1942041656" value="10" id="group_1942041656_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Very Good</td></tr></tbody></table>
<div class="required-message"></div></div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1919695574"><div class="ss-q-title"  style="padding-top:10px;">4. How do you rate the overall interaction and the experience?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_1158601023"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_1158601023_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How do you rate the overall interaction and the experience?  Select a value from a range from 1,Bad, to 10,Very Good,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="1" id="group_1158601023_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="2" id="group_1158601023_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="3" id="group_1158601023_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="4" id="group_1158601023_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="5" id="group_1158601023_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="6" id="group_1158601023_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="7" id="group_1158601023_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="8" id="group_1158601023_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="9" id="group_1158601023_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.1158601023" value="10" id="group_1158601023_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Very Good</td></tr></tbody></table>
<div class="required-message"></div></div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-scale"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_977653122"><div class="ss-q-title"  style="padding-top:10px;">5. How would you rate us on the overall pickup &amp; drop experience?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<table border="0" cellpadding="5" cellspacing="0" id="entry_265833614"><tbody><tr aria-hidden="true"><td class="ss-scalenumbers"></td>
<td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_1">1</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_2">2</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_3">3</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_4">4</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_5">5</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_6">6</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_7">7</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_8">8</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_9">9</label></td> <td class="ss-scalenumbers"><label class="ss-scalenumber" for="group_265833614_10">10</label></td>
<td class="ss-scalenumbers"></td></tr>
<tr role="radiogroup" aria-label="How would you rate us on the overall pickup &amp; drop experience?  Select a value from a range from 1,Bad, to 10,Very Good,."><td class="ss-scalerow ss-leftlabel"><div aria-hidden="true" class="aria-todo">Bad</div></td>
<td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="1" id="group_265833614_1" role="radio" class="ss-q-radio" aria-label="1" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="2" id="group_265833614_2" role="radio" class="ss-q-radio" aria-label="2" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="3" id="group_265833614_3" role="radio" class="ss-q-radio" aria-label="3" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="4" id="group_265833614_4" role="radio" class="ss-q-radio" aria-label="4" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="5" id="group_265833614_5" role="radio" class="ss-q-radio" aria-label="5" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="6" id="group_265833614_6" role="radio" class="ss-q-radio" aria-label="6" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="7" id="group_265833614_7" role="radio" class="ss-q-radio" aria-label="7" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="8" id="group_265833614_8" role="radio" class="ss-q-radio" aria-label="8" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="9" id="group_265833614_9" role="radio" class="ss-q-radio" aria-label="9" required="" aria-required="true"></div></td> <td class="ss-scalerow"><div class="ss-scalerow-fieldcell"><input type="radio" name="entry.265833614" value="10" id="group_265833614_10" role="radio" class="ss-q-radio" aria-label="10" required="" aria-required="true"></div></td>
<td class="ss-scalerow ss-rightlabel" aria-hidden="true">Very Good</td></tr></tbody></table>
<div class="required-message"></div></div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item ss-item-required ss-radio"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_11908173"><div class="ss-q-title"  style="padding-top:10px;">6. Will you recommend our services to other?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" aria-hidden="true">*</span></div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>

<ul class="ss-choices" role="radiogroup" aria-label="Will you recommend our services to other?  " style="list-style-type: none; padding-top:10px;">
<li class="ss-choice-item" style="display:inline-block;"><label><span class="ss-choice-item-control goog-inline-block"><input type="radio" name="entry.111177002" value="Yes" id="group_111177002_1" role="radio" class="ss-q-radio" aria-label="Yes" required="" aria-required="true"></span>
<span class="ss-choice-label">Yes</span>
</label></li> 
<li class="ss-choice-item" style="display:inline-block; margin-left:40px;"><label><span class="ss-choice-item-control goog-inline-block"><input type="radio" name="entry.111177002" value="No" id="group_111177002_2" role="radio" class="ss-q-radio" aria-label="No" required="" aria-required="true"></span>
<span class="ss-choice-label">No</span>
</label></li>
</ul>
<div class="error-message" id="11908173_errorMessage"></div>
<div class="required-message"></div></div></div></div> <div class="ss-form-question errorbox-good" role="listitem">
<div dir="auto" class="ss-item  ss-paragraph-text"><div class="ss-form-entry">
<label class="ss-q-item-label" for="entry_1681034440"><div class="ss-q-title"  style="padding-top:10px;">7. Anything else you would like us to know?
</div>
<div class="ss-q-help ss-secondary-text" dir="auto"></div></label>
<textarea name="entry.1681034440" rows="8" cols="60" class="ss-q-long" id="entry_1681034440" dir="auto" aria-label="Anything else you would like us to know?  " style="margin: 10px 20px;"></textarea>
<div class="error-message" id="1003083472_errorMessage"></div>
<div class="required-message"></div>
</div></div></div>
<input type="hidden" name="draftResponse" value="[,,&quot;-5260546940849075059&quot;]
">
<input type="hidden" name="pageHistory" value="0">

<input type="hidden" name="fvv" value="0">


<input type="hidden" name="fbzx" value="-5260546940849075059">

<div class="ss-item ss-navigate"><table id="navigation-table"><tbody><tr><td class="ss-form-entry goog-inline-block" id="navigation-buttons" dir="ltr">
<input type="submit" name="submit" value="Submit" id="ss-submit" class="jfk-button jfk-button-action ">
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
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-96.png" alt="Facebook" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>
				                                    
				                                    
				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:10px; padding-bottom:9px;">
				                                            <a href="http://www.facebook.com/clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Facebook</a>
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
				                                            <a href="http://www.clickgarage.in" target="_blank"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-96.png" alt="Website" class="mcnFollowBlockIcon" width="48" style="width:48px; max-width:48px; display:block;"></a>
				                                        </td>
				                                    </tr>
				                                    
				                                    
				                                    <tr>
				                                        <td align="center" valign="top" class="mcnFollowTextContent" style="padding-right:0; padding-bottom:9px;">
				                                            <a href="http://www.clickgarage.in" target="_blank" style="color: #606060;font-family: Arial;font-size: 11px;font-weight: normal;line-height: 100%;text-align: center;text-decoration: none;">Website</a>
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
	Email : info@clickgarage.in | Phone No. : +91-9717353148<br>
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


	# file_pdf = MIMEText(file(path_file)
	# msg.attach(file_pdf)
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(path_file, "rb").read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; '+'filename=Invoice_'+booking_id+'.pdf')
	
	msg.attach(part)


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



def send_booking_final(username,useremail,userphone,time_start,date,booking_id,html_script):
	send_booking_details(["shashwat@clickgarage.in","bhuvan@clickgarage.in","sanskar@clickgarage.in","bookings@clickgarage.in"],booking_id,html_script)
	send_booking_email(useremail,username,time_start,date,booking_id)
	send_booking_sms(username, userphone, date, time_start, booking_id)

#views.send_booking_sms("Rajeev", "8447021642", "29-10-2015", "10:00AM", "0001")
def send_booking_details(to_address,booking_id,html_script):
	me = from_address
	you = to_address

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


	smtp_port = '25'
	smtp_do_tls = True

	server = smtplib.SMTP(
	    host = smtp_server,
	    port = smtp_port,
	    timeout = 30
	)
	
	server.set_debuglevel(10)
	server.ehlo()
	server.starttls()
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
