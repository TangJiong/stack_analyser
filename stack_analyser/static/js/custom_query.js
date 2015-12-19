/**
 * Created by tangjiong on 15-12-10.
 */
$(function(){

    get_top_tags(10);


    $("#search-input").on('input', function(){
        var keyword = $(this).val();
        if(keyword == ''){
            $("#search-result").addClass("hidden");
            $("#hot-tags").show();
        }else{
            $("#search-result").removeClass("hidden");
            $("#hot-tags").hide();
            search_tag(keyword);
        }

    });

});

var get_top_tags = function(size){
    $.ajax({
        type: "POST",
        url: "/top_tags",
        data: {
            "size": size
        },
        dataType: "json",
        complete: function(XMLHttpRequest, textStatus){

        },
        success: function(data, textStatus){
            var taglist = eval(data);
            init_top_tags(taglist);

        },
        error: function(XMLHttpRequest, textStatus, errorThrown){

        }
    });
};

var search_tag = function(keyword){
    $.ajax({
        type: "POST",
        url: "/search",
        data: {
            "keyword": keyword
        },
        dataType: "json",
        complete: function(XMLHttpRequest, textStatus){

        },
        success: function(data, textStatus){
            var taglist = eval(data);
            init_search_result(taglist);

        },
        error: function(XMLHttpRequest, textStatus, errorThrown){

        }
    });
};

var init_top_tags = function(taglist){

    var column_size = 5;
    var row = parseInt(taglist.length / column_size + 1);

    for(var i=0; i<row ; i++){
        var tr = $("<tr>");
        for(var j=0; j<column_size; j++ ){
            if(i * column_size + j < taglist.length){
                var tag = taglist[i*column_size+j];
                var td = "<td><a href=\"/tag.html?tagname="+tag.tagname+"\">"+ tag.tagname +" <span class=\"badge\">"+ tag.questotal +"</span></a></td>";
                tr.append(td);
            }else{
                tr.append("<td></td>")
            }

        }
        $("#hot-tags").find("table").append(tr);
    }
};

var init_search_result = function(taglist){
    $("#search-result").find("ul.list-group").html("");
    for(var i = 0; i<taglist.length; i++){
        var tag = taglist[i];
        var li = "<li class=\"list-group-item\"><a href=\"/tag.html?tagname="+tag.tagname+"\"><span>"
            + tag.tagname + "</span>&nbsp;&nbsp;&nbsp;&nbsp;<span>"
            + tag.questotal + "</span></a></li>";
        $("#search-result").find("ul.list-group").append(li);
    }
};