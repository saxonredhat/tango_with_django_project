function display_form(which){
     //隐藏其他的用户评论form
     $("form[name='user_comment_form']").attr("style","display:none;");
     //隐藏其他的文章评论form
     $("form[name='article_comment_form']").attr("style","display:none;");
     //显示当前元素下面的form
     $(which).nextAll("form").attr("style","inline");
}
function hidden_form(which){
     //隐藏当前父form
     $(which).parents("form").attr("style","display:none;");
}
function delete_article_comment(which){
    var comment_id=$(which).attr("id");
    var order=$("#comment_order").attr("value");
    $.get('/blog/comment_delete/'+comment_id, function(data){
       //隐藏删除的评论
       $(which).parents(".article_comment").hide();
       //更新评论数
       var comment_counts=$("#comment_counts");
       comment_counts.text(parseInt(comment_counts.text())-1);
       //更新评论的楼层号
       if(order=='desc'){
            $(which).parents(".article_comment").prevAll(".article_comment").each(function(){
                var comment_layer=$(this).find(".comment_layer");
                comment_layer.text(comment_layer.text()-1);
           });
       }
       else{
           $(which).parents(".article_comment").nextAll(".article_comment").each(function(){
                var comment_layer=$(this).find(".comment_layer");
                comment_layer.text(comment_layer.text()-1);
           });
       };
   });
}
function delete_user_comment(which){
    var comment_id=$(which).attr("id");
    $.get('/blog/comment_delete/'+comment_id, function(data){
       //删除用户的评论
       $(which).parents(".user_comment").hide();
       //更新用户评论数
       var comment_count=$(which).parents(".article_comment").find(".replay_counts");
       comment_count.text(comment_count.text()-1);
   });
}

//获取按时间正序的评论
function comment_list(article_id,order){
    var article_id=article_id;
    $.get('/blog/comment_list/'+article_id+'?order='+order, function(data){
       $("#comment_list").html('');
       $("#comment_list").html(data);
   });
}

//获取按时间倒序的评论

$(document).ready(function(){
        //文章评论表单
        $(".article_form").submit(function(event){
            //阻止默认form提交
            event.preventDefault();
            //获取form的action参数值
            var post_url = $(this).attr("action");
            //获取form的method参数值
            var request_method = $(this).attr("method");
            //序列化form的参数
            var form_data = $(this).serialize();
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
                data : form_data
            }).done(function(response){
                //把响应的response放到id为comment_all节点内最后
                var order=$("#comment_order").attr("value");
                if(order=='desc'){
                    $("#comment_order").prepend(response);
                }else{
                    $("#comment_order").append(response);
                }

                //清空当前的form
                var comment_counts=$("#comment_counts");
                $(parent_this)[0].reset();
                comment_counts.text(parseInt(comment_counts.text())+1)

              });
        });
        //回复用户评论表单,通过on关键字动态添加元素绑定事件
        $("body").on("submit", ".article_comment_form", function(event) {
           //阻止默认form提交
            event.preventDefault();
            //获取form的action参数值
            var post_url = $(this).attr("action");
            //获取form的method参数值
            var request_method = $(this).attr("method");
            //序列化form的参数
            var form_data = $(this).serialize();
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
                data : form_data
            }).done(function(response){
                //把响应的response放到子节点的前面
                $(parent_this).after(response);
                //alert(response);
                //获取当前评论的回复数
                var comment_count=$(parent_this).parents(".article_comment").find(".replay_counts");
                //把当前评论的回复数+1
                comment_count.text(parseInt(comment_count.text())+1);
                //清空当前的form
                $(parent_this)[0].reset();
                //隐藏当前form
                $(parent_this).hide();
              });
        });
        //回复用户回复表单,通过on关键字动态添加元素绑定事件
        $("body").on("submit", ".user_comment_form", function(event) {
            //阻止默认form提交
            event.preventDefault();
            //获取form的action参数值
            var post_url = $(this).attr("action");
            //获取form的method参数值
            var request_method = $(this).attr("method");
            //序列化form的参数
            var form_data = $(this).serialize();
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
                data : form_data
            }).done(function(response){
                //把响应的response放到子节点的前面
                $(parent_this).parents(".comment_user_parent").children('.user_comment').eq(0).before(response);
                //获取当前评论的回复数
                var comment_count=$(parent_this).parents(".article_comment").find(".replay_counts");
                //把当前评论的回复数+1
                comment_count.text(parseInt(comment_count.text())+1);
                //清空当前的form
                $(parent_this)[0].reset();
                //隐藏当前form
                $(parent_this).hide();
              });
        });
});