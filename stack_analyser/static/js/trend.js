/**
 * Created by tangjiong on 15-11-24.
 */
$(function(){

    var recent = 7;
    var period = 'day';
    var top = 3;

    var ajax_toptrend = function(_recent, _period, _top){
        $.ajax({
            type: "POST",
            url: "/toptrend",
            data: {
                "recent": _recent,
                "period": _period,
                "top": _top
            },
            dataType: "json",
            complete: function(XMLHttpRequest, textStatus){
                console.log(textStatus);
            },
            success: function(data, textStatus){
                var responseData = eval(data);
                console.log(responseData);
                init_trend_charts("#toptrend", responseData);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){

            }

        });
    };

    var init_trend_charts = function(chart_dom, data){

        var date = data.date;
        var datelist = data.datelist;
        var taglist = data.taglist;
        var dataArray = [];

        for(var i=0; i<taglist.length; i++){
            dataArray.push({
                "name": taglist[i].tag_name,
                "data": taglist[i].count_array
            });
        }

        $(chart_dom).highcharts({
            title: {
                text: 'Trend of Top ' + top + ' Topics',
                x: -20 //center
            },
            subtitle: {
                text: date,
                x: -20
            },
            xAxis: {
                categories: datelist
            },
            yAxis: {
                title: {
                    text: 'Questions'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: null
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                borderWidth: 0
            },
            series: dataArray
        });
    };

    ajax_toptrend(recent, period, top);

    $("ul.nav-tabs li").click(function(){
        $("ul.nav-tabs li.active").removeClass('active');
        $(this).addClass('active');
        period = $(this).text().toLowerCase();
        ajax_toptrend(recent, period, top);
    });

    $("ul.select-recent li").click(function(){
        recent = $(this).find("span").text();
        $("#select_recent").find("span.select-recent").text(recent);
        ajax_toptrend(recent, period, top);
    });

    $("ul.select-top li").click(function(){
        top = $(this).find("span").text();
        $("#select_top").find("span.select-top").text(top);
        ajax_toptrend(recent, period, top);
    });



});