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