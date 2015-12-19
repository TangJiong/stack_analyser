/**
 * Created by tangjiong on 15-11-24.
 */
/**
 * Created by tangjiong on 15-11-11.
 */

$(function(){

    var period = 'day';
    var top = 10;

    var ajax_topshares = function(_period, _top){
        $.ajax({
            type: "POST",
            url: "/topshares",
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
                init_shares_charts("#topshares", responseData.date, responseData.taglist);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){

            }

        });
    };

    var init_shares_charts = function(chart_dom, date, taglist){

        var data = [];

        for(var i=0; i<taglist.length; i++){

            var item = {};
            item.name = taglist[i].tag_name;
            item.y = taglist[i].tag_count;

            if(i == 0){
                item.sliced = true;
                item.selected = true;
            }

            data.push(item);
        }

        $(chart_dom).highcharts({
            chart: {
                plotBackgroundColor: null,
                plotBorderWidth: null,
                plotShadow: false,
                type: 'pie'
            },
            title: {
                text: 'Topic Shares (Top '+top+')'
            },
            subtitle: {
                text: date
            },
            tooltip: {
                pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
            },
            plotOptions: {
                pie: {
                    allowPointSelect: true,
                    cursor: 'pointer',
                    dataLabels: {
                        enabled: true,
                        format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                        style: {
                            color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                        }
                    },
                    showInLegend: true
                }
            },
            series: [{
                name: "shares",
                colorByPoint: true,
                data: data
            }]
        });
    };

    ajax_topshares(period, top);

    $("ul.nav-tabs li").click(function(){
        $("ul.nav-tabs li.active").removeClass('active');
        $(this).addClass('active');
        period = $(this).text().toLowerCase();
        ajax_topshares(period, top);
    });

    $("ul.dropdown-menu li").click(function(){
        top = $(this).find("span").text();
        $("a.dropdown-toggle").find("span.select-top").text(top);
        ajax_topshares(period, top);
    });

});

