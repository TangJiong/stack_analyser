/**
 * Created by tangjiong on 15-11-11.
 */

$(function(){

    var period = 'day';
    var top = 10;

    var ajax_toprank = function(_period, _top){
        $.ajax({
            type: "POST",
            url: "/toprank",
            data: {
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
                init_rank_charts("#toprank", responseData.date, responseData.taglist);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){

            }

        });
    };

    var init_rank_charts = function(chart_dom, date, taglist){

        var tagArray = [];
        var countArray = [];

        for(var i=0; i<taglist.length; i++){
            tagArray.push("No." + (i+1) +" "+ taglist[i].tag_name);
            countArray.push(taglist[i].tag_count);
        }

        $(chart_dom).highcharts({
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Top ' + top + ' Topics'
            },
            subtitle: {
                text: date
            },
            xAxis: {
                categories: tagArray
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Questions',
                    align: 'high'
                },
                labels: {
                    overflow: 'justify'
                }
            },
            tooltip: {
                valueSuffix: null
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'Total',
                data: countArray
            }]
        });
    };

    ajax_toprank(period, top);

    $("ul.nav-tabs li").click(function(){
        $("ul.nav-tabs li.active").removeClass('active');
        $(this).addClass('active');
        period = $(this).text().toLowerCase();
        ajax_toprank(period, top);
    });

    $("ul.dropdown-menu li").click(function(){
        top = $(this).find("span").text();
        $("a.dropdown-toggle").find("span.select-top").text(top);
        if(top == 5){
            $("#toprank").width("90%").height(400);
        }else if(top == 10){
            $("#toprank").width("90%").height(600);
        }else if(top == 15){
            $("#toprank").width("90%").height(800);
        }else if(top == 20){
            $("#toprank").width("90%").height(1200);
        }
        ajax_toprank(period, top);
    });

});

