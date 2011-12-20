function send_lock_request(){
    if (editing_form_open){

        $.get('/lock_form/' + form_key, function(data){
        if (data != 'ok'){
            message = data;
            load(document.location.hash.replace('#',''));
        }
    })
    }
    }
function lock_form(){
    
        return setInterval('send_lock_request()', 30000);
}

function send_unlock_request(){
    if (editing_form_open){
        $.get('/lock_form/' + form_key, function(data){
        if (data != 'ok'){
            $('#lock_info').html(data).css('display', 'block');
        }
        else{
            message = "form is unlocked";
            load(document.location.hash.replace('#',''));
            }
        })}
        }
function unlock_form(){

      return setInterval('send_unlock_request()', 30000);}