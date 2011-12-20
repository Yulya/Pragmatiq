function load_role(a, user_key){
    if (a == 'manager'){
        $('#settings').css('display','table-cell');
        window.location = '/#/manager/home'
    }
    if (a == 'employee'){
        $('#settings').css('display','none');
        window.location = '/#/employee';}
    
    if (a == 'hr'){
        $('#settings').css('display','table-cell');
        window.location = '/#/hr'

    }
}
function parent_replace(obj){
    $(document).find(obj).parent().replaceWith('')
}
function hide_hint(){
      $('#hint').css('display', 'none');
    }

function load(url) {
    editing_form_open = false;
    
    $('.result').css('display', 'block');
    $('.result').load(url);
    if (lock_timer){
        clearInterval(lock_timer);
    }
    if (unlock_timer){
        clearInterval(unlock_timer);
    }
    if (message){
        $('#hint').find('.message').html(message);
        message = '';
        $('#hint').css('display', 'block');
        setTimeout('hide_hint()', 30000);
    }
    else{
        hide_hint()
    }

}

function set_result(id, value) {
        $.post('/pr/data/update/'+id,
                {'result': value})
        }

function update_data(id,value){
    $.post('/pr/data/update/'+ id, {value: value});
}
function add_textarea(obj, form_key){
     var object = $(document).find(obj);
     var table = object.parent().attr('id');
     var button = object.parent().find('.add_button');
     var ul =  object.parent().find('ul');
     $.post(
            '/pr/data/add',
            {form_key: form_key, table: table},
            function(data){
                var input = $('<textarea rows="4" cols="40"></textarea>');
                input.attr('id',data);
                input.keypress(function(e){
                    if (e.keyCode == '13'){
                        add_data(input, form_key);
                    }
                });
                input.focusout(function(){
                    update_data(this.id,this.value);
                    make_text(this)});
                input.insertBefore(button);
                input.focus();
                    });

     }
function make_textarea(object){
    var obj = $(document).find(object);
    var input_text = $('<textarea rows="4" cols="40"></textarea>');
    input_text.attr('id', obj.attr('id'));
    input_text.html(obj.html());
    input_text.focusout(function(){
        $.post('/pr/data/update/'+ this.id,{value: this.value});
        make_text(this);
    });
    input_text.keypress(function(e){
                    if (e.keyCode == '13'){
                        make_text(this);
                    }
                });
    obj.replaceWith(input_text);
    input_text.focus();
}
function add_data(obj, form_key){
     var object = $(document).find(obj);
     var table = object.parent().attr('id');
     var button = object.parent().find('.add_button');
     var ul =  object.parent().find('ul');
     $.post(
            '/pr/data/add',
            {form_key: form_key, table: table},
            function(data){
                var input = $('<input type="text" size="75">');
                input.attr('id',data);
                input.keypress(function(e){
                    if (e.keyCode == '13'){
                        add_data(input.parent(), form_key);
                    }
                });
                input.focusout(function(){
                    update_data(this.id,this.value);
                    make_text(this)}).appendTo(ul);
                    input.focus();
                    });

     }

function send_value(id, value) {
   $.post('/pr/data/update/'+ id, {value: value});
}

function make_input(object){
    var obj = $(document).find(object);
    var input_text = $('<input type="text" size="75">');
    input_text.attr('id', obj.attr('id'));
    input_text.attr('value', obj.html());
    input_text.focusout(function(){
        $.post('/pr/data/update/'+ this.id,{value: this.value});
        make_text(this);
    });
    input_text.keypress(function(e){
                    if (e.keyCode == '13'){
                        make_text(this);
                    }
                });
    obj.replaceWith(input_text);
    input_text.focus();
}

function make_text(object){
    var obj = $(document).find(object);
    var text = $('<li></li>');
    text.attr('id', obj.attr('id'));
    text.html(obj.val());
    text.click(function(){
        make_input(this)
    });
    if (obj.val() == ''){
        obj.replaceWith('');
    }
    else{obj.replaceWith(text)}
    
}

function display(obj){
    var object = $(document).find(obj);
    object.parent().find('div').css('display', 'block');
    object.attr('onclick', 'hide(this)');
}
function hide(obj){
    var object = $(document).find(obj);
    object.parent().find('div').css('display', 'none');
    object.attr('onclick', 'display(this)');
}
function update_event(obj){
    var object = $(document).find(obj);
    var type = object.parent().attr('id');
    var start = object.parent().find('[name="start"]').val();
    var finish = object.parent().find('[name="finish"]').val();
    var first_date = object.parent().find('[name="first_date"]').val();
    $.post('/event/update', {'type': type, 'start': start, 'finish': finish, 'first_date': first_date}, function(data){alert(data)})

}
function create_event(obj){
    var object = $(document).find(obj);
    var type = object.parent().find('[name="type"]').val();
    var start = object.parent().find('[name="start"]').val();
    var finish = object.parent().find('[name="finish"]').val();
    var first_date = object.parent().find('[name="first_date"]').val();
    $.post('/event/update', {'type': type, 'start': start, 'finish': finish, 'first_date': first_date}, function(data){
        if (data == 'ok'){
        message = "You've created new event";
        load('/hr/settings');
        message = ""}
    })

}
