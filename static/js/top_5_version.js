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

var chart = Highcharts.chart(paramObj['id'], {
	chart: {
	    backgroundColor: '#353c48',
		spacing : [0, 0 , 0, 0]
	},
	title: {
	    style: {
            color: '#ced4da',
        },
		floating:true,
		text: decodeURIComponent('TOP 5 ' + paramObj['title'])
	},
	tooltip: {
		pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
	},
	plotOptions: {
		pie: {
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
				enabled: false,
				format: '{point.name}',
				style: {
					color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
				}
			},
			point: {
				events: {
                    click: function (event) {
                          window.location.href="/app_management/" + event.point.url + "/version/?VersionName=" + event.point.name;
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
		name: decodeURIComponent( paramObj['count']),
        colors: [
            '#fb9678',
            '#03a9f3',
            '#00c292',
            '#ab8ce4',
            '#01c0c8',
        ],
		data: [
			{
                name: paramObj['name_1'],
                y: parseFloat(paramObj['value_1']),
                url: paramObj['app_pk'],
                sliced: false,
                selected: false
            },
            {
                name: paramObj['name_2'],
                y: parseFloat(paramObj['value_2']),
                url: paramObj['app_pk'],
                sliced: false,
                selected: false
            },
            {
                name: paramObj['name_3'],
                y: parseFloat(paramObj['value_3']),
                url: paramObj['app_pk'],
                sliced: false,
                selected: false
            },
            {
                name: paramObj['name_4'],
                y: parseFloat(paramObj['value_4']),
                url: paramObj['app_pk'],
                sliced: false,
                selected: false
            },
            {
                name: paramObj['name_5'],
                y: parseFloat(paramObj['value_5']),
                url: paramObj['app_pk'],
                sliced: false,
                selected: false
            },
		]
	}]
}, function(c) {
	var centerY = c.series[0].center[1],
		titleHeight = parseInt(c.title.styles.fontSize);
	c.setTitle({
		y:centerY + titleHeight/2
	});
});