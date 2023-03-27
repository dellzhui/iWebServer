function getParam() {
    var js = document.getElementsByTagName("script");
    var arraytemp = js[js.length - 1].src.split('#?');
    var obj = {};
    if (arraytemp.length > 1) {
        var params = arraytemp[1].split('#&');
        for (var i = 0; i < params.length; i++) {
            var parm = params[i].split("#=");
            obj[parm[0]] = parm[1];
        }
    }
    return obj;
}

var paramObj = getParam();
// if(paramObj['name_1'] === '') {
//     paramObj['value_1'] = '100';
//     paramObj['url_1'] = 'javascript:void(0)';
// }

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
                          window.location.href=event.point.url;
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
                name: decodeURIComponent(paramObj['name_1']),
                y: parseInt(paramObj['value_1']),
                url: paramObj['url_1'],
                sliced: false,
                selected: false
            },
            {
                name: decodeURIComponent(paramObj['name_2']),
                y: parseInt(paramObj['value_2']),
                url: paramObj['url_2'],
                sliced: false,
                selected: false
            },
            {
                name: decodeURIComponent(paramObj['name_3']),
                y: parseInt(paramObj['value_3']),
                url: paramObj['url_3'],
                sliced: false,
                selected: false
            },
            {
                name: decodeURIComponent(paramObj['name_4']),
                y: parseInt(paramObj['value_4']),
                url: paramObj['url_4'],
                sliced: false,
                selected: false
            },
            {
                name: decodeURIComponent(paramObj['name_5']),
                y: parseInt(paramObj['value_5']),
                url: paramObj['url_5'],
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