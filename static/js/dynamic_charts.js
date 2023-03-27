var chart_cpu_usage;
var chart_cpu_termperature;
var chart_cpu_current_freq;
var flag = 1;

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

//更新
function requestData() {
 var stime = new Date();
    $.ajax({
        url:'data/',
        // async:false,
        success: function(point) {

       /*if(!chart_cpu_usage){
             setTimeout(requestData, 1000);
           return
                                 }   */
        var x = (new Date()).getTime() + 8*3600*1000; // 当前时间
        var out = eval("(" + point + ")");
        cpurate = out[0];
        cpu_termperature = out[1];
        cpu_current_freq = out[2];
       if(cpurate == 100) {
           cpurate = 99.9;
       }
        if(flag === 1){
            cpurate = 0;
            cpu_termperature = 0;
            cpu_current_freq = 0;
            flag =0
        }
       chart_cpu_usage.series[0].addPoint([x,cpurate], true, true);
       chart_cpu_termperature.series[0].addPoint([x,cpu_termperature], true, true);
       chart_cpu_current_freq.series[0].addPoint([x,cpu_current_freq], true, true);

       var etime = new Date();
       d_date=etime.getTime()-stime.getTime();
       if(d_date >= 1000) {
           d_date = 900
       }
            setTimeout(requestData, 1000 - d_date);
        },
        cache: false
    });
}

$(document).ready(function(){
    chart_cpu_usage = new Highcharts.Chart({
        chart: {
            renderTo: 'cpu_usage', //图表放置的容器，DIV
            defaultSeriesType: 'spline', //图表类型为曲线图
            backgroundColor:'#DFFDFD',
            events: {
                load: requestData
                       }
              },
        title: {
            text: 'CPU Usage'      //图表标题
                      },
        xAxis: { //设置X轴
            title: { text: ''   },
            type: 'datetime',       //X轴为日期时间类型
            tickPixelInterval: 150  //X轴标签间隔
                      },
        yAxis: { //设置Y轴
            title: { text: 'CPU Usage'   },
            labels: {
			   	  formatter: function() {
				    		return this.value +'%';
				              }
                                 },
            max: 100, //Y轴最大值
            min: 0  //Y轴最小值
                      },
        tooltip: {//当鼠标悬置数据点时的提示框
            formatter: function() { //格式化提示信息
                return Highcharts.dateFormat('%H:%M:%S', this.x) +' '+
                Highcharts.numberFormat(this.y, 2)+'%';
                                }
                      },
        legend: {
            enabled: false  //设置图例不可见
                      },
        exporting: {
            enabled: false  //设置导出按钮不可用
                      },

        series: [{
            marker: {
                enabled: false
            },
            data: (function() { //设置默认数据，
                var data = [],
                time = (new Date()).getTime() + 8*3600*1000,
                i;

                for (i = -19; i <= 0; i++) {
                    data.push({
                        x: time + i * 1000,
                        y: 0
                                                      });
                                           }
                return data;
                                 })()
                       }]
           });
});

$(document).ready(function(){
    chart_cpu_termperature = new Highcharts.Chart({
        chart: {
            renderTo: 'cpu_temperature', //图表放置的容器，DIV
            defaultSeriesType: 'spline', //图表类型为曲线图
            backgroundColor:'#DFFDFD',
            events: {
                load: requestData
                               }
                      },
        title: {
            text: 'CPU Temperature'      //图表标题
                      },
        xAxis: { //设置X轴
            title: { text: ''   },
            type: 'datetime',       //X轴为日期时间类型
            tickPixelInterval: 150  //X轴标签间隔
                      },
        yAxis: { //设置Y轴
            title: { text: 'CPU Temperature'   },
            labels: {
			   	  formatter: function() {
				    		return this.value +'℃';
				              }
                                 },
            max: 120, //Y轴最大值
            min: 0  //Y轴最小值
                      },
        tooltip: {//当鼠标悬置数据点时的提示框
            formatter: function() { //格式化提示信息
                return Highcharts.dateFormat('%H:%M:%S', this.x) +' '+
                Highcharts.numberFormat(this.y, 2) + '℃';
                                }
                      },
        legend: {
            enabled: false  //设置图例不可见
                      },
        exporting: {
            enabled: false  //设置导出按钮不可用
                      },

        series: [{
            marker: {
                enabled: false
            },
            data: (function() { //设置默认数据，
                var data = [],
                time = (new Date()).getTime() + 8*3600*1000,
                i;

                for (i = -19; i <= 0; i++) {
                    data.push({
                        x: time + i * 1000,
                        y: 0
                     });
                }
                return data;
            })()
        }]
           });
});

$(document).ready(function(){
    chart_cpu_current_freq = new Highcharts.Chart({
        chart: {
            renderTo: 'cpu_current_freq', //图表放置的容器，DIV
            defaultSeriesType: 'spline', //图表类型为曲线图
            backgroundColor:'#DFFDFD',
            events: {
                load: requestData
                       }
              },
        title: {
            text: 'CPU Frequency'      //图表标题
                      },
        xAxis: { //设置X轴
            title: { text: ''   },
            type: 'datetime',       //X轴为日期时间类型
            tickPixelInterval: 150  //X轴标签间隔
                      },
        yAxis: { //设置Y轴
            title: { text: 'CPU Frequency'   },
            labels: {
			   	  formatter: function() {
				    		return this.value +' GHz';
				              }
                                 },
            max: 3, //Y轴最大值
            min: 0  //Y轴最小值
                      },
        tooltip: {//当鼠标悬置数据点时的提示框
            formatter: function() { //格式化提示信息
                return Highcharts.dateFormat('%H:%M:%S', this.x) +' '+
                Highcharts.numberFormat(this.y, 2)+' GHz';
                                }
                      },
        legend: {
            enabled: false  //设置图例不可见
                      },
        exporting: {
            enabled: false  //设置导出按钮不可用
                      },

        series: [{
            marker: {
                enabled: false
            },
            data: (function() { //设置默认数据，
                var data = [],
                time = (new Date()).getTime() + 8*3600*1000,
                i;

                for (i = -19; i <= 0; i++) {
                    data.push({
                        x: time + i * 1000,
                        y: 0
                                                      });
                                           }
                return data;
                                 })()
                       }]
           });
});
