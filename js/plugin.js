function Trie(key) {
    this.value;
    this.key = key;
}

Trie.prototype.put = function (name, value) {
    var node = this,
        nameLength = name.length,
        i = 0,
        currentLetter;

    //if the node exists, make it current and proceed
    //if not, we create it, make it current and proceed
    for (i = 0; i < nameLength; i++) {
        currentLetter = name[i].toLowerCase();
        node = node[currentLetter] || (node[currentLetter] = new Trie(currentLetter));
    }
    node.name = name;
    node.value = value;
};

Trie.prototype.get = function (name) {

    var node = this,
        nameLength = name.length,
        i, node;

    //same idea, zip through the collection
    //in this case we break if we hit a dead end
    for (i = 0; i < nameLength; i++) {
        if (!(node = node[name[i]].toLowerCase())) break;
    }

    //only when the loop went over all letters will we find a value
    //if not, well, we don't find anything
    return (i === nameLength) ? node.value : 'not found';
};

Trie.prototype.getAutoSuggest = function(name) {
    var node = this,
        nameLength = name.length,
        i, node;

    for (i = 0; i < nameLength; i++) {
        if (!(node = node[name[i].toLowerCase()])) break;
    }
    //found results
    if (i === nameLength) {
        return node.addValues([]);
    }
    //
    else {
        return [];
    }

};

Trie.prototype.getAutoSuggestObjs = function(name) {
    var node = this,
        nameLength = name.length,
        i, node;

    for (i = 0; i < nameLength; i++) {
        if (!(node = node[name[i].toLowerCase()])) break;
    }
    //found results
    if (i === nameLength) {
        return node.addValueObjs([]);
    }
    //
    else {
        return [];
    }
};

Trie.prototype.addValues = function(array) {
    var arry = array;
    var check = ''
    var dict = this;
    if (this.name)
        arry.push(this.name);
    for (var key in dict) {
        if (dict[key] instanceof Trie) {
            dict[key].addValues(arry);
        }
    }
    return arry;
};
Trie.prototype.addValueObjs = function(array) {
    var arry = array;
    var check = ''
    var dict = this;
    if (this.name)
        arry.push({'name':this.name,'val':this.value});
    for (var key in dict) {
        if (dict[key] instanceof Trie) {
            dict[key].addValueObjs(arry);
        }
    }
    return arry;

};

var Keys = {
    UP : 38,
    DOWN : 40,
    ENTER : 13
};

$.fn.materialDropDown = function(options) {

    function matDrpDwn(wrapper, inp, drp, drplist){

//        this.input = $(inp);
//        this.dropdown = $(drp);
//        this.dropholder = $(drplist);
//        this.wrapper = $(wrapper);

        if(wrapper){
            this.wrapper = $(wrapper);

            this.input = $(wrapper).find(inp);
            this.dropdown = $(wrapper).find(drp);
            this.dropholder = $(wrapper).find(drplist);
            this.suggestTimeout = null;
            this.trieData = null;
        }else{
            this.input = $(inp);
            this.dropdown = $(drp);
            this.dropholder = $(drplist);
            this.wrapper = $(wrapper);
            this.suggestTimeout = null;
            this.trieData = null;
        }
    }

    matDrpDwn.prototype.applySettings = function(options){
        var _this = this;
        console.log(options);
        console.log(_this);
        if(options.inpClass)
            _this.input.addClass(options.inpClass);
        if(options.drpClass)
            _this.dropdown.addClass(options.drpClass);
        if(options.wrapClass)
            _this.wrapper.addClass(options.wrapClass);
        if(options.DDID)
            _this.wrapper.attr('data-id', options.DDID);
    };

    matDrpDwn.prototype.events = function(){
        var _this = this;
        $(_this.input).off().on('click', function(e){
            $(_this.dropdown).toggle();
            if($(_this.dropdown).is(':visible')){
                $(_this.dropdown).animate({'opacity':1},400);
            }else{
                $(_this.dropdown).animate({'opacity':0},400);
            }
        });

        $(_this.dropdown).off().on('click','li', function(e){
            $(_this.input).val($(this).text());
        });
        $(document).on('click', function(e){
            var target = $(e.target);
            if(!target.closest('div[data-id="'+_this.settings.DDID+'"]').length){
                console.log('outclick')
                $(_this.dropdown).hide();
            }
        });

    };

    if(options.input && options.dropdown){
        var settings = $.extend(true, {
            inpClass : 'mat-drp-inp-box',
            drpClass : 'mat-drp-slct-box',
            wrapClass : 'mat-drp-dwn',
            DDID : 'dropdown-'+(new Date()).getTime()
        }, options.settings);
        var drplst = null;
        if(settings.droplist){
            drplst = options.droplist
        }else{
            drplst = $(options.dropdown).find('ul');
        }
        return this.each(function(){
            var _this = $(this);
            var myMatDrpDwn = new matDrpDwn(_this, options.input, options.dropdown, drplst);
            myMatDrpDwn.settings = settings;
            myMatDrpDwn.applySettings(settings);
            myMatDrpDwn.events();
            _this.data('drpdwn',myMatDrpDwn).addClass('active-mat-drp');
        });
    }else{
        return this;
    }

};

$.fn.materialAutoSuggest = function(options, data) {

    function matAutoSuggest(wrapper, inp, drp, drplist){
        if(wrapper){
            this.wrapper = $(wrapper);

            this.input = $(wrapper).find(inp);
            this.dropdown = $(wrapper).find(drp);
            this.droplist = $(wrapper).find(drplist);
            this.suggestTimeout = null;
            this.trieData = null;
        }else{
            this.input = $(inp);
            this.dropdown = $(drp);
            this.droplist = $(drplist);
            this.wrapper = $(wrapper);
            this.suggestTimeout = null;
            this.trieData = null;
        }
    }
    matAutoSuggest.prototype.setData = function(data){
        var _this = this;
        var car_word_map = {};
        $.each(data, function(idx,val){
            var car_name = [val['make'],val['name']].join(' ');
            var word_array = car_name.split(' ');
            var car_id = val['id']
            $.each(word_array, function(ix, vl){
                if(!car_word_map[vl]){
                    car_word_map[vl] = [{name:car_name, id:car_id}];
                }else{
                    car_word_map[vl].push({name:car_name, id:car_id});
                }
            });
        });

        _this.trieData = new Trie();
        $.each(car_word_map, function(word, array){
//            console.log(word, array)
            _this.trieData.put(word, array);
        });
        _this.data = data;
//        console.log(_this.trieData);
    }
    matAutoSuggest.prototype.applySettings = function(options){
        var _this = this;
        console.log(options);
        console.log(_this);
        if(options.inpClass)
            _this.input.addClass(options.inpClass);
        if(options.drpClass)
            _this.dropdown.addClass(options.drpClass);
        if(options.wrapClass)
            _this.wrapper.addClass(options.wrapClass);
        if(options.ASID)
            _this.wrapper.attr('data-id', options.ASID);
    };
    matAutoSuggest.prototype.populateSuggest = function(){
        var _this = this;
        var val = _this.input.val();
        _this.droplist.find("li").remove();
        var newList = [];
        var completeNameDict = {};
        var completeDict = {};
        $.each(val.split(' '), function(ix, vl){
            if(vl.length){
                newList.push(_this.trieData.getAutoSuggestObjs(vl));
            }
        });
        var words = 0
        $.each(newList, function(idx,val){
            console.log(idx,val)
            $.each(val, function(ix,vl){
                console.log(ix,vl)
                $.each(vl.val, function(i,v){
                    var name = v.name;
                    var id = v.id;
                        completeNameDict[id] = name;
                    if(completeDict[id]){
                        completeDict[id] += 1;
                    }
                    else{
                        completeDict[id] = 1;
                    }
                });
            });
        words = (idx+1);
        });
        $.each(completeDict, function(i,v){
                //second onwards, overlap
            if(v == words){
                _this.droplist.append("<li data-id='"+i+"' >"+completeNameDict[i]+"</li>");
            }
        });
        _this.droplist.find('li').eq(0).addClass('spotlight');
        _this.dropdown.show().animate({'opacity':1});
//        if(_this.TrieData){
//
//        }
    }
    matAutoSuggest.prototype.events = function(){
        var _this = this;
        $(_this.input).off().on('click', function(e){
            $(_this.dropdown).toggle();
            if($(_this.dropdown).is(':visible')){
                _this.populateSuggest();
                $(_this.dropdown).animate({'opacity':1},400);
            }else{
                $(_this.dropdown).animate({'opacity':0},400);
            }
        });
        $(_this.input).on('change', function(e){
            $(this).siblings('#hidden-id-box').removeAttr('value');
        });
        $(_this.input).on('keydown', function(e){
            var keyCode = e.keyCode;
            var fallThrough = false;
            switch (keyCode){
                case Keys.UP:
                    if(!_this.droplist.find('li').length){
                        fallThrough = true;
                    }
                    if(!fallThrough){
                        $(this).siblings('#hidden-id-box').removeAttr('value');
                        if(_this.droplist.find('li.spotlight').length){
                            if(_this.droplist.find('li.spotlight').prev().length){
                                _this.droplist.find('li.spotlight').removeClass('spotlight').prev().addClass('spotlight')
                            }else if(_this.droplist.find('li.spotlight').next().length){
                                _this.droplist.find('li.spotlight').removeClass('spotlight');
                                _this.droplist.find('li:last-child').addClass('spotlight');
                            }else{
                                //dhating naach
                            }
                        }
//                        $(_this)
                        break;
                    }
                case Keys.DOWN:
                    if(!fallThrough){
                        $(this).siblings('#hidden-id-box').removeAttr('value');
                        if(_this.droplist.find('li.spotlight').length){
                            if(_this.droplist.find('li.spotlight').next().length){
                                _this.droplist.find('li.spotlight').removeClass('spotlight').next().addClass('spotlight')
                            }else if(_this.droplist.find('li.spotlight').prev().length){
                                _this.droplist.find('li.spotlight').removeClass('spotlight');
                                _this.droplist.find('li:first-child').addClass('spotlight');
                            }else{
                                //dhating naach
                            }
                        }
                        break;
                    }
                case Keys.ENTER:
                    if(!fallThrough){
                        if(_this.droplist.find('li.spotlight').length){
                            var text = _this.droplist.find('li.spotlight').text();
                            var id = _this.droplist.find('li.spotlight').attr('data-id');
                            _this.input.val(text);
                            _this.input.siblings('#hidden-id-box').val(id);
                        }
                        $(_this.dropdown).hide();
                        break;
                    }
                default:
                    $(this).siblings('#hidden-id-box').removeAttr('value');
                    if(fallThrough){
                        clearTimeout(_this.suggestTimeout);
                        _this.suggestTimeout = setTimeout(function(){
                            _this.populateSuggest();
                        }, 100);
                    }else{
                        clearTimeout(_this.suggestTimeout);
                        _this.suggestTimeout = setTimeout(function(){
                            _this.populateSuggest();
                        }, 100);
                    }
                    break;

            }
        });

        $(_this.dropdown).off().on('click','li', function(e){
            _this.input.val($(this).text());
            _this.input.siblings('#hidden-id-box').val($(this).attr('data-id'));
        });
        $(_this.wrapper).on('click', function(e){

        });
        $(_this.dropdown).on('mouseover', 'li', function(e){
            $(this).siblings().removeClass('spotlight');
            $(this).addClass('spotlight');
        });
        $(document).on('click', function(e){
            console.log(e)
            var target = $(e.target);
            if(!target.closest('div[data-id="'+_this.settings.ASID+'"]').length){
                console.log('outclick')
                $(_this.dropdown).hide();
            }
        });
    }
    if(options.input && options.dropdown){
        var settings = $.extend(true, {
            inpClass : 'mat-drp-inp-box',
            drpClass : 'mat-drp-slct-box',
            wrapClass : 'mat-drp-dwn',
            ASID : 'autosuggest-'+(new Date()).getTime()
        }, options.settings);
        var drplst = null;
        if(settings.droplist){
            drplst = options.droplist
        }else{
            drplst = $(options.dropdown).find('ul');
        }
        return this.each(function(){
            var _this = $(this);

            var myAutoSuggest = new matAutoSuggest(_this, options.input, options.dropdown, drplst);
            myAutoSuggest.settings = settings;
            if(options.data){
                myAutoSuggest.setData(options.data);
            }
            myAutoSuggest.applySettings(settings);
            myAutoSuggest.events();
            _this.data('suggest',myAutoSuggest).addClass('active-mat-drp');
        });
    }else{
        return this;
    }
};
