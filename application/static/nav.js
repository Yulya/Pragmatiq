/**
* Javascript anchor navigation
*/

function init(delegate) {
    if (arguments.callee.done) return;
    arguments.callee.done = true;
    delegate();
}

// ff, opera
if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", init, false);
}

// ie
/*@cc_on @*/
/*@if (@_win32)
document.write("<script id=__ie_onload defer src=javascript:void(0)>");
document.write("<\/script>");
var script = document.getElementById("__ie_onload");
script.onreadystatechange = function() {
if (this.readyState == "complete") {
init();
}
};
/*@end @*/

// safari
if (/WebKit/i.test(navigator.userAgent)) {
    var _timer = setInterval(function() {
        if (/complete/.test(document.readyState)) {
            clearInterval(_timer);
            delete _timer;
            init();
        }
    }, 10);
}

// others
window.onload = init;

var message = '';
var lock_timer = false;
var unlock_timer = false;
var editing_form_open = false;
//On load page, init the timer which check if the there are anchor changes each 300 ms
init(function(){
    setInterval("checkAnchor()", 500);
});

var currentAnchor = document.location.hash;
console.log('init');

    //Function which check if there are anchor changes, if there are, sends the ajax petition
function checkAnchor(){
    //Check if it has changes
    if(currentAnchor != document.location.hash){
        console.log('anchor changed');
    currentAnchor = document.location.hash;

var url = currentAnchor.replace('#','');
url = encodeURI(url);
        console.log('3');

var role = url.split("/")[1];

if (role == 'manager'){
    $('#settings').html('<a href="#/manager/settings">settings</a>').css('display','table-cell');
}
if (role == 'hr'){
        $('#settings').html('<a href="#/hr/settings">settings</a>').css('display','table-cell');
}
if (role == 'employee'){
    $('#settings').html('').css('display','none');
}
        console.log('4');

$('.select_role').val(role);
        console.log('5');


load(url);
        console.log('6');

}
    }

