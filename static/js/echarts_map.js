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
var nodes = [];
var links = [];
var index = 0;
for(var item in paramObj) {
    var values = paramObj[item].split('_');
    if(item.startsWith('n_')) {
        console.log('' + item + ':' + paramObj[item]);
        var local_node = {};
        local_node.x = values[0];
        local_node.y = values[1];
        local_node.name = values[2];
        if(local_node.name.split(':').length === 6) {
            local_node.img = 'stb.png';
        } else {
            local_node.img = 'data-1547632915872-WZMUphq72.png';
        }
        nodes[index] = local_node;
        index++;
    }
}

index = 0;
for(var item in paramObj) {
    var values = paramObj[item].split('_');
    if(item.startsWith('l_')) {
        console.log('' + item + ':' + paramObj[item]);
        var local_link = {};
        local_link.source = nodes[values[0]-1].name;
        local_link.target = nodes[values[1]-1].name;
        local_link.name = '';
        links[index] = local_link;
        index++;
    }
}

// var nodes = [{
//         x: '5',
//         y: '5',
//         name: '服务器',
//         img: 'data-1547632686885-o5Rfi3tyk.png',
//         alarm: '产生告警了哦'
//     },
//     {
//         x: '3',
//         y: '0',
//         name: '存储设备1',
//         img: 'data-1547633192258-2EYYUDdcd.png'
//     },
//     {
//         x: '7',
//         y: '0',
//         name: '存储设备2',
//         img: 'data-1547633192258-2EYYUDdcd.png'
//     },
//     {
//         x: '9',
//         y: '0',
//         name: '存储设备3',
//         img: 'data-1547633192258-2EYYUDdcd.png'
//     },
//     {
//         x: '0',
//         y: '10',
//         name: '防火墙',
//         img: 'data-1547633094304-08Q_2YEvH.png'
//     },
//     {
//         x: '5',
//         y: '10',
//         name: '网络设备1',
//         img: 'data-1547632915872-WZMUphq72.png',
//         alarm: '产生告警了哦'
//     },
//     {
//         x: '12',
//         y: '12',
//         name: '网络设备2',
//         img: 'data-1547632915872-WZMUphq72.png'
//     }
// ]
// var links = [{
//         source: '存储设备2',
//         target: '存储设备1',
//         name: '数据传输'
//     }, {
//         source: '存储设备3',
//         target: '服务器',
//         name: '数据传输'
//     },{
//         source: '存储设备1',
//         target: '服务器',
//         name: '数据传输'
//     },
//     {
//         source: '服务器',
//         target: '防火墙',
//         name: '访问'
//     },
//     {
//         source: '防火墙',
//         target: '网络设备1',
//         name: '访问'
//     },
//     {
//         source: '网络设备1',
//         target: '网络设备2',
//         name: '访问'
//     }
// ]
var charts = {
    nodes: [],
    links: [],
    linesData: []
};
var dataMap = new Map();
for (var j = 0; j < nodes.length; j++) {
    var x = parseInt(nodes[j].x);
    var y = parseInt(nodes[j].y);
    var node = {
        name: nodes[j].name,
        value: [x, y],
        symbolSize: 50,
        alarm: nodes[j].alarm,
        symbol: 'image:///static/img/echarts/' + nodes[j].img,
        itemStyle: {
            normal: {
                color: '#12b5d0',
            }
        }
    };
    dataMap.set(nodes[j].name, [x, y]);
    charts.nodes.push(node)
}
for (var i = 0; i < links.length; i++) {
    var link = {
        source: links[i].source,
        target: links[i].target,
        label: {
            normal: {
                show: true,
                formatter: links[i].name
            }
        },
        lineStyle: {
            normal: {
                color: '#00FFFF'
            }
        }
    };
    charts.links.push(link);
    // 组装动态移动的效果数据
    var lines = [{
        coord: dataMap.get(links[i].source)
    }, {
        coord: dataMap.get(links[i].target)
    }];
    charts.linesData.push(lines)
}
option = {
    title: {
        text: paramObj['desc'],
        textStyle: {
            fontWeight: 'normal',
            color: "#00FFFF",
        }
    },
    backgroundColor: "#1b2735",
    xAxis: {
        show: false,
        type: 'value'
    },
    yAxis: {
        show: false,
        type: 'value'
    },
    series: [{
        type: 'graph',
        layout: 'none',
        coordinateSystem: 'cartesian2d',
        symbolSize: 50,
        label: {
            normal: {
                show: true,
                position: 'bottom',
                color: '#00FFFF'
            }
        },
        lineStyle: {
            normal: {
                width: 2,
                shadowColor: 'none'
            }
        },
        edgeSymbolSize: 8,
        data: charts.nodes,
        links: charts.links,
        itemStyle: {
            normal: {
                label: {
                    show: true,
                    formatter: function(item) {
                        return item.data.name
                    }
                }
            }
        }
    }, {
        name: 'A',
        type: 'lines',
        coordinateSystem: 'cartesian2d',
        effect: {
            show: true,
            trailLength: 0,
            symbol: 'arrow',
            color: '#00FFFF',
            symbolSize: 8
        },
        data: charts.linesData
    }]
};
// 用于告警的动态效果
setInterval(() => {
    var dataI = [];
    for (var n = 0; n < nodes.length; n++) {
        var alarm = nodes[n].alarm;
        if (alarm !== null && alarm !== '' && alarm !== undefined) {
            option.series[0].data[n].symbolSize = 60;
            option.series[0].data[n].label = {
                normal: {
                    color: '#DC143C'
                }
            };
            option.series[0].itemStyle.normal.label.formatter = function(item) {
                if (item.data.alarm !== undefined) {
                    return item.data.name + '\n[ ' + item.data.alarm + ' ]'
                } else {
                    return item.data.name
                }
            };
            dataI.push(n)
        }
    }
    myChart.setOption(option);
    setTimeout(() => {
        for (var m = 0; m < dataI.length; m++) {
            option.series[0].data[dataI[m]].symbolSize = 50;
            option.series[0].data[dataI[m]].label = {
                normal: {
                    color: '#00FFFF'
                }
            };
            option.series[0].itemStyle.normal.label.formatter = function(item) {
                return item.data.name
            }
        }
        myChart.setOption(option)
    }, 500)
}, 1000);

var mainDom = document.getElementById('rd_mtr_main');
var myChart = echarts.init(mainDom);
myChart.on('click', function (params) {
    console.log(params);
});
// 使用刚指定的配置项和数据显示图表。
myChart.setOption(option);
