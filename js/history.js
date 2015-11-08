/**
 * Created with PyCharm.
 * User: vociferous
 * Date: 02/08/15
 * Time: 3:17 PM
 * To change this template use File | Settings | File Templates.
 */

var Global = {
     init:function(){
        var _this = this;
        _this.setLayout();
        _this.eventHandlers();
        Commons.eventHandlers();
        if(!_this.carSelected){
            var cookDict = local.load();
            if(cookDict['clgacarid'] && _this.carData){
                _this.carSelected =  $.grep(_this.carData, function(e){ return e.id == cookDict['clgacarid']; })[0];

            }
        }
//        if(_this.carSelected){
//            $("#selected-details").show();
//            $("#selected-details").find('.c-name').html(_this.carSelected.name);
//            $("#selected-details").find('.c-make').html(_this.carSelected.make);
//        }else{
//                _this.generateCarSelect();
//        }
       
      
      
//        history.replaceState({state:'servicing'}, null, window.location.href);
    },
    setLayout:function(){
    },
    eventHandlers:function(){
        var _this = this;
        $('.section-headers .section-menu-item').on('click', function(e){
            if(!$(this).hasClass('active')){
                $(this).addClass('active');
                $(this).siblings().removeClass('active');
                var classy = $(this).attr('data-class');
//                console.log($(this).closest('.section-box').find('.section-content-item').hide())
                $(this).closest('.section-box').find('.section-content-item').hide();
                var mine = $(this).closest('.section-box').find('.section-content-item').filter('.'+classy).show();
                console.log(classy)
                if(mine.hasClass('loaded')){

                }else{
                    if(classy == 'cancelled' || classy == 'booking'){
                        Commons.ajaxData('fetch_car_'+classy, {c_id:_this.carSelected.id},"get",_this, eval("_this.load"+classy.toTitleCase()))
                    }
                }
            }else{

            }
//            var stateObj = { foo: "bar" };
        });

        $(".section-listings").on('click','#cancel-booking',function(e){
            if(!$(this).hasClass('cancelled')){
                var elem = $(this);
                elem.addClass('cancelled')
                var tran_id = elem.attr('tran_id')
                var classy = 'Booking'
                Commons.ajaxData('cancel_booking', {tran_id:tran_id},"get",_this, eval("_this.afterCancel"+classy.toTitleCase()))

            }
        })
       


    },

    afterCancelBooking: function(data){
        console.log(data)    
        var btn = $('[tran_id="'+data['cancelled_id']+'"]')
        btn.find('div').text('Booking Cancelled')
        btn.addClass('cancelled_booking')
    },

    loadBooking : function(data){
        console.log(data)
        var container = $('.section-box .booking');
        container.html('');
        console.log(container)
        console.log(Templates.bookingPage.booking)
        container.json2html(data, Templates.bookingPage.booking, {append:true});
//        container.append(json2html.transform(data,Templates.bookingPage.services));
        $.each(data, function(idx, val){

        });

    },

    loadCancelled : function(data){
        console.log(data)
        var container = $('.section-box .cancelled');
        container.html('');
        container.json2html(data, Templates.bookingPage.cancelled, {append:true});
//        container.append(json2html.transform(data,Templates.bookingPage.services));
        $.each(data, function(idx, val){

        });

    },

    
    loadServicing : function(data){
        console.log(data)
        var container = $('.section-box .servicing');
        container.html('');
        container.json2html(data, Templates.orderPage.servicing, {append:true});
//        container.append(json2html.transform(data,Templates.bookingPage.services));
        $.each(data, function(idx, val){

        });

    },
    
    loadCleaning : function(data){
        console.log(data);
        var container = $('.section-box .cleaning');
        container.html('');
        container.json2html(data, Templates.bookingPage.cleaning, {append:true});

//        var headHolder = $('.section-box .cleaning .list-head');
//        headHolder.html('');
//        headHolder.json2html(data, Templates.bookingPage.cleaning.cleaning_group_head, {append:true});
//        var bodyHolder = $('.section-box .cleaning .list-body');
//        bodyHolder.html('');
//        bodyHolder.json2html(data, Templates.bookingPage.cleaning.cleaning_group_body, {append:true});


//        container.append(json2html.transform(data,Templates.bookingPage.services));
        $.each(data, function(idx, val){

        });
    },
};


$(document).ready(function(){
    Global.init();
});


