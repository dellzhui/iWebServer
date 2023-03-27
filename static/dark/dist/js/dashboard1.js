$(function () {
    "use strict";
    //This is for the Notification top right
    // $.toast({
    //         heading: 'Welcome A to Elite admin'
    //         , text: 'Use the predefined ones, or specify a custom position object.'
    //         , position: 'top-right'
    //         , loaderBg: '#ff6849'
    //         , icon: 'info'
    //         , hideAfter: 3500
    //         , stack: 6
    //     })

    jQuery("#visitfromworld").vectorMap({
            map: "world_mill_en"
            , backgroundColor: "transparent"
            , borderColor: "#000"
            , borderOpacity: .9
            , borderWidth: 1
            , zoomOnScroll: !1
            , color: "#ddd"
            , regionStyle: {
                initial: {
                    fill: "transparent"
                    , "stroke-width": 1
                    , stroke: "#a6b7bf"
                }
            }
            , markerStyle: {
                initial: {
                    r: 5
                    , fill: "#26c6da"
                    , "fill-opacity": 1
                    , stroke: "#fff"
                    , "stroke-width": 1
                    , "stroke-opacity": 1
                }
            }
            , enableZoom: !0
            , hoverColor: "#79e580"
            , markers: [{
                latLng: [39, 112]
                , name: "China : 9347"
                , style: {
                    fill: "#24d2b5"
                }
        }, {
                latLng: [-33, 151]
                , name: "Australia : 250"
                , style: {
                    fill: "#ff9040"
                }
        }, {
                latLng: [36.77, -119.41]
                , name: "USA : 250"
                , style: {
                    fill: "#20aee3"
                }
        }, {
                latLng: [55.37, -3.41]
                , name: "UK   : 250"
                , style: {
                    fill: "#6772e5"
                }
        }, {
                latLng: [25.2, 55.27]
                , name: "UAE : 250"
                , style: {
                    fill: "#24d2b5"
                }
        }]
            , hoverOpacity: null
            , normalizeFunction: "linear"
            , scaleColors: ["#fff", "#ccc"]
            , selectedColor: "#c9dfaf"
            , selectedRegions: []
            , showTooltip: !0
            , onRegionClick: function (e, o, l) {
                var t = 'You clicked "' + l + '" which has the code: ' + o.toUpperCase();
                alert(t)
            }
        })

        jQuery("#visitfromcn").vectorMap({
            map: "cn_mill"
            , backgroundColor: "transparent"
            , borderColor: "#000"
            , borderOpacity: .9
            , borderWidth: 1
            , zoomOnScroll: !1
            , color: "#ddd"
            , regionStyle: {
                initial: {
                    fill: "transparent"
                    , "stroke-width": 1
                    , stroke: "#a6b7bf"
                }
            }
            , markerStyle: {
                initial: {
                    r: 5
                    , fill: "#26c6da"
                    , "fill-opacity": 1
                    , stroke: "#fff"
                    , "stroke-width": 1
                    , "stroke-opacity": 1
                }
            }
            , enableZoom: !0
            , hoverColor: "#79e580"
            , markers: [{
                latLng: [39, 112]
                , name: "China : 9347"
                , style: {
                    fill: "#24d2b5"
                }
        }, {
                latLng: [-33, 151]
                , name: "Australia : 250"
                , style: {
                    fill: "#ff9040"
                }
        }, {
                latLng: [36.77, -119.41]
                , name: "USA : 250"
                , style: {
                    fill: "#20aee3"
                }
        }, {
                latLng: [55.37, -3.41]
                , name: "UK   : 250"
                , style: {
                    fill: "#6772e5"
                }
        }, {
                latLng: [25.2, 55.27]
                , name: "UAE : 250"
                , style: {
                    fill: "#24d2b5"
                }
        }]
            , hoverOpacity: null
            , normalizeFunction: "linear"
            , scaleColors: ["#fff", "#ccc"]
            , selectedColor: "#c9dfaf"
            , selectedRegions: []
            , showTooltip: !0
            , onRegionClick: function (e, o, l) {
                var t = 'You clicked "' + l + '" which has the code: ' + o.toUpperCase();
                alert(t)
            }
        })

        var data = []
        , totalPoints = 100;

    function getRandomData() {
        if (data.length > 0) data = data.slice(1);
        // Do a random walk
        while (data.length < totalPoints) {
            var prev = data.length > 0 ? data[data.length - 1] : 50
                , y = prev + Math.random() * 10 - 5;
            if (y < 0) {
                y = 0;
            }
            else if (y > 100) {
                y = 100;
            }
            data.push(y);
        }
        // Zip the generated y values with the x values
        var res = [];
        for (var i = 0; i < data.length; ++i) {
            res.push([i, data[i]])
        }
        return res;
    }
    // Set up the control widget
    var updateInterval = 20;
    $("#updateInterval").val(updateInterval).change(function () {
        var v = $(this).val();
        if (v && !isNaN(+v)) {
            updateInterval = +v;
            if (updateInterval < 1) {
                updateInterval = 1;
            }
            else if (updateInterval > 2000) {
                updateInterval = 2000;
            }
            $(this).val("" + updateInterval);
        }
    });
    var plot = $.plot("#placeholder", [getRandomData()], {
        series: {
            shadowSize: 0 // Drawing is faster without shadows
        }
        , yaxis: {
            min: 0
            , max: 100
        }
        , xaxis: {
            show: false
        }
        , colors: ["#01c0c8"]
        , grid: {
            color: "#AFAFAF"
            , hoverable: true
            , borderWidth: 0
            , backgroundColor: 'transparent'
        }
        , tooltip: true
        , resize: true
        , tooltipOpts: {
            content: "Y: %y"
            , defaultTheme: false
        }
    });

    function update() {
        plot.setData([getRandomData()]);
        // Since the axes don't change, we don't need to call plot.setupGrid()
        plot.draw();
        setTimeout(update, updateInterval);
    }
    update();

    $("body").trigger("resize");
    //This is for the perfect scroll

    $('.slimscrollcountry').perfectScrollbar();


        // Dashboard 1 Morris-chart
    Morris.Area({
        element: 'morris-area-chart'
        , data: [{
                period: '2010'
                , info: 50
                , error: 80
                , warning: 20
        }, {
                period: '2011'
                , info: 130
                , error: 100
                , warning: 80
        }, {
                period: '2012'
                , info: 80
                , error: 60
                , warning: 70
        }, {
                period: '2013'
                , info: 70
                , error: 200
                , warning: 140
        }, {
                period: '2014'
                , info: 180
                , error: 150
                , warning: 140
        }, {
                period: '2015'
                , info: 105
                , error: 100
                , warning: 80
        }
            , {
                period: '2016'
                , info: 250
                , error: 150
                , warning: 200
        }
            /*, {
                period: '2017'
                , info: 250
                , error: 150
                , warning: 200
        }
            , {
                period: '2018'
                , info: 250
                , error: 150
                , warning: 200
        }
            , {
                period: '2019'
                , info: 250
                , error: 150
                , warning: 200
        }*/]
        , xkey: 'period'
        , ykeys: ['info', 'error', 'warning']
        , labels: ['Info', 'Error', 'Warning']
        , pointSize: 3
        , fillOpacity: 0
        , pointStrokeColors: ['#00bfc7', '#fb9678', '#9675ce']
        , behaveLikeLine: true
        , gridLineColor: 'rgba(255, 255, 255, 0.1)'
        , lineWidth: 3
        , hideHover: 'auto'
        , lineColors: ['#00bfc7', '#fb9678', '#9675ce']
        , resize: true
    });
    Morris.Area({
        element: 'morris-area-chart2'
        , data: [{
                period: '2010'
                , SiteA: 0
                , SiteB: 0
        , }, {
                period: '2011'
                , SiteA: 130
                , SiteB: 100
        , }, {
                period: '2012'
                , SiteA: 80
                , SiteB: 60
        , }, {
                period: '2013'
                , SiteA: 70
                , SiteB: 200
        , }, {
                period: '2014'
                , SiteA: 180
                , SiteB: 150
        , }, {
                period: '2015'
                , SiteA: 105
                , SiteB: 90
        , }
            , {
                period: '2016'
                , SiteA: 250
                , SiteB: 150
        , }]
        , xkey: 'period'
        , ykeys: ['SiteA', 'SiteB']
        , labels: ['Site A', 'Site B']
        , pointSize: 0
        , fillOpacity: 0.4
        , pointStrokeColors: ['#b4becb', '#01c0c8']
        , behaveLikeLine: true
        , gridLineColor: 'rgba(255, 255, 255, 0.1)'
        , lineWidth: 0
        , smooth: false
        , hideHover: 'auto'
        , lineColors: ['#b4becb', '#01c0c8']
        , resize: true
    });
});    
    // sparkline
    var sparklineLogin = function() { 
        $('#sales1').sparkline([20, 40, 30], {
            type: 'pie',
            height: '90',
            resize: true,
            sliceColors: ['#01c0c8', '#7d5ab6', '#ffffff']
        });
        $('#sales2').sparkline([20, 40, 30], {
            type: 'pie',
            height: '90',
            resize: true,
            sliceColors: ['#01c0c8', '#7d5ab6', '#ffffff']
        });
        $('#sales3').sparkline([20, 40, 30], {
            type: 'pie',
            height: '90',
            resize: true,
            sliceColors: ['#01c0c8', '#7d5ab6', '#ffffff']
        });
        $('#sales4').sparkline([20, 40, 30], {
            type: 'pie',
            height: '90',
            resize: true,
            sliceColors: ['#01c0c8', '#7d5ab6', '#ffffff']
        });
        $('#sales5').sparkline([20, 40, 30], {
            type: 'pie',
            height: '90',
            resize: true,
            sliceColors: ['#01c0c8', '#7d5ab6', '#ffffff']
        });
        $('#sparkline2dash').sparkline([6, 10, 9, 11, 9, 10, 12], {
            type: 'bar',
            height: '154',
            barWidth: '4',
            resize: true,
            barSpacing: '10',
            barColor: '#25a6f7'
        });
        $('#sparklinedash').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar'
            , height: '30'
            , barWidth: '4'
            , resize: true
            , barSpacing: '5'
            , barColor: '#4caf50'
        });
        $('#sparklinedash2').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar'
            , height: '30'
            , barWidth: '4'
            , resize: true
            , barSpacing: '5'
            , barColor: '#9675ce'
        });
        $('#sparklinedash3').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar'
            , height: '30'
            , barWidth: '4'
            , resize: true
            , barSpacing: '5'
            , barColor: '#03a9f3'
        });
        $('#sparklinedash4').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar'
            , height: '30'
            , barWidth: '4'
            , resize: true
            , barSpacing: '5'
            , barColor: '#f96262'
        });
        $('#sparklinedash5').sparkline([0, 5, 6, 10, 9, 12, 4, 9], {
            type: 'bar'
            , height: '30'
            , barWidth: '4'
            , resize: true
            , barSpacing: '5'
            , barColor: '#01777c'
        });
    };
    var sparkResize;
 
        $(window).resize(function(e) {
            clearTimeout(sparkResize);
            sparkResize = setTimeout(sparklineLogin, 500);
        });
        sparklineLogin();
