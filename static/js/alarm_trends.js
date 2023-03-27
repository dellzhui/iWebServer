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
var is_local_deploy = "True";
if (paramObj['is_local_deploy'] !=null){
    is_local_deploy = paramObj['is_local_deploy'] ;
}
if (is_local_deploy != "True"){
    new Chart(document.getElementById(paramObj['id']), {
      type: 'line',
      data: {
        labels: [paramObj['labels_1'],paramObj['labels_2'],paramObj['labels_3'],paramObj['labels_4'],paramObj['labels_5'],paramObj['labels_6'],paramObj['labels_7'],paramObj['labels_8'],paramObj['labels_9'],paramObj['labels_10'], paramObj['labels_11'], paramObj['labels_12'], paramObj['labels_13'], paramObj['labels_14']],
        datasets: [{
            data: [paramObj['error_1'],paramObj['error_2'],paramObj['error_3'],paramObj['error_4'],paramObj['error_5'],paramObj['error_6'],paramObj['error_7'],paramObj['error_8'],paramObj['error_9'],paramObj['error_10'], paramObj['error_11'], paramObj['error_12'], paramObj['error_13'], paramObj['error_14']],
            // label: "Error",
            label: decodeURIComponent(paramObj['labels_0']),
            borderColor: "#fb9678",
            "pointBackgroundColor":"#fb9678",
            "pointBorderColor":"#fb9678",
            "pointBorderWidth":5,
            "pointRadius":1,
            fill: false
          }
          , {
            data: [paramObj['qoe_1'],paramObj['qoe_2'],paramObj['qoe_3'],paramObj['qoe_4'],paramObj['qoe_5'],paramObj['qoe_6'],paramObj['qoe_7'],paramObj['qoe_8'],paramObj['qoe_9'],paramObj['qoe_10'], paramObj['qoe_11'], paramObj['qoe_12'], paramObj['qoe_13'], paramObj['qoe_14']],
            label: "QoE",
            borderColor: "#9675ce",
            "pointBackgroundColor":"#9675ce",
            "pointBorderColor":"#9675ce",
            "pointBorderWidth":5,
            "pointRadius":1,
            fill: false
          }
        ]
      },
      options: {
        title: {
          display: false,
          // text: 'Alarm Trends'
        }
      }
    });
}else {
        new Chart(document.getElementById(paramObj['id']), {
      type: 'line',
      data: {
        labels: [paramObj['labels_1'],paramObj['labels_2'],paramObj['labels_3'],paramObj['labels_4'],paramObj['labels_5'],paramObj['labels_6'],paramObj['labels_7'],paramObj['labels_8'],paramObj['labels_9'],paramObj['labels_10'], paramObj['labels_11'], paramObj['labels_12'], paramObj['labels_13'], paramObj['labels_14']],
        datasets: [{
            data: [paramObj['error_1'],paramObj['error_2'],paramObj['error_3'],paramObj['error_4'],paramObj['error_5'],paramObj['error_6'],paramObj['error_7'],paramObj['error_8'],paramObj['error_9'],paramObj['error_10'], paramObj['error_11'], paramObj['error_12'], paramObj['error_13'], paramObj['error_14']],
            // label: "Error",
            label: decodeURIComponent(paramObj['labels_0']),
            borderColor: "#fb9678",
            "pointBackgroundColor":"#fb9678",
            "pointBorderColor":"#fb9678",
            "pointBorderWidth":5,
            "pointRadius":1,
            fill: false
          }
        ]
      },
      options: {
        title: {
          display: false,
          // text: 'Alarm Trends'
        }
      }
    });
}