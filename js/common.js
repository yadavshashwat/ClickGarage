/**
 * Created with PyCharm.
 * User: vociferous
 * Date: 03/08/15
 * Time: 10:06 PM
 * To change this template use File | Settings | File Templates.
 */


var Commons = {
    ajaxData : function(name, params, type, bindObj, success_cb, fail_cb){
        var _this = this;
        var url = _this.getOrigin() + _this.URLFromName[name];
        var callType = "GET";
        if(type == "POST" || type == "GET"){
            callType = type
        }
        console.log(name)
        if(name){
            $.ajax({
                url:url,
                data:params,
                dataType:"json",
                type:callType

            }).always(function(res){
                    console.log(res)
                    if(res.status){
                        bind(success_cb, bindObj, [res.result])
                    }
                });
        }
    },
    URLFromName : {
        'fetch_all_cars':'/api/fetch_all_cars/',
        //'fetch_car_servicing':'/api/fetch_car_servicing/',
        //'fetch_servicing_details':'/api/fetch_servicing_details/',

        'fetch_car_servicing':'/api/fetch_car_servicing_new/',
        'fetch_servicing_details':'/api/fetch_servicing_details_new/',

        'fetch_car_cleaning':'/api/fetch_car_cleaning/',
        'fetch_car_windshield':'/api/fetch_car_windshield/',
        'fetch_windshield_details':'/api/fetch_windshield_details/',
        'fetch_cleaning_details':'/api/fetch_cleaning_details/',
        'fetch_car_vas':'/api/fetch_car_vas/',
        'fetch_vas_details':'/api/fetch_vas_details/',
        'fetch_car_cleanings':'/api/fetch_all_cleaningcatservices/',
        'fetch_car_tyres':'/api/fetch_all_cleaningcatservices/',
        'add_to_cart':'/api/add_to_cart/',
        'place_order':'/api/place_order/',
        'place_emergency_order':'/api/place_emergency_order/',
        'fetch_car_booking':'/api/fetch_car_booking/',
        'fetch_car_cancelled':'/api/fetch_car_cancelled/',
        'cancel_booking':'/api/cancel_booking/',
        'fetch_all_booking':'/api/fetch_all_booking/',
        'fetch_additional_details':'/api/fetch_additional_details/',
    },
    getOrigin: function(){
        var origin = window.location.origin;
        if(origin[origin.length-1] == '/'){
            origin = origin.slice(0,-1);
        }
        return origin;
    },
    showRegisterForm : function(){
        $('.loginBox').fadeOut('fast',function(){
            $('.registerBox').fadeIn('fast');
            $('.login-footer').fadeOut('fast',function(){
                $('.register-footer').fadeIn('fast');
            });
            $('.modal-title').html('Register with');
        });
        $('.error').removeClass('alert alert-danger').html('');

    },
    showLoginForm : function(){
        $('#loginModal .registerBox').fadeOut('fast',function(){
            $('.loginBox').fadeIn('fast');
            $('.register-footer').fadeOut('fast',function(){
                $('.login-footer').fadeIn('fast');
            });

            $('.modal-title').html('Login with');
        });
        $('.error').removeClass('alert alert-danger').html('');

    },
    openLoginModal : function(){
        Commons.showLoginForm();
        setTimeout(function(){
            $('#loginModal').modal('show');
        }, 230);

    },
    openRegisterModal : function(){
        Commons.showRegisterForm();
        setTimeout(function(){
            $('#loginModal').modal('show');
        }, 230);

    },
    loginAjax : function(){
        /*   Remove this comments when moving to server*/
        $.post( "/login", function( data ) {
                if(data == 1){
                    window.location.replace("/home");
                } else {
                     shakeModal();
                }
            });

    /*   Simulate error message from the server   */
         Commons.shakeModal();

    },
    shakeModal : function(){
        $('#loginModal .modal-dialog').addClass('shake');
                 $('.error').addClass('alert alert-danger').html("Invalid email/password combination");
                 $('input[type="password"]').val('');
                 setTimeout( function(){
                    $('#loginModal .modal-dialog').removeClass('shake');
        }, 1000 );

    },
    eventHandlers : function(){
        $('body').on('click', function(e){
            var $target = $(e.target);
            if( !$target.closest('.logged-user-drpdwn').length && !$target.closest('#settings-drpdwn').length ){
                $('.logged-user-drpdwn').hide();
            }
            if( !$target.closest('.description.tooltip-wrapper').length && !$target.closest('.info-icon').length){
                $('.description.tooltip-wrapper:visible').hide();
            }
        });
        $('body').on('click', '.modal-container .close-btn', function(e){
            $(this).closest('.modal-container').remove();
        });
        $('#sign-up-in-home').on('click', function(e){
//            console.log($('.modal-container'))
            $('.login-modal-container').show().animate({
                'opacity':1
            },100);//.children().hide();
//            $('.login-modal-container').find('#loginModal').show();
//            alert('p')
            $('.login-modal-container').find('#loginModal').addClass('in');
        });
        $('#sign-up-in-dash').on('click', function(e){
            $('.login-modal-container').show().animate({
                'opacity':1
            },100);//.children().hide();
            $('.login-modal-container').find('#loginModal').addClass('in');
        });
        $('.login-modal-container').on('click', function(e){
            var $target = $(e.target);
            if(!$target.closest('.modal-dialog').length && $('#loginModal').hasClass('in')){
                $('#loginModal').removeClass('in');
                $(this).animate({
                    'opacity':0
                }, 300).fadeOut(10);

            }
        });
//        $('#loginModal')
    }
};
function bind(f, obj, args)
{   //console.log('Bind-',obj, args);
    if (f){
        if(f instanceof Function){
            return f.apply(obj, args);
        }else{
            for(var fi=0;fi<f.length;fi++)
            {
                f[fi].apply(obj, args);
            }
        }
    }else
        console.log('Empty callback');

}

var logoMap = {
    '3M':'../static/img/dl-logo-3M.png',
    'Tee Car Care':'../static/img/dl-logo-Tee.png',
    'Exppress Car Wash':'../static/img/dl-logo-Exppress.png',
    'ClickGarage On-The-Go':'../static/img/dl-logo-OntheGo.png',
    'ClickGarage Doorstep':'../static/img/dl-logo-doorstep.png',
    'Authorized':'../static/img/brands/',
    'Authorized Bike':'../static/img/brands/Bike/',
    'Authorized Car':'../static/img/brands/Car/',
    'Bosch':'../static/img/dl-logo-Bosch.jpg',
    'ClickGarage Verified':'../static/img/dl-logo-cgverified.png',
    'Mahindra First Choice':'../static/img/dl-logo-MFC.jpg',
    'ClickGarage Workshop':'../static/img/dl-logo-cgverified.png',
    'Bosch Car Care':'../static/img/dl-logo-Bosch.jpg',
    'AIS':'../static/img/ais.png',
    '--':'../static/img/dl-logo-cgverified.png',
};

var Templates = {
    orderPage:{
        servicing_old:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                        {"tag":"div", "class":"vendor-div", "html":function(){return "<div> Select this Service </div>";}}
                    ]},

                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"due-div fl", "html":function(){return "<span class='due-at-read'>Due at</span> <span class='odo-read'>"+ String(this.odometer).replace(/(.)(?=(\d{3})+$)/g,'$1,')+ ' km ' + (this.year == "" ? '': '/ ') + this.year+"</span>";}},
                        
                    {"tag":"div", "class":"service-details fix_servicedetails", "children":[  
                        {"tag":"div", "class":"checks-div", "html":function(){return 'Washing';}},
                        {"tag":"div", "class":"checks-div", "html":function(){return 'Regular Checks';}},        
                        {"tag":"div", "class":"parts-div", "html":function(){
                            var html = '';
                            if(this['parts_replaced'] && this['parts_replaced'].length){
                                $.each(this['parts_replaced'], function(i, part){
                                    html += '<span class="token-class">'+part+'</span>&nbsp;';
                                });
                                return html;
    //                            return "Regular Checks :" + this['parts_replaced'].join(', ');
                            }
                            else
                                return "None";}}
                            ]}
                    ]}
                ]},
            
                {"tag":"div", "class":"state-update none-i"}
            ]
        }],
        servicing:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                        {"tag":"div", "class":"vendor-div", "html":function(){return "<div> Select this Service </div>";}}
                    ]},
                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"due-div fl", "html":function(){return "<span class='odo-read'>"+  (this.type_service == "Not Defined" ? 'I am not sure<br> <span class="due-at-read">- I will go with minor servicing and <br> would  like post check-up recommendation</span>': this.type_service)+"</span>";}},

                    {"tag":"div", "class":"service-details fix_servicedetails", "children":[
                        {"tag":"div", "class":"checks-div", "html":function(){return 'Washing';}},
                        {"tag":"div", "class":"checks-div", "html":function(){return 'Regular Checks';}},
                        {"tag":"div", "class":"parts-div", "html":function(){
                            var html = '';
                            if(this['car_bike']=="Bike"){
                                html += '<span class="token-class">Engine Oil</span>&nbsp;';
                                html += '<span class="token-class">Oil Filter</span>&nbsp;';
                                html += '<span class="token-class">Other Parts as required</span>&nbsp;';
                                return html;
                            }else{
                                if(this['parts_replaced'] && this['parts_replaced'].length){
                                $.each(this['parts_replaced'], function(i, part){
                                    html += '<span class="token-class">'+part+'</span>&nbsp;';
                                });
                                return html;
    //                            return "Regular Checks :" + this['parts_replaced'].join(', ');
                            }
                            else
                                return "None";

                            }
                            }}
                            ]}
                    ]}
                ]},

                {"tag":"div", "class":"state-update none-i"}
            ]
        }],
        cleaning:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                        {"tag":"div", "class":"vendor-div", "html":function(){return "<div> Select this Service </div>";}}
                    ]},

                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"due-div", "html":function(){return "<span class='clean-cat'>"+this.category +"</span>";}},
//                        {"tag":"div", "class":"price-div", "html":function(){return "Type : <span>"+this['paid_free']+"</span>";}}
                    ]}
                ]},
                {"tag":"div", "class":"state-update none-i"}
            ]
        }],
        windshield:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                        {"tag":"div", "class":"vendor-div", "html":function(){return "<div> Select this Product </div>";}}
                    ]},

                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"due-div", "html":function(){return "<span class='service-cat'>"+this.ws_type +"</span>";}},
                        ]
                    }]
                }]
        }],
        vas:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                        {"tag":"div", "class":"vendor-div", "html":function(){return "<div> Select this Service </div>";}}
                    ]},

                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"due-div", "html":function(){return "<span class='clean-cat'>"+this.category +"</span>";}},
//                        {"tag":"div", "class":"price-div", "html":function(){return "Type : <span>"+this['paid_free']+"</span>";}}
                    ]}
                ]},
                {"tag":"div", "class":"state-update none-i"}
            ]
        }],
        dealers_old:[{
            "tag":"div","class":"dealer-list-item","data-id":"${id}", "data-name":"${vendor}", "children":[
                {"tag":"div","class":"td-dealer-info", "children":[
                    {"tag":"div", "class":"vendor-name","html":function(){
                         if($.trim(this.vendor) == 'Authorized'){
                                     return this.brand + ' Authorized';
                                }else{
                                    return this.vendor;
                                }
                    }},
                    {"tag":"div", "class":"dealer-logo-wrapper", "html":function(){
                        if(this.vendor){
                            if($.trim(this.vendor) == 'Authorized'){
                                if(this.car_bike=='Bike'){
                                     return '<img src="'+ logoMap['Authorized Bike'] + $.trim(this.brand)+'.jpg" alt="'+this.vendor+'" /><div class="aligner"></div>';
                                }else{
                                     return '<img src="'+ logoMap['Authorized Car'] + $.trim(this.brand)+'.jpg" alt="'+this.vendor+'" /><div class="aligner"></div>';
                                }

                            }else{
                                return '<img src="'+logoMap[$.trim(this.vendor)]+'" alt="'+this.vendor+'" /><div class="aligner"></div>';
                            }
                        }else{
                            return 'N/A'
                        }
                    }},
                ]},
                {"tag":"div","class":"td-service-info", "children":[
                    {"tag":"div", "class":"text","html":"Regular Servicing"},
                    {"tag":"div", "class":"sub-text","html":"(${odometer}km)"}
                ]},
                {"tag":"div","class":"col-item td-dealer-select", "children":[
                    // {"tag":"div", "class":"dealer-checkout", "html":"<a href='/checkout'>Checkout</a>"},

                    {"tag":"div", "html":"<a class='dealer-add-to-cart' href='/cart'>Add to Cart</a>"}

                ]},
                {"tag":"div","class":"td-price", "children":[
                    {"tag":"div", "class":"table-parts","html":function(){return "<table><tr><td>Parts</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+parseInt(this.parts_price)+"</td></tr><tr><td>Labour</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+Math.ceil((this.labour_price))+"</td></tr><tr><td>Service Tax</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+Math.ceil((this.labour_price*0.14))+"</td></tr><tr><td>Pick-Up Fee</td><td>:<strike><i style='padding-left:10px' class='fa fa-inr'></i>200</strike><i style='padding-left:10px' class='fa fa-inr'></i>"+ (this.car_bike == 'Car' ? '0': '0')+"</td></tr><tr id = 'total-row'><td>Total</td><td>:<i class='fa fa-inr' style='padding-left:10px'></i>"+(parseInt(this.parts_price)+parseInt(Math.ceil((this.labour_price)))+parseInt(Math.ceil((this.labour_price*0.14)))+parseInt((this.car_bike == 'Car' ? '0': '0')))+"</td></tr></table>";}}
                    ]},
                {"tag":"div","class":"col-item td-rating", "html":""}
            ]
        }],
                dealers:[{
            "tag":"div","class":"dealer-list-item","data-id":"${id}", "data-name":"${vendor}", "children":[
                {"tag":"div","class":"td-dealer-info", "children":[
                    {"tag":"div", "class":"vendor-name","html":function(){
                         if($.trim(this.vendor) == 'Authorized'){
                                     return this.brand + ' Authorized';
                                }else{
                                    return this.vendor;
                                }
                    }},
                    {"tag":"div", "class":"dealer-logo-wrapper", "html":function(){
                        if(this.vendor){
                            if($.trim(this.vendor) == 'Authorized'){
                                if(this.car_bike=='Bike'){
                                     return '<img src="'+ logoMap['Authorized Bike'] + $.trim(this.brand)+'.jpg" alt="'+this.vendor+'" /><div class="aligner"></div>';
                                }else{
                                     return '<img src="'+ logoMap['Authorized Car'] + $.trim(this.brand)+'.jpg" alt="'+this.vendor+'" /><div class="aligner"></div>';
                                }

                            }else{
                                return '<img src="'+logoMap[$.trim(this.vendor)]+'" alt="'+this.vendor+'" /><div class="aligner"></div>';
                            }
                        }else{
                            return 'N/A'
                        }
                    }},
                ]},
                {"tag":"div","class":"td-service-info", "children":[
                    {"tag":"div", "class":"text","html":function(){
                         if(this.type_service == 'Not Defined'){
                                    return 'Minor Servicing';
                                }else{
                                    return this.type_service;
                                }}},
                    //{"tag":"div", "class":"sub-text","html":"(${odometer}km)"}
                ]},
                {"tag":"div","class":"col-item td-dealer-select", "children":[
                    // {"tag":"div", "class":"dealer-checkout", "html":"<a href='/checkout'>Checkout</a>"},

                    {"tag":"div", "html":"<a class='dealer-add-to-cart' href='/cart'>Add to Cart</a>", "class":"none-i"},
                    {"tag":"div", "html":"<a class='servicing-form-generate'>Add to Cart</a>"}
                ]},
                {"tag":"div","class":"td-price", "children":[
                    {"tag":"div", "class":"table-parts","html":function(){
                        if(this.vendor=='Authorized'){
                            if(this.car_bike=='Bike'){
                                var s = '<Table>'
                                $.each(this.part_dic,function(i,elem){
                                    s += '<tr><td>'+elem.part_name+"</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+parseInt(this.part_price)+"</td></tr>"
                                    })
                                    s += "<tr><td>Labour</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+Math.ceil((this.labour_price))+"</td></tr><tr><td>Service Tax</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+Math.ceil((this.labour_price*0.14))+"</td></tr><tr><td>Pick-Up Fee</td><td>:<strike><i style='padding-left:10px' class='fa fa-inr'></i>200</strike><i style='padding-left:10px' class='fa fa-inr'></i>"+ (this.car_bike == 'Car' ? '0': '0')+"</td></tr>"
                                    s += '</table>'
                                    return s

                            }else{
                           return "<table><tr>&nbspService Centre Bill Amount</tr><tr><td></td><td>+</td></tr><td>Pick-Up Fee</td><td>:<strike><i style='padding-left:10px' class='fa fa-inr'></i>200</strike><i style='padding-left:10px' class='fa fa-inr'></i>"+ (this.car_bike == 'Car' ? '0': '0')+"</td></tr></table>";
                            }
                        }else{
                            return "<table><tr><td>Parts</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+parseInt(this.parts_price)+"</td></tr><tr><td>Labour</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+Math.ceil((this.labour_price))+"</td></tr><tr><td>Service Tax</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+Math.ceil((this.labour_price*0.14))+"</td></tr><tr><td>Pick-Up Fee</td><td>:<strike><i style='padding-left:10px' class='fa fa-inr'></i>200</strike><i style='padding-left:10px' class='fa fa-inr'></i>"+ (this.car_bike == 'Car' ? '0': '0')+"</td></tr><tr id = 'total-row'><td>Total</td><td>:<i class='fa fa-inr' style='padding-left:10px'></i>"+(parseInt(this.parts_price)+parseInt(Math.ceil((this.labour_price)))+parseInt(Math.ceil((this.labour_price*0.14)))+parseInt((this.car_bike == 'Car' ? '0': '0')))+"</td></tr></table>";
                    }}}
                    ]},
                {"tag":"div","class":"col-item td-rating", "html":""},
                {"tag":"div","class":"none-i", "html":function(){
                    if(Global && Global.dealerAddressObj){
                        if(this.vendor == 'Authorized'){
                            Global.dealerAddressObj[this.brand] = this.dealer_details;
                        }
                    }
                    return JSON.stringify({'dealer_details':this.dealer_details, 'brand':this.brand, 'vendor':this.vendor});
                }}

            ]
        }],
        cleaning_old:{
            cleaning_group_head:[{
                "tag":"div","class":"service-group-head", "data-name":"${name}", "data-id":"${id}",  "children":[
                    {"tag":"div", "class":"dealer-logo-wrapper", "html":function(){
                        if(this.name){
                            return '<img src="'+logoMap[$.trim(this.name)]+'" alt="'+this.name+'" /><div class="aligner"></div>';
                        }else{
                            return 'N/A'
                        }
                    }},
                    {"tag":"div", "class":"dealer-number-label", "html":function(){ return this.list.length; }},
                    {"tag":"div", "class":"pointer right-triangle"},
                    {"tag":"div", "class":"select-border"}
//                    {"tag":"div", "class":"brand-div", "html":function(){return "Dealer : <span>"+this.name+"</span>";}},
//                    {"tag":"div", "class":"price-div", "html":function(){return "Number : <span>"+this.list.length+"</span>";}}
                ]
            }],
            cleaning_group_body:[{
                "tag":"div","class":"service-group-item wrapper detail-wrapper", "data-name":"${name}", "data-id":"${id}", "html":function(){
                        return json2html.transform(this.list, Templates.orderPage.cleaning.cleaning_item)
                }
            }],
            cleaning_item:[{
                "tag":"div", "class":"service-list-item", "data-id":"${id}", "children":[
                    {"tag":"div", "class":"header-wrapper", "children":[
                        {"tag":"div", "class":"", "html":function(){return this.category}}
                    ]},
                    {"tag":"div", "class":"state-update none-i"}
                ]
            }]
        },
        packages:[{
            "tag":"div","class":"dealer-list-item cleaning","data-id":"${id}", "data-name":"${vendor}", "children":[
                {"tag":"div","class":"td-dealer-info", "children":[
                    {"tag":"div", "class":"vendor-name","html":function(){
                         if($.trim(this.vendor) == 'Authorized'){
                                     return this.brand + ' Authorized';
                                }else{
                                    return this.vendor;
                                }}},
                    {"tag":"div", "class":"dealer-logo-wrapper", "html":function(){
                        if(this.vendor){
                            if($.trim(this.vendor) == 'Authorized'){
                                return '<img src="'+logoMap['Authorized']+ $.trim(this.brand)+'.jpg" alt="'+this.vendor+'" /><div class="aligner"></div>';
                            }else{
                                return '<img src="'+logoMap[$.trim(this.vendor)]+'" alt="'+this.vendor+'" /><div class="aligner"></div>';
                            }
                        }else{
                            return 'N/A'
                        }
                    }},

                ]},
                {"tag":"div","class":"td-service-info", "children":[
                    {"tag":"div", "class":"text", "children":[
                        {"tag":"span","class":"car-care", "html":"${service}"},
                        {"tag":"span", "class":"info-icon fr","html":"Info <i class='fa fa-info-circle'></i>"},
                    ]},
                    {"tag":"div", "class":"sub-text","html":"(${category})"},
                    {"tag":"div", "class":"doorstep-div", "html":function(){
                        if(this.doorstep=="1"){return "<span class='doorstep'><i class='fa fa-home'></i>&nbspDoorstep Service</span>"
                        }else{
                            return ''
                        }}},
                    {"tag":"div","class":"description tooltip-wrapper","children":[
                        {"tag":"div","class":"tri-tip"},
                        {"tag":"div","class":"tooltip-box","html":"${description}"}
                    ]},
                    {"tag":"div", "class":"description none-i","html":"${description}"},
                ]},
                {"tag":"div","class":"col-item td-dealer-select", "children":[
                    // {"tag":"div", "class":"dealer-checkout", "html":"<a href='/checkout'>Checkout</a>"},
                    {"tag":"div", "html":"<a class='dealer-add-to-cart' href='/cart'>Add to Cart</a>"}
                ]},
                {"tag":"div","class":"col-item td-price", "children":[
    {"tag":"div", "class":"table-parts","html":function(){return "<table><tr><td>Service Price</td><td>:"+(this.discount=='0' ? '' : "<strike>")+"<i style='padding-left:10px' class='fa fa-inr'></i>"+this.total_price + (this.discount=='0' ? '' : "</strike>&nbsp<i style='padding-left:10px' class='fa fa-inr'></i>") + (this.discount=='0' ? '' : parseInt(parseFloat(this.total_price)*(1.0-parseFloat(this.discount))))+ "</td></tr>"+ (this.doorstep == '0' ? "<tr><td>Pick-Up Fee</td><td>:<strike><i style='padding-left:10px' class='fa fa-inr'></i>200</strike><i style='padding-left:10px' class='fa fa-inr'></i>0</td></tr>" : '')+"<tr><td>Total</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+parseInt(parseFloat(this.total_price)*(1.0-parseFloat(this.discount)))+"</td></tr></table>";}}                ]},
                {"tag":"div","class":"col-item td-rating", "html":""}
            ]
        }],
        packages_vas:[{
            "tag":"div","class":"dealer-list-item cleaning","data-id":"${id}", "data-name":"${vendor}", "children":[
                {"tag":"div","class":"td-dealer-info", "children":[
                    {"tag":"div", "class":"vendor-name","html":function(){
                         if($.trim(this.vendor) == 'Authorized'){
                                     return this.brand + ' Authorized';
                                }else{
                                    return this.vendor;
                                }}},
                    {"tag":"div", "class":"dealer-logo-wrapper", "html":function(){
                        if(this.vendor){
                            if($.trim(this.vendor) == 'Authorized'){
                                return '<img src="'+logoMap['Authorized']+ $.trim(this.brand)+'.jpg" alt="'+this.vendor+'" /><div class="aligner"></div>';
                            }else{
                                return '<img src="'+logoMap[$.trim(this.vendor)]+'" alt="'+this.vendor+'" /><div class="aligner"></div>';
                            }
                        }else{
                            return 'N/A'
                        }
                    }},

                ]},
                {"tag":"div","class":"td-service-info", "children":[
                    {"tag":"div", "class":"text", "children":[
                        {"tag":"span","class":"car-care", "html":"${service}"},
                        {"tag":"span", "class":"info-icon fr","html":"Info <i class='fa fa-info-circle'></i>"},
                    ]},
                    {"tag":"div", "class":"sub-text","html":"(${category})"},
                    {"tag":"div", "class":"doorstep-div", "html":function(){
                        if(this.doorstep=="1"){return "<span class='doorstep'><i class='fa fa-home'></i>&nbspDoorstep Service</span>"
                        }else{
                            return ''
                        }}},
                    {"tag":"div","class":"description tooltip-wrapper","children":[
                        {"tag":"div","class":"tri-tip"},
                        {"tag":"div","class":"tooltip-box","html":"${description}"}
                    ]},
                    {"tag":"div", "class":"description none-i","html":"${description}"},
                ]},
                {"tag":"div","class":"col-item td-dealer-select", "children":[
                    // {"tag":"div", "class":"dealer-checkout", "html":"<a href='/checkout'>Checkout</a>"},
                    {"tag":"div", "html":"<a class='dealer-add-to-cart' href='/cart'>Add to Cart</a>"}
                ]},
                {"tag":"div","class":"col-item td-price", "children":[
    {"tag":"div", "class":"table-parts","html":function(){return "<table><tr><td>Service Price</td><td>:"+(this.discount=='0' ? '' : "<strike>")+"<i style='padding-left:10px' class='fa fa-inr'></i>"+this.total_price + (this.discount=='0' ? '' : "</strike>&nbsp<i style='padding-left:10px' class='fa fa-inr'></i>") + (this.discount=='0' ? '' : parseInt(parseFloat(this.total_price)*(1.0-parseFloat(this.discount))))+ "</td></tr>"+ (this.doorstep == '0' ? "<tr><td>Pick-Up Fee</td><td>:<strike><i style='padding-left:10px' class='fa fa-inr'></i>200</strike><i style='padding-left:10px' class='fa fa-inr'></i>0</td></tr>" : '')+"<tr><td>Total</td><td>:<i style='padding-left:10px' class='fa fa-inr'></i>"+parseInt(parseFloat(this.total_price)*(1.0-parseFloat(this.discount)))+"</td></tr></table>";}}                ]},
                {"tag":"div","class":"col-item td-rating", "html":""}
            ]
        }],
        
        ws_subtype:[{
            "tag":"div","class":"dealer-list-item","data-id":"${id}", "data-name":"${vendor}", "children":[
                {"tag":"div","class":"td-dealer-info", "children":[
                    {"tag":"div", "class":"vendor-name","html":function(){
                        return this.vendor;
                    }},
                    {"tag":"div", "class":"dealer-logo-wrapper", "html":function(){
                        return '<img src="'+logoMap[$.trim(this.vendor)]+'" alt="'+this.vendor+'" /><div class="aligner"></div>';
                    }},
                ]},
                {"tag":"div","class":"td-service-info", "children":[
                    {"tag":"div", "class":"parts-div","html":function(){
                        var html = '';
                        if(this.ws_type=='Door Glass'){
                            html += this.ws_subtype+' '+this.ws_type;
                        }
                        else{
                            html += this.ws_type;
                        }
                        return html;
                    }},
                    {"tag":"div", "class":"parts-div","html":function(){
                        var html = '';
                        if(this.ws_subtype=='With Defogger'){
                                html += '<span class="token-class">'+this.ws_subtype+'</span>&nbsp;';}
                        if(this.colour=='Green'){
                                html += '<span class="token-class">Green Tinted</span>&nbsp;';}
                        return html;
                    }},
                    {"tag":"div", "class":"text","html":function(){
                        return '<span class="doorstep"><i class="fa fa-home"></i>&nbspDoorstep Service</span>';
                    }}
                ]},
                {"tag":"div","class":"col-item td-dealer-select", "children":[
                    // {"tag":"div", "class":"dealer-checkout", "html":"<a href='/checkout'>Checkout</a>"},

                    {"tag":"div", "html":"<a class='dealer-add-to-cart', href='/cart'>Add to Cart</a>"}
                ]},
                {"tag":"div","class":"td-price", "children":[
                    {"tag":"div", "class":"text","html":function(){
                        if(this.price_total=='NA'){
                            return "Conveyed post booking"
                        }
                        else {
                            return 'Price (incl taxes) :'+'<i style="padding-left:10px" class="fa fa-inr"></i> '+parseInt(Math.ceil((this.price_total)));
                        }
                    }}
                    ]},
                {"tag":"div","class":"col-item td-rating", "html":""}
            ]
        }]
    },
    bookingPage:{
        booking_new:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                        {"tag":"div", "id":"cancel-booking",  "tran_id":"${tran_id}", "class":"vendor-div none-i", "html":function(){return "<div> Cancel Booking </div>";}}
                    ]},

                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"booking id booking_id", "html":function(){return '#'+(this.booking_id);}},
                        {"tag":"div", "class":"booking car booking_car", "html":function(){return (this.cust_carname);}},
                        {"tag":"div", "class":"booking date booking_date", "html":function(){return (this.date_booking) + ' ('+this.time_booking+')';}},
                        {"tag":"div", "class":"booking list booking_list",
                        //    "html":function(){
                        //    var s = '<ul class="service-components">'
                        //    $.each(this.service_items,function(i,elem){
                        //        if(elem.service == 'servicing'){
                        //        s += '<li class="indiv_booking" style="height: 90px;">'+elem.served_data.dealer_cat+'  <i class="fa fa-caret-right"></i>  '+ elem.served_data.odometer+'km (Regular Sevicing) <div id="cancel-booking" tran_id="561ac69396f69553e74fe545" class="vendor-div" style="padding: 0px; float: right;"><div> Cancel Booking </div></div></li>'
                        //        }else{
                        //        s += '<li class="indiv_booking" style="height: 90px;">'+elem.served_data.vendor +'  <i class="fa fa-caret-right"></i>  '+ elem.served_data.service+' ( '+elem.served_data.category+' ) <div id="cancel-booking" tran_id="561ac69396f69553e74fe545" class="vendor-div" style="padding: 0px; float: right;"><div> Cancel Booking </div></div></li>'
                        //        }
                        //    })
                        //    s += '</ul>'
                        //    return s
                        //},
                        "children": [
                            {"tag":"ul", "class":"service-components", "html":function(){
                                var _booking = this;
                                var s = ''
                                $.each(this.service_items,function(i,elem){

                                    if(elem.service == 'servicing'){
                                        s += '<li class="indiv_booking" style="height: 90px;">'+elem.served_data.dealer_cat+'  <i class="fa fa-caret-right"></i>  '
                                        if(elem.served_data.type_service == "Not Defined"){
                                            s+="Minor Servicing</li>"
                                        }else{
                                            s+=elem.served_data.type_service + '</li>'
                                        }
                                        s += '</li><div id="cancel-booking" tran_id="'+_booking.tran_id+'" item_id="'+elem.served_data.ts+'" class="vendor-div" style="padding: 0px; float: right;"><div> Cancel Booking </div></div></li>'
                                    }else{
                                    s += '<li class="indiv_booking" style="height: 90px;">'+elem.served_data.vendor +'  <i class="fa fa-caret-right"></i>  '+ elem.served_data.service+' ( '+elem.served_data.category+' ) <div id="cancel-booking" tran_id="'+_booking.tran_id+'" item_id="'+elem.served_data.ts+'" class="vendor-div" style="padding: 0px; float: right;"><div> Cancel Booking </div></div></li>'
                                    }
                                })
                                return s;
                            }}
                        ]
                        },    
                        
                        ]},
    

                ]},
        
            ]
        }],
        cancelled_new:[{
            "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                {"tag":"div", "class":"top-row", "children":[
                    
                    {"tag":"div", "class":"wrapper header-wrapper", "children":[
                        {"tag":"div", "class":"booking id booking_id", "html":function(){return '#'+(this.booking_id);}},
                        {"tag":"div", "class":"booking car booking_car", "html":function(){return (this.cust_carname);}},
                        {"tag":"div", "class":"booking date booking_date", "html":function(){return (this.date_booking) + ' ('+this.time_booking+')';}},
                        {"tag":"div", "class":"booking list booking_list", "html":function(){
                            var s = '<ul class="service-components">'
                            $.each(this.service_items,function(i,elem){
                             if(elem.service == 'servicing'){
                                s += '<li class="indiv_booking">'+elem.served_data.dealer_cat+'  <i class="fa fa-caret-right"></i>  '
                                 if(elem.served_data.type_service=="Not Defined"){
                                     s+="Minor Servicing"
                                 }else{
                                     s+=elem.served_data.type_service
                                 }
                                 s += '</li>'
                                }else{
                                s += '<li class="indiv_booking">'+elem.served_data.vendor +'  <i class="fa fa-caret-right"></i>  '+ elem.served_data.service+' ( '+elem.served_data.category+' ) </li>'
                                }
                            })
                            s += '</ul>'
                            return s
                        }
                        },    
                        
                        ]},
    

                ]},
        
            ]
        }],
        booking:[{
                "tag":"div","class":"service-list-item minimized", "data-id":"${id}", "children":[
                    {"tag":"div", "class":"top-row", "children":[
                        {"tag":"div", "class":"wrapper detail-wrapper", "children":[
                            {"tag":"div", "id":"cancel-booking",  "tran_id":"${tran_id}", "class":"vendor-div", "html":function(){return '<div> Cancel Booking </div>';}}
                        ]},

                        {"tag":"div", "class":"wrapper header-wrapper", "children":[
                            {"tag":"div", "class":"booking id booking_id", "html":function(){return '#'+(this.booking_id);}},
                            {"tag":"div", "class":"booking car booking_car", "html":function(){return (this.cust_carname);}},
                            {"tag":"div", "class":"booking date booking_date", "html":function(){return (this.date_booking) + ' ('+this.time_booking+')';}},
                            {"tag":"div", "class":"booking list booking_list", "html":function(){
                                var s = '<ul class="service-components">'
                                $.each(this.service_items,function(i,elem){
                                    if(elem.service == 'servicing'){
                                        if(elem.served_data){
                                        s += '<li class="indiv_booking">'+elem.served_data.dealer_cat+'  <i class="fa fa-caret-right"></i>  '
                                            if(elem.served_data.type_service && elem.served_data.type_service=="Not Defined"){
                                                s+="Minor Servicing </li>"
                                            }else if(elem.served_data.type_service){
                                                s+= elem.served_data.type_service + '</li>'
                                            }else{
                                                s += elem.served_data.odometer+'km / '+elem.served_data.year
                                            }
                                        }
                                    }else{
                                    s += '<li class="indiv_booking">'+elem.served_data.vendor +'  <i class="fa fa-caret-right"></i>  '+ elem.served_data.service+' ( '+elem.served_data.category+' ) </li>'
                                    }
                                })
                                s += '</ul>'
                                return s
                            }
                            },

                            ]},


                    ]},

                ]
            }],
        cancelled:[{
            "tag": "div", "class": "service-list-item minimized", "data-id": "${id}", "children": [
                {
                    "tag": "div", "class": "top-row", "children": [

                    {
                        "tag": "div", "class": "wrapper header-wrapper", "children": [
                        {
                            "tag": "div", "class": "booking id booking_id", "html": function () {
                            return '#' + (this.booking_id);
                        }
                        },
                        {
                            "tag": "div", "class": "booking car booking_car", "html": function () {
                            return (this.cust_carname);
                        }
                        },
                        {
                            "tag": "div", "class": "booking date booking_date", "html": function () {
                            return (this.date_booking) + ' (' + this.time_booking + ')';
                        }
                        },
                        {
                            "tag": "div", "class": "booking list booking_list", "html": function () {
                            var s = '<ul class="service-components">'
                            $.each(this.service_items, function (i, elem) {
                                if (elem.service == 'servicing') {
                                    if(elem.served_data) {
                                        s += '<li class="indiv_booking">' + elem.served_data.dealer_cat + '  <i class="fa fa-caret-right"></i>  '
                                        if (elem.served_data.type_service && elem.served_data.type_service == "Not Defined") {
                                            s += "Minor Servicing </li>"
                                        } else if(elem.served_data.type_service) {
                                            s += elem.served_data.type_service + '</li>'
                                        } else {
                                            s += elem.served_data.odometer+'km / '+elem.served_data.year
                                        }
                                    }
                                } else {
                                    s += '<li class="indiv_booking">' + elem.served_data.vendor + '  <i class="fa fa-caret-right"></i>  ' + elem.served_data.service + ' ( ' + elem.served_data.category + ' ) </li>'
                                }
                            })
                            s += '</ul>'
                            return s
                        }
                        },

                    ]
                    },


                ]
                },

            ]
        }]
    }

};

if (typeof String.prototype.toTitleCase != 'function') {
    String.prototype.toTitleCase = function (){
        return (this[0].toUpperCase() + this.slice(1));
    };
}

/*
*   1   -   userid
*   2   -   name
*   3   -
*   4   -
*   5   -
*
total transaction data required -
    booking_id         = models.IntegerField()
    trans_timestamp    = models.CharField(max_length=200)
    cust_name          = models.CharField(max_length=200)
    cust_brand         = models.CharField(max_length=200)
    cust_carname       = models.CharField(max_length=200)
    cust_number        = models.CharField(max_length=200)
    cust_email         = models.CharField(max_length=200)
    cust_pickup_add    = models.CharField(max_length=200)
    cust_drop_add      = models.CharField(max_length=200)
    booking_vendor     = models.CharField(max_length=200)
    booking_cat        = models.CharField(max_length=200)
    booking_type       = models.CharField(max_length=200)
    price_labour       = models.CharField(max_length=200)
    price_parts        = models.CharField(max_length=200)
    price_total        = models.CharField(max_length=200)
    date_booking       = models.CharField(max_length=200)
    time_booking       = models.CharField(max_length=200)
    amount_paid        = models.BooleanField()
    status             = models.CharField(max_length=200)
    comments           = models.CharField(max_length=300)

*
* */

var local = {
    save:function(key, value){
        var stringKey = 'clgacart';
        if(key){
            stringKey = key;
        }
        var stringVal = value;
        if(value instanceof Object){
            stringVal = JSON.stringify(value);
        }
        var dc_old = document.cookie;
        document.cookie = key+"="+stringVal+"; path=/";
    },
    load:function(){
        var dc_str = document.cookie;
        var dc_arr = dc_str.split(';');
        var dict = {};
        $.each(dc_arr, function(idx, val){
            dict[val.split('=')[0].trim()] = val.split('=')[1]
        });
        return dict;
    },
    clearKey:function(key){
        var stringKey = 'clgacart';
        if(key){
            stringKey = key;
        }
        document.cookie = stringKey+'=; expires=Thu, 01 Jan 1970 00:00:00 UTC;';
        document.cookie = stringKey+'=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/';
    },
    clearAll:function(){

    }
};

var formCheck = {
    getDateFromFormat : function(date, format) {
        if (date instanceof Date){
            function one2two(val) {
                if (val < 9) {
                    val = '0' + val;
                }
                return val;
            }
        if (format == 'dd/mm/yyyy') {
            return one2two(date.getDate()) + '/' + (one2two(date.getMonth() + 1) + '/' + (1900 + date.getYear()));
        } else if (format == 'mm/dd/yyyy') {
            return (one2two(date.getMonth() + 1) + '/' + one2two(date.getDate()) + '/' + (1900 + date.getYear()));
        }
        }else{
            return 'invalid date'
        }
    },
    addressForm : function(container){

        var valid = function(str){
            if(!str || !(str.length)){
                return false
            }
            return true;
        };
        var user_name = $(container).find('.user-name').val();
        var user_number = $(container).find('.user-number').val();
        var car_reg_number = $(container).find('.car-reg-no').val();

        var pick_addr = $(container).find('.pick-addr').val();
        var pick_pin = $(container).find('.pick-pin').val();
        var pick_lmark = $(container).find('.pick-lmark').val();

        var dropMatch = $(container).find('.pick-drop-toggle').is(':checked');

        var drop_addr = $(container).find('.drop-addr').val();
        var drop_pin = $(container).find('.drop-pin').val();
        var drop_lmark = $(container).find('.drop-lmark').val();

        if(!valid(user_name)){
            $(container).find('.user-name').addClass('error');
            return false
        }
        if(!valid(user_number)){
            $(container).find('.user-number').addClass('error');
            return false
        }else{
            if(isNaN(parseInt(user_number)) || user_number.length != 10){
                $(container).find('.user-number').addClass('error');
                return false
            }
        }


        if(!valid(pick_addr)){
            $(container).find('.pick-addr').addClass('error');
            return false
        }
        if(!valid(pick_pin)){
            $(container).find('.pick-pin').addClass('error');
            return false
        }else{
            console.log(pick_pin.length)
            if(isNaN(parseInt(pick_pin)) || pick_pin.length != 6){
                $(container).find('.pick-pin').addClass('error');
                return false
            }
        }
        if(!valid(car_reg_number)){
            $(container).find('.car-reg-no').addClass('error');
            return false
        }else{
            if(car_reg_number.length > 10){
                $(container).find('.car-reg-no').addClass('error');
                return false
            }
        }
        if(!valid(drop_addr)){
            $(container).find('.drop-addr').addClass('error');
            return false
        }
        if(!valid(drop_pin)){
            $(container).find('.drop-pin').addClass('error');
            return false
        }else{
//            console.log(pick_pin.length)
            if(isNaN(parseInt(drop_pin)) || drop_pin.length != 6){
                $(container).find('.drop-pin').addClass('error');
                return false
            }
        }
//        if(!valid(pick_lmark)){
//            $(container).find('.pick-lmark').addClass('error');
//            return false
//        }
        return true;
    },
    emergAddressForm : function(container){

        var valid = function(str){
            if(!str || !(str.length)){
                return false
            }
            return true;
        };
        var user_name = $(container).find('.user-name').val();
        var user_number = $(container).find('.user-number').val();
        var car_reg_number = $(container).find('.car-reg-no').val();

        var pick_addr = $(container).find('.pick-addr').val();
        var pick_pin = $(container).find('.pick-pin').val();
        var pick_lmark = $(container).find('.pick-lmark').val();


        if(!valid(user_name)){
            $(container).find('.user-name').addClass('error');
            return false
        }
        if(!valid(user_number)){
            $(container).find('.user-number').addClass('error');
            return false
        }else{
            if(isNaN(parseInt(user_number)) || user_number.length != 10){
                $(container).find('.user-number').addClass('error');
                return false
            }
        }


        if(!valid(pick_addr)){
            $(container).find('.pick-addr').addClass('error');
            return false
        }
        if(!valid(pick_pin)){
            $(container).find('.pick-pin').addClass('error');
            return false
        }else{
            console.log(pick_pin.length)
            if(isNaN(parseInt(pick_pin)) || pick_pin.length != 6){
                $(container).find('.pick-pin').addClass('error');
                return false
            }
        }
        if(!valid(car_reg_number)){
            $(container).find('.car-reg-no').addClass('error');
            return false
        }else{
            if(car_reg_number.length > 10){
                $(container).find('.car-reg-no').addClass('error');
                return false
            }
        }
//        if(!valid(pick_lmark)){
//            $(container).find('.pick-lmark').addClass('error');
//            return false
//        }
        return true;
    },
    clearErrorEvent : function(e){
        if($(this).val() && $(this).val().length){
            $(this).removeClass('error');
        }
    },
    setSelectedAddress : function(){

    },
    getSelectedAddress : function(container,formType){
        var user_name = $(container).find('.user-name').val();
        var user_number = $(container).find('.user-number').val();
        var car_reg_number = $(container).find('.car-reg-no').val();
        var pick_addr = $(container).find('.pick-addr').val();
        var pick_pin = $(container).find('.pick-pin').val();
        var pick_lmark = $(container).find('.pick-lmark').val();
        var pick_city = $(container).find('.pick-city').val();
        var pick_time = $(container).find('.pick-up-time').val();
        var pick_date = $(container).find('.pick-up-date').val();
        var drop_addr = $(container).find('.drop-addr').val();
        var drop_pin = $(container).find('.drop-pin').val();
        var drop_lmark = $(container).find('.drop-lmark').val();
        var drop_city = $(container).find('.drop-city').val();
        var obj = {}
        if(formType && formType == 'emergency'){
            var date = new Date();
            var hrs = date.getHours();
            if(hrs<10){
                hrs = '0'+hrs
            }
            var mts = date.getMinutes();
            if(mts<10){
                mts = '0'+mts
            }
            obj = {
                name : user_name,
                number : user_number,
                reg_no : car_reg_number,
                pick:{
                    street : pick_addr,
                    pincode : pick_pin,
                    landmark : pick_lmark,
                    city : pick_city,
                    time : ((hrs) + ':' + (mts)),
                    date : ((date.getMonth()+1) + '/' + (date.getDate()) + '/' +(date.getYear()))
                }
            };
//                orderItem['date'] = (date.getMonth()+1) + '/' + (date.getDate()) + '/' +(date.getYear());
//                orderItem['time'] = (date.getHours()) + ':' + (date.getMinutes());

        }else{
            obj = {
                name : user_name,
                number : user_number,
                reg_no : car_reg_number,
                pick:{
                    street : pick_addr,
                    pincode : pick_pin,
                    landmark : pick_lmark,
                    city : pick_city,
                    time : pick_time,
                    date : pick_date
                },
                drop:{
                    street : drop_addr,
                    pincode : drop_pin,
                    landmark : drop_lmark,
                    city : drop_city
                }
            };
        }
        return obj;
    },
    updateTime : function(container){
            var todayFlag = false;
            var sameDay = false;
            if($(container).find('#date-time-pair .pick-up-date').val() == formCheck.getDateFromFormat((new Date()), 'mm/dd/yyyy')){
                todayFlag = true;
            }
            if($('#same-day-toggle').is(':checked')){
                sameDay = true;
            }

            var thisHour = (new Date()).getHours() + 2;
            var thisMinute = (new Date()).getMinutes();
                thisHour += 1
            if(thisHour < 8)
                thisHour = 8
            if(thisHour >16)
                thisHour = 16
                var hr =  $(container).find('#date-time-pair .pick-up-time').val();
                var ampm = $(container).find('#date-time-pair .pick-up-time').val();
                if(hr){
                    hr = hr.split(':')[0];
                    hr = parseInt(hr);
                }
        if(ampm){
            ampm = ampm.split(' ')[1];
        }
        if(hr && !isNaN(hr) && (hr != 12) && ampm == 'PM'){
            hr = hr + 12
        }

            var minTime = new Date(0,0,0,thisHour,0,0);
            //var maxTime = new Date(0,0,0,12,0,0);
            if(todayFlag){
                $(container).find('#date-time-pair .pick-up-time').timepicker('option', 'minTime',minTime);
//                console.log(hr, thisHour)
                if(hr < thisHour){
                $(container).find('#date-time-pair .pick-up-time').timepicker('setTime',minTime);
                    alert('Pick up time slots start from 2 hours after booking time');
                }
            }else{
                $(container).find('#date-time-pair .pick-up-time').timepicker('option', 'minTime',new Date(0,0,0,8,0,0));
            }
        if(todayFlag && sameDay && thisHour>11){
            alert('We are unable to process any same day delivery bookings for today. Please book for any other day for same day delivery.');
            $(container).find('#same-day-toggle').prop('checked', false);
        }else{
            if(sameDay){
                var maxSameDayHr = 11;
                if(zyxCart.carData && zyxCart.carData.car_bike == 'Bike'){
                    maxSameDayHr = 12
                }
                if(hr > maxSameDayHr){
                    $('#same-day-toggle').prop('checked', false);
                    if(maxSameDayHr >= 12){
                    alert('Same day delivery can only be checked for bookings before 12 Noon')
                    }else{
                    alert('Same day delivery can only be checked for bookings before '+maxSameDayHr+' AM');
                    }
                }else{
                $(container).find('#date-time-pair .pick-up-time').timepicker('option', 'maxTime',new Date(0,0,0,maxSameDayHr,0,0));
                }
//                $(container).find('#date-time-pair .pick-up-time').timepicker('setTime',new Date(0,0,0,11,0,0));
            }else{
                $(container).find('#date-time-pair .pick-up-time').timepicker('option', 'maxTime',new Date(0,0,0,16,0,0));
            }
        }
            //$(container).find('.pick-up-time').data('timepicker');

    },



};