/**
 * Created by tangjiong on 15-12-12.
 */
$(function(){

    var recent = 7;
    var tagname = $('h1.page-header').text();

    var ajax_taginfo = function(_tagname, _recent){
        $.ajax({
            type: "POST",
            url: "/tag_info",
            data: {
                "recent": _recent,
                "tagname": _tagname
            },
            dataType: "json",
            complete: function(XMLHttpRequest, textStatus){

            },
            success: function(data, textStatus){
                var responseData = eval(data);
                init_trend_charts("#tagtrend", responseData);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){

            }

        });
    };

    var init_trend_charts = function(chart_dom, data){

        var date = data.date;
        var datelist = data.datelist;
        var dataArray = [];

        dataArray.push({
            "name": data.tagname,
            "data": data.count_array
        });

        $(chart_dom).highcharts({
            title: {
                text: 'How ' + data.tagname + ' changes with time',
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

    ajax_taginfo(tagname, recent);


    $("ul.select-recent li").click(function(){
        recent = $(this).find("span").text();
        $("#select_recent").find("span.select-recent").text(recent);
        ajax_taginfo(tagname, recent);
    });


});