/**
 * Created by tangjiong on 15-12-10.
 */
$(function(){

    $("#taginput").on('input', function(){
        var keyword = $(this).val();
        if(keyword == ''){
            $("#search-result").addClass("hidden");
        }else{
            $("#search-result").removeClass("hidden");
            search_tag(keyword);
        }

    });

    $("ul.list-group").on('click', 'li', function(){
        var tag = $(this).find('span.tagname').text();
        $("#taginput").val('');
        $("#search-result").addClass("hidden");
        $("#tag-area").removeClass('hidden').find('.taglist').append('<a class="label label-info">'+tag+'</a>');
    });

    $("div.taglist").on('click', 'a', function(){
        $(this).remove();
    });

    $('#startdatepicker').datetimepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        minView: 2,
        todayBtn: "linked",
        todayHighlight: true
    });

    $('#enddatepicker').datetimepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        minView: 2,
        todayBtn: "linked",
        todayHighlight: true
    });

    $('button.submit').click(function(){
        var taglist = [];
        $("div.taglist a").each(function(){
            taglist.push($(this).text());
        });
        var startDate = $("#startdatepicker").val();
        var endDate = $("#enddatepicker").val();
        var data = {
                'taglist': JSON.stringify(taglist),
                'startDate': startDate,
                'endDate': endDate
            };
        if($(this).hasClass('shares')){
            ajax_custom_shares(data);
        }else{
            ajax_custom_trend(data);
        }
        $("div.alert").remove();
    });

});

var search_tag = function(keyword){
    $.ajax({
        type: "POST",
        url: "/search",
        data: {
            "keyword": keyword
        },
        dataType: "json",
        complete: function(XMLHttpRequest, textStatus){
            console.log(textStatus);
        },
        success: function(data, textStatus){
            var taglist = eval(data);
            init_search_result(taglist);

        },
        error: function(XMLHttpRequest, textStatus, errorThrown){

        }
    });
};

var init_search_result = function(taglist){
    $("#search-result").find("ul.list-group").html("");
    for(var i = 0; i<taglist.length; i++){
        var tag = taglist[i];
        var li = '<li class="list-group-item"><a href="javascript:void"><span class="tagname">'
            + tag.tagname + '</span>&nbsp;&nbsp;&nbsp;&nbsp;'
            + ' <span class="glyphicon glyphicon-plus"></span></a></li>';
        $("#search-result").find("ul.list-group").append(li);
    }
};


var ajax_custom_shares = function(data){
    $.ajax({
        type: 'POST',
        url: '/custom_shares',
        data: data,
        traditional: true,
        dataType: 'json',
        complete: function(XMLHttpRequest, textStatus){
            console.log(textStatus);
        },
        success: function(data, textStatus){
            var responseData = eval(data);
            init_shares_charts("#custom_shares", responseData.date, responseData.taglist);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown){

        }
    });
};

var ajax_custom_trend = function(data){
    $.ajax({
        type: 'POST',
        url: '/custom_trend',
        data: data,
        traditional: true,
        dataType: 'json',
        complete: function(XMLHttpRequest, textStatus){
            console.log(textStatus);
        },
        success: function(data, textStatus){
            var responseData = eval(data);
            init_trend_charts("#custom_trend", responseData);
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
            text: 'Shares of Custom Chosen Topics'
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
            text: 'Trend of Custom Chosen Topics',
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
