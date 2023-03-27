function getParam() {
    var js = document.getElementsByTagName("script");
    var arraytemp = js[js.length - 1].src.split('?');
    var obj = {};
    if (arraytemp.length > 1) {
        var params = arraytemp[1].split('&');
        for (var i = 0; i < params.length; i++) {
            var parm = params[i].split("=");
            obj[parm[0]] = parm[1].replace('%20', ' ');
        }
    }
    return obj;
}

var paramObj = getParam();
var duration_s = parseInt(paramObj['duration']);

function idms_refrash() {
    window.location.reload();
}

countdown_index = duration_s - 1;
var intervalid;
intervalid = setInterval("fun()", 1000);
function fun() {
    if (countdown_index === 0) {
        clearInterval(intervalid);
    } else {
        document.getElementById("mtr_reload").innerHTML = countdown_index;
    }
    countdown_index--;
}

setTimeout('idms_refrash()', duration_s * 1000);