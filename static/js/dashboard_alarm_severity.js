function getParam() {
        var js = document.getElementsByTagName("script");
        var arraytemp = js[js.length - 1].src.split('?');
        var obj = {};
        if (arraytemp.length > 1) {
            var params = arraytemp[1].split('&');
            for (var i = 0; i < params.length; i++) {
                var parm = params[i].split("=");
                obj[parm[0]] = parm[1];
            }
        }
        return obj;
    }
var paramObj = getParam();

var chart = Highcharts.chart('alarm_security', {
	chart: {
		backgroundColor: '#353c48',
		spacing : [0, 0 , 0, 0]
	},
	title: {
		style: {
            color: '#ced4da',
        },
		floating:true,
		text: 'Alarm Severity'
	},
	tooltip: {
		pointFormat: '{series.name}: <b>{point.y} ({point.percentage:.1f}%)</b>'
	},
	plotOptions: {
		pie: {
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
				enabled: false,
				format: '<b>{point.name}</b>: {point.y}',
				style: {
					color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
				}
			},
			point: {
				events: {
					click: function (event) {
                         window.location.href="alarms/?EventTypeName=" + event.point.name;
                      }
				}
			},
		}
	},
	series: [{
		type: 'pie',
		borderColor: '#353c48',
        borderWidth: 0,
		innerSize: '85%',
		name: 'Alarm',
        colors: [
            '#fb9678',
            '#9675ce',
            // '#01c0c8',
        ],
		data: [
		    ['Error', parseInt(paramObj['error_count'])],
            ['Warning', parseInt(paramObj['warning_count'])],
            // ['Info',   parseInt(paramObj['info_count'])],
		]
	}]
}, function(c) {
	var centerY = c.series[0].center[1],
		titleHeight = parseInt(c.title.styles.fontSize);
	c.setTitle({
		y:centerY + titleHeight/2
	});
});