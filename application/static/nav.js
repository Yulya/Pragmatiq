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
        if (/loaded|complete/.test(document.readyState)) {
            clearInterval(_timer);
            delete _timer;
            init();
        }
    }, 10);
}

// others
window.onload = init;


//On load page, init the timer which check if the there are anchor changes each 300 ms
init(function(){
    setInterval("checkAnchor()", 100);
});

var currentAnchor = '';
//Function which check if there are anchor changes, if there are, sends the ajax petition
function checkAnchor(){
    //Check if it has changes
    if(currentAnchor != document.location.hash){
        if (currentAnchor == null) {
currentAnchor = document.location.hash;
            return
        } else {
currentAnchor = document.location.hash;
        }

var url = currentAnchor.replace('#','');
load(url);

    }
}
