function maf_draft(name, flag){
    $.get('/pr/manager/draft/' + form_key, function(data){
            if (data == 'ok'){
                if (!flag){
                message = 'You have successfully cancelled submitting <a href="/#/manager/pr/get/manager/' + form_key + '">' + name +
                    '</a> form. <a href="#" onclick="maf_submit(name, true); return false">Undo</a>';
                window.location.href = "/#/manager/get/all";}
             else{
                window.location.href = "/#/manager/pr/get/manager/"+ form_key}
            }
            })
}
function register(name, flag){
    $.get('/pr/manager/register/' + form_key, function(data){
            if (data == 'ok'){
                if (!flag){
                message = 'You have successfully cancelled approving <a href="/#/manager/pr/get/manager/'+ form_key + '">' + name +
                    '</a> form. <a href="#" onclick="approve(name, true); return false">Undo</a>';
                window.location.href = "/#/manager/get/all";}
                else{
                window.location.href = "/#/manager/pr/get/manager/"+ form_key}
            }
            })
}

function approve(name, flag){
    $.get('/pr/manager/approve/' + form_key, function(data){
        if (data == 'ok'){
            if (!flag){
            message = 'You have successfully approved <a href="/#/manager/pr/get/manager/'+ form_key + '">' + name +
                '</a> form. <a href="#" onclick="register(name, true); return false">Undo</a>';
            window.location.href = "/#/manager/get/all";}
            else{
                window.location.href = "/#/manager/pr/get/manager/"+ form_key}
        }
    });

}
function maf_submit(name, flag){
            $.get('/pr/manager/submit/' + form_key, function(data){
            if (data == 'ok'){
                if (!flag){
                message = 'You have  successfully submitted <a href="/#/manager/pr/get/manager/'+ form_key + '">' + name +
                    '</a> form. <a href="#" onclick="maf_draft(name, true); return false">Undo</a>';
                window.location.href = "/#/manager/get/all";}
                else{
                    window.location.href = "/#/manager/pr/get/manager/"+ form_key}
            }
            });
}
function check_form(name){
    $.get('pr/manager/check/' + form_key, function(data){
        if (data){if (confirm('Unfilled fields: ' + data + '. Continue?')){
                  approve(name);}
                 }
        else {approve(name)}

    })
}
function eaf_submit(flag){
                    $.get('/pr/employee/submit/' + form_key,
                            function(data){
                                if (data == 'ok'){
                                    if (!flag){
                                message = 'You have successfully submitted form. <a href="#" onclick="eaf_draft(true); return false">Undo</a>';
                                window.location = '/#/employee';}
                                    else{
                                    window.location.href = "/#/employee/pr/get/employee/"+ form_key}
                                }
                        })
                    }
function eaf_draft(flag){
    $.get('/pr/employee/draft/' + form_key, function(data){
            if (data == 'ok'){
                if (!flag){
                message = 'You have successfully cancelled submitting form. <a href="#" onclick="eaf_submit(true); return false">Undo</a>';
                window.location.href = "/#/employee";}
                else{
                   window.location.href = "/#/employee/pr/get/employee/"+ form_key}
            }
            })

}