function maf_draft(name){
    $.get('/pr/manager/draft/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have successfully cancelled submitting ' + name + ' form ';
                window.location.href = "/#/manager";
            }
            })
}
function register(name){
    $.get('/pr/manager/register/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have successfully cancelled approving ' + name + ' form ';
                window.location.href = "/#/manager";
            }
            })
}

function approve(name){
    $.get('/pr/manager/approve/' + form_key, function(data){
        if (data == 'ok'){
            message = 'You have successfully approved ' + name + ' form ';
            window.location.href = "/#/manager";
        }
    });

}
function maf_submit(name){
            $.get('/pr/manager/submit/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have  successfully submitted ' + name + ' form ';
                window.location.href = "/#/manager";
            }
            })
}
function check_form(name){
    $.get('pr/manager/check/' + form_key, function(data){
        if (data){if (confirm('Unfilled fields: ' + data + '. Continue?')){
                  approve(name);}
                 }
        else {approve(name)}

    })
}
function eaf_submit(){
                    $.get('/pr/employee/submit/' + form_key,
                            function(data){
                                if (data == 'ok'){
                                window.location = '/#/employee';
                                }
                        })
                    }
function eaf_draft(){
    $.get('/pr/employee/draft/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have successfully cancelled submitting form ';
                window.location.href = "/#/employee";
            }
            })

}