function load_role(a){
    if (a == 'manager'){
        $('.result').load('/manager');
        $('.result').css('display', 'block');
    }
    if (a == 'employee'){
        $.get('/pr/get/self',
                function(data){
                    if (data){
                        $('.result').load('pr/get/' + data);}
                    else {$('.result').load('pr/add/{{user.key}}')}
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
