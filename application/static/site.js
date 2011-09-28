function load_role(a){
    if (a == 'manager'){
        $('.result').load('/manager');
    }
    if (a == 'employee'){
        $.get('/pr/get/self',
                function(data){
                    if (data){
                        $('.result').load('pr/get/' + data);}
                    else {$('.result').load('pr/add/{{user.key}}')}
        })
    }
    if (a == 'hr'){
        $('.result').load('/hr');

    }
}

function load(url) {
    alert(url)
    $('.result').load(url);
}
