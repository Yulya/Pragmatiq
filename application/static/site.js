function load_role(a, user_key){
    $('#hint').html('');
    if (a == 'manager'){
        $('#settings').css('display','none');
        $('.result').load('/manager');
        $('.result').css('display', 'block');
    }
    if (a == 'employee'){
        $.get('/pr/get/self',
                function(data){
                    if (data){
                        if (data == 'pr not created'){
                            $('.result').css('display', 'block');
                            $('.result').html(data);
                        }
                        else{
                        $('.result').load('pr/get/employee/' + data);
                        }}
                    else {$('.result').load('pr/add/employee/' + user_key)}
        $('.result').css('display', 'block');
        $('#settings').css('display','none');
        })
    }
    if (a == 'hr'){
        $('#settings').css('display','table-cell');
        $('.result').css('display', 'block');
        $('.result').load('/hr');

    }
}

function load(url) {
    $('.result').css('display', 'block');
    $('.result').load(url);
}

function set_result(id, value) {
        $.post('/pr/data/update/'+id,
                {'result': value})
        }

function add_data(obj, form_key){
     var object = $(document).find(obj);
     var table = object.parent().attr('id');
     var button = object.parent().find('.add_button');
     $.post(
            '/pr/data/add',
            {form_key: form_key, table: table},
            function(data){
                var input = $('<input type="text" size="75">');
                input.attr('id',data);
                input.focusout(function(){
                    $.post('/pr/data/update/'+ this.id,{value: this.value});
                    make_text(this)}).insertBefore(button);
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
    input_text.keydown(function (e){
        alert('fgdfg');
    })

    });
    obj.replaceWith(input_text);
    input_text.focus();
}
function make_text(object){
    var obj = $(document).find(object);
    var text = $('<p></p>');
    text.attr('id', obj.id);
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
    $.post('/event/update', {'type': type, 'start': start, 'finish': finish}, function(data){alert(data)})

}
function create_event(obj){
    var object = $(document).find(obj);
    var type = object.parent().find('[name="type"]').val();
    var start = object.parent().find('[name="start"]').val();
    var finish = object.parent().find('[name="finish"]').val();
    $.post('/event/update', {'type': type, 'start': start, 'finish': finish}, function(data){alert(data)})

}
