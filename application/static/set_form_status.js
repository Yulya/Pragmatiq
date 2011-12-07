function maf_draft(name){
    $.get('/pr/manager/draft/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have cancelled submitting ' + name + ' form ';
                window.location.href = "/#/manager";
            }
            })
}
function register(name){
    $.get('/pr/manager/register/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have cancelled approving ' + name + ' form ';
                window.location.href = "/#/manager";
            }
            })
}

function approve(name){
    $.get('/pr/manager/approve/' + form_key, function(data){
        if (data == 'ok'){
            message = 'You have approved ' + name + ' form ';
            window.location.href = "/#/manager";
        }
    });

}
function maf_submit(name){
            $.get('/pr/manager/submit/' + form_key, function(data){
            if (data == 'ok'){
                message = 'You have submitted ' + name + ' form ';
                window.location.href = "/#/manager";
            }
            })
}
function check_form(){
    $.get('pr/manager/check/' + form_key, function(data){
        if (data){if (confirm('Unfilled fields: ' + data + '. Continue?')){
                  approve();}
                 }
        else {approve()}

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
                message = 'You have cancelled submitting form ';
                window.location.href = "/#/employee";
            }
            })

}