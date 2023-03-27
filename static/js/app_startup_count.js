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

new Chart(document.getElementById(paramObj['id']), {
  type: 'line',
  data: {
    labels: [paramObj['labels_1'],paramObj['labels_2'],paramObj['labels_3'],paramObj['labels_4'],paramObj['labels_5'],paramObj['labels_6'],paramObj['labels_7']/*,paramObj['labels_8'],paramObj['labels_9'],paramObj['labels_10'], paramObj['labels_11'], paramObj['labels_12'], paramObj['labels_13'], paramObj['labels_14']*/],
    datasets: [{
        data: [/*20 ,80,70,140,140,80, 200,*/paramObj['count_1'],paramObj['count_2'],paramObj['count_3'],paramObj['count_4'],paramObj['count_5'],paramObj['count_6'],paramObj['count_7']/*,paramObj['count_8'],paramObj['count_9'],paramObj['count_10'], paramObj['count_11'], paramObj['count_12'], paramObj['count_13'], paramObj['count_14']*/],
        label: decodeURIComponent(paramObj['labels_0']),
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
