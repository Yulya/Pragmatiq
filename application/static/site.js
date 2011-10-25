function load_role(a, user_key){
    if (a == 'manager'){
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
        })
    }
    if (a == 'hr'){
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
        make_text(this)

    });
    obj.replaceWith(input_text)
}
function make_text(object){
    var obj = $(document).find(object);
    var text = $('<p></p>');
    text.attr('id', obj.id);
    text.html(obj.val());
    text.click(function(){
        make_input(this)
    });
    obj.replaceWith(text)
}