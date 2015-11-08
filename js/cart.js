

var Global = {
    init : function(){
        var _this = this;
        _this.setLogos();
        _this.setLayout();
        _this.eventHandlers();
        Commons.eventHandlers();
        var cookDict = local.load();
        console.log(cookDict)
        var carSelected = null;
        if(cookDict['clgacarname']){
            $('#car-select-box').val(cookDict['clgacarname']);
        }
        $('#car-select-box').trigger('change');
        if(Global.loginFlag){
            local.clearKey('clgacart');
            local.clearKey('clgacartaddi');

        }
           Commons.ajaxData('fetch_additional_details', {}, "GET", _this, _this.updateCartItems );

    },
    setLogos : function(){
        $.each($('img.dealer-logo'), function(i, img){
            var dealer = $(img).attr('alt');
            var carMake = $(img).attr('data-name');
//            console.log(dealer)
            if(dealer == 'Authorized'){
                $(img).attr('src', logoMap['Authorized']+ $.trim(carMake)+'.jpg');
            }else{
                $(img).attr('src', logoMap[dealer]);
//                $(img).attr('src', )
            }
        });
    },
    setLayout : function(){
        var _this = this;
    },
    eventHandlers : function(){
        var _this = this;
        $('#car-select-box').on("change", function(){
            var carVal = $(this).val();
//            console.log(carVal);
            $('table.cart-table').hide();
            $('table.cart-table[data-id="'+carVal+'"]').show();
                var c_name = $(this).find('option:selected').attr('data-name');
                var c_id = $(this).find('option:selected').attr('data-id');
//            console.log(c_name, c_id);
            if(c_name && c_name.length && c_id && c_id.length){
                local.save('clgacarid',c_id);
                local.save('clgacarname',c_name);
            }
        });
        $('#settings-drpdwn').on('click', function(e){
            $(this).parent().find('.logged-user-drpdwn').toggle();
        });

        $('.table-holder').on('click', '.delete-icon', function(e){
            var ts = $(this).closest('tr').attr('ts');
            $(this).closest('tr').remove();
            if(ts && ts.length){
    //            http://local.clickgarage.in/api/add_to_cart/?cookie=1444236368751&delete=true
                Commons.ajaxData('add_to_cart', {'cookie':ts, 'delete':true}, "get", _this, function(){});
            }
        });
        $('.table-holder').on('click', '.max-min', function(e){
            var minDiv = $(this).closest('.additional');
            if(minDiv.hasClass('minimized')){
                minDiv.removeClass('minimized').addClass('maximized');
            }else if(minDiv.hasClass('maximized')){
                minDiv.removeClass('maximized').addClass('minimized');
            }else{
                minDiv.addClass('minimized');
            }
        });
        if(!Global.loginFlag){
            $('.checkout-btn.login-in').on('click', function(){
                $('#sign-up-in-dash').click();
            });
        }
    },
    updateCartItems : function(data){
        $.each(data, function(ts, iData){
            if(iData.additional_data){
                if( $('.table-holder').find('tr[ts="'+ts+'"]') && $('.table-holder').find('tr[ts="'+ts+'"]').length ){
                    var trDiv = $('.table-holder').find('tr[ts="'+ts+'"]').eq(0).find('td.detail .additional');
                    console.log(iData.additional_data)
                    var html_feat = '';
                    var html_custom = '';
                    var html_address = '';
                    $.each(iData.additional_data, function(feat,val){
                        if(feat == 'Custom Requests' && val && val.length){
                            html_custom = '<div>Custom Requests : <span class="cust-feat">'+val+'</span></div>';
                        }else if(feat == 'Damage Type'){
                            if(val && val.length)
                                html_feat = '<div>Damage Type : <span class="cust-feat">'+val+'</span></div>';
                        }else if(feat == 'Selected Authorized'){
                            html_address = '<div>Dealer Name : <span class="d-name">';
//                            console.log(val.name)
                            if(val.name){
                                html_address += val.name
                            }
                            html_address += '</span><br/>Dealer Address : <span  class="d-address">';
                            if(val.address){
                                html_address += val.address
                            }
                            html_address += '</span></div>';
                        }else{
                            if(val && val != 'false'){
                                html_feat += '<span class="ad-feat">'+feat+'</span>';
                            }
                        }
                    });
                    console.log(html_address)
                    html_feat = '<div> Additional Requests : '+html_feat+'</div>';
//                    $(trDiv).text(JSON.stringify(iData.additional_data));
                    $(trDiv).html(html_feat+html_custom+html_address)
                    if($(trDiv).height() > 40){
                        $(trDiv).addClass('minimized').append('<i class="fa max-min"></i>');
                    }

                }
            }
        });
    }

}

$(document).ready(function(){
    Global.init();
});

