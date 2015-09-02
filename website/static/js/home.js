/**
 * Created with PyCharm.
 * User: vociferous
 * Date: 25/07/15
 * Time: 7:30 PM
 * To change this template use File | Settings | File Templates.
 */

var Global = {
    init:function(){
        var _this = this;
        _this.setLayout();
        var cityBoxHolder = $('#home-citybox-holder');
        if(cityBoxHolder.length){
            $(cityBoxHolder).materialDropDown({
                input:".city-search-box",
                dropdown:".city-drop-box"
            });
        }
        var omniBoxHolder = $('#home-omnibox-holder');
        console.log(omniBoxHolder)
        if(omniBoxHolder.length){
            $(omniBoxHolder).materialAutoSuggest({
                input:".omni-search-box",
                dropdown:".omni-drop-box",
                data:_this.carData
            });
        }
        _this.eventHandlers();
        Commons.eventHandlers();
        $('body').scrollTop(0);
        _this.autosliderObj.tmout = setInterval(function(){
            console.log($('#point'+_this.autosliderObj.presentID))
            $('#point'+_this.autosliderObj.presentID).click();
            _this.autosliderObj.presentID += 1;
            if(_this.autosliderObj.presentID > 3){
                _this.autosliderObj.presentID = 1;
            }
        }, 2000);
    },
    autosliderObj : {
        tmout:null,
        presentID:1
    },
        setLayout:function(){
        var scrn_ht = $(window).innerHeight();
        var scrn_wd = $('body').innerWidth();
        $('body').css({
            'height':scrn_ht
        });
        if(scrn_ht < 614){
            scrn_ht = 614
        }
        $('.pane').css({
            height:scrn_ht,
            width:scrn_wd
        });
        var searchContentHolder = $('.search-pane').find('.content-holder');
        var givenHt = searchContentHolder.outerHeight();
        var reqd_offset = (scrn_ht - givenHt)/2;
        searchContentHolder.css({
           'marginTop':reqd_offset
        });

        //video set
        if(scrn_ht > 850){
            var offBottom = scrn_ht-850;
//            console.log(offBottom)

            offBottom =  -230 + offBottom;
//            console.log(offBottom)
            if(offBottom > 0){
                offBottom = 0
            }
//            console.log(offBottom)
            $('.search-pane').find('.overlay-video video').css({
                'bottom': offBottom
            }).attr('data-init', offBottom);
        }
        if(scrn_ht > 1080){
            $('.search-pane').find('.overlay-video video').css({
                'width':'100%'
            })

        }

//        var reqd_offset = scrn_ht/2 - 50;
//        $('#home-search-set-holder').css({
//            'marginTop':reqd_offset
//        });
        $('#workflow-box').css({
            'line-height': (scrn_ht)+'px'
        });
        var toppy = $('.lined-box.workflow-box .pusher-wrapper').position().top;
        $('.lined-box.preview-box .wrapper').css({
            'top':toppy
        });


//        $('#preview-box').find('')
    },
    eventHandlers:function(){
        $(window).on('resize', function(){
            Global.setLayout();
        })
        $(window).on('scroll', function(e){
            var scrn_ht = $(window).innerHeight();
            var scrollTop = $('body').scrollTop();
            var initBot = $('.search-pane').find('.overlay-video video').attr('data-init');
            initBot = parseInt(initBot);
            if(!initBot || isNaN(initBot)){
                initBot = 0
            }
            var toScrollBot = initBot - scrollTop*0.5;
//            console.log(toScrollBot, scrn_ht)
            if(toScrollBot < scrn_ht){
                $('.search-pane').find('.overlay-video video').css({
                    'bottom':toScrollBot
                });
            }

            var toScrollTop = scrollTop - (scrn_ht*2);
            if(toScrollTop >0 && toScrollTop < scrn_ht){
                toScrollTop = toScrollTop*0.5;
                $('.features-pane').find('.overlay-image img').css({
                    'bottom':(0-toScrollTop)
                });
            }else if(toScrollTop < 0 ){
//                $('.features-pane').find('.overlay-image img').animate({
//                    'bottom':"0"
//                },300);
            }
        });

        function DisplayPoint(point){
            var preview = $('.preview-box');
//            console.log(preview.find('.detail-'+point))
//                console.log(preview.find('.detail-'+point).is(':visible'));
            if( !preview.find('.detail-'+point).is(':visible') ){
//                console.log(preview.find('.detail:visible'));
                preview.find('.detail:visible').animate({
                    'left':-100,
                    'opacity':0
                }, 300, function(){
                    $(this).hide();
                });
                preview.find('.detail-'+point).show().css({
                    'left':100
                }).animate({
                    'left':0,
                    'opacity':1
                }, 300, function(){
                });
            }
        }
        $('.workflow-box .marker-point').on('click', function(e){
            if(e.screenX && e.screenX != 0 && e.screenY && e.screenY != 0){
                clearInterval(Global.autosliderObj.tmout);
            }
            var cls = $(this).attr('id');
            DisplayPoint(cls);
            $(this).closest('.workflow-box').find('#pusher').removeClass().addClass(cls);
            e.stopPropagation();
        });
        $('.workflow-box .text-holder').on('click', function(e){
            if(e.screenX && e.screenX != 0 && e.screenY && e.screenY != 0){
                clearInterval(Global.autosliderObj.tmout);
            }
            var cls = $(this).attr('data-id')
            DisplayPoint(cls);
            $(this).closest('.workflow-box').find('#pusher').removeClass().addClass(cls);
        });
        $('#settings-drpdwn').on('click', function(e){
            $(this).parent().find('.logged-user-drpdwn').toggle();
        });
        $('#home-search-form').on('submit', function(e){
//           var value = $(this).find('#omni-search-box').attr('data-id');
            var c_id = $(this).find('#hidden-id-box').val();
            if (!c_id.length){
                return false
            }else{
               $(this).find('#omni-search-box').remove();
            }
        });
        $('.learn-more').on('click', function(e){
            $('body').animate(
                {'scrollTop':$('.search-pane').outerHeight()},
                500
            );
        })
    },
    paneScrolls:function(){

    },
    carData:null
};

//var Plugins = {
//    materialDropDown : function(options){
//        if(options.input && options.dropdown){
//            this.input = options.input;
//            this.dropdown = options.dropdown;
//            $(input).off.on('click', function(){
//                $(dropdown).
//            })
//        }
//
//    }
//}

$(document).ready(function(){
    Global.init();
});