
var Global = {
    init:function(){
        var _this = this;
//    $("[data-role=panel]").panel().enhanceWithin();  
        _this.events();
        //$('#submit-button').button('disable');
    },
    events:function(){
        var _this = this;
        console.log('adding hanlder')   

    $('.booking-search').on("click", function(event, data) {
//          console.log( data.state.info );
//          console.log( data.state.direction )
//          console.log( data.state.url )
//          console.log( data.state.hash )
//          $("#test").text("new text");
          Commons.ajaxData('fetch_all_booking', {r_id:"dmFydW5ndWxhdGlsaWtlc2dhbG91dGlrZWJhYg=="},"get",_this, _this.loadBookings)
//          Commons.ajaxData('fetch_all_cars', {},"get",_this, _this.loadBookings)
            }
        );
        
//    $('.action-button').on('click', function(e){
    $('.centered-content').on('click', '#sms-button', function(e){
        console.log('testing');
        var obj = {};
        var parent_div = $(this).closest('.booking-entry') 
        obj.bkg_id = parent_div.find('#id-div p').text();
        obj.service = parent_div.find('#service-div #service-type').text().replace("Service: ","");
        obj.pickup_time = parent_div.find('#service-div #pickup-time').text().replace("Pickup-time: ","");
        obj.cust_name = parent_div.find('#cust-div #cust-name').text().replace("Name: ","");
        obj.cust_contact = parent_div.find('#cust-div #cust-contact').text().replace("Phone: ","");
        obj.cust_email = parent_div.find('#cust-div #cust-email').text().replace("Email: ","");
        obj.cust_address = parent_div.find('#cust-div #cust-address').text().replace("Address: ","");
        obj.brand = parent_div.find('#car-div #brand').text().replace("Brand: ","");
        obj.make = parent_div.find('#car-div #make').text().replace("Make: ","");
        obj.regn = parent_div.find('#car-div #regn').text().replace("Regn#: ","");
        console.log(obj);
        $('.sms-popup .booking-id').text(obj.bkg_id);
        $('.sms-popup .service').text(obj.service);
        $('.sms-popup .cust-name').text(obj.cust_name);
        $('.sms-popup .cust-contact').text(obj.cust_contact);
        $('.sms-popup .cust-address').text(obj.cust_address);
        $('.sms-popup .vehicle').text(obj.brand + ' ' + obj.make);
        $('.sms-popup .pickup-time').text(obj.pickup_time);
        $('.sms-popup').show()
            }
        );
        
        
    $('#select-driver').on('change', function(e){
        var driver_det = $('#select-driver option:selected').text();
        $('.sms-popup .driver-details').text(driver_det);        
            }
        );
        
    $('#select-advisor').on('change', function(e){
        var advisor_det = $('#select-advisor option:selected').text();
        $('.sms-popup .advisor-details').text(advisor_det);        
            }
        );
    
    
    },

    loadBookings : function(data){
        console.log(data)
        var container = $('.booking');
        container.html('');
        var html = '';
        $.each(data, function(idx, val){
            html += '<div class="booking-entry">';
//            id-div starts
            html += '<div class="booking-entry-cat" id="id-div">'
            html += '<p>' + String(val.booking_id) + '</p>';
            html += '</div>';
//            service-div starts here
            html += '<div class="booking-entry-cat" id="service-div">';
            html += '<p id="service-type">Service: ' + String(val.service_items[0].served_data.type_service) + '</p>';
            html += '<p id="vendor-type">Vendor: ' + String(val.service_items[0].served_data.dealer_cat) + '</p>';
            html += '<p id="pickup-time">Pickup-time: ' + String(val.time_booking) + '</p>';
            html += '</div>';
//            car-div starts
            html += '<div class="booking-entry-cat" id="car-div">';
            html += '<p id="brand">Brand: ' + String(val.service_items[0].served_data.brand) + '</p>';
            html += '<p id="make">Make: ' + String(val.service_items[0].served_data.car).replace(String(val.service_items[0].served_data.brand),"") + '</p>';
            html += '<p id="regn">Regn#: ' + String(val.cust_carnumber) + '</p>';
            html += '</div>';
//            cust-div starts
            html += '<div class="booking-entry-cat" id="cust-div">';
            html += '<p id="cust-name">Name: ' + String(val.cust_name) + '</p>';
            html += '<p id="cust-contact">Phone: ' + String(val.cust_number) + '</p>';
            html += '<p id="cust-email">Email: ' + String(val.cust_email) + '</p>';
            html += '<p id="cust-address">Address: ' + String(val.cust_pickup_add.street) + ', ' + String(val.cust_pickup_add.city) + ' (Landmark: ' + String(val.cust_pickup_add.landmark)+')</p>';
            html += '</div>';
//            status-div starts
            html += '<div class="booking-entry-cat" id="status-div">';
            html += '<p>Status: ' + String(val.status) + '</p>';
//            html += '<p> Status: ' + if(String(val.status)==''){'Upcoming'}else{String(val.status)} + '</p>';
            html += '</div>';
//            actions-div starts
            html += '<div class="booking-entry-cat" id="actions-div">';
            html += '<button class="action-button" id="sms-button">Send SMS</button>';
            html += '<button class="action-button" id="email-button">Send E-mail</button>';
            html += '<button class="action-button" id="change-status">Change Status</button>';
            html += '</div>';
//            bookings-div closing tag here
            html += '</div>';
        });
        container.html(html);
    }

};




document.onreadystatechange = function () {
      Global.init();
}


