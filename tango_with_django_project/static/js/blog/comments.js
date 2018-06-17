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
                console.log(comment_layer)
                comment_layer.text(comment_layer.text()-1);
           });
       }
       else{
           $(which).parents(".article_comment").nextAll(".article_comment").each(function(){
                var comment_layer=$(this).find(".comment_layer");
                console.log(comment_layer.text());
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
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
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
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
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
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
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
        //点赞用户评论,通过on关键字动态添加元素绑定事件
        $("body").on("click", ".like_comment", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/like_comment/'+$(this).attr("comment_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
                if(response == 'like_comment'){
                    $(parent_this).children("span[name='like_hand']").css('color','#ee9f49');
                    var like_count=$(parent_this).children(".like_count");
                    like_count.text(parseInt(like_count.text())+1);
                    like_count.addClass("gold-color");
                }
              });
        });

        //点赞文章,通过on关键字动态添加元素绑定事件
        $("body").on("click", ".like_article", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/like_article/'+$(this).attr("article_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
                if(response == 'like_article'){
                    $(parent_this).children("span[name='like_hand']").css('color','#ee9f49');
                    var like_article_count=$(parent_this).children(".like_article_count");
                    like_article_count.text(parseInt(like_article_count.text())+1);
                    like_article_count.addClass("gold-color");
                }
              });
        });

        //点赞用户,通过on关键字动态添加元素绑定事件(暂时没有使用)
        $("body").on("click", ".like_user", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/like_user/'+$(this).attr("user_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
                if(response == 'like_user'){
                    $(parent_this).children("span[name='like_hand']").css('color','red');
                    var like_user_count=$(parent_this).children(".like_user_count");
                    like_user_count.text(parseInt(like_user_count.text())+1);
                }
              });
        });

        //关注或取消关注,通过on关键字动态添加元素绑定事件
        $("body").on("click", ".follow_or_unfollow", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/user_follow/'+$(this).attr("user_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == '403'){
                    window.location.replace('/blog/login/');
                }
                if(response == 'follow'){
                    $(parent_this).removeClass('btn-success');
                    $(parent_this).addClass('btn-danger');
                    $(parent_this).children("span[name='follow_icon']").removeClass('glyphicon-plus');
                    $(parent_this).children("span[name='follow_icon']").addClass('glyphicon-ok');
                    $(parent_this).children("span[name='follow_word']").text('已关注');
                }
                if(response == 'unfollow'){
                    $(parent_this).removeClass('btn-danger');
                    $(parent_this).addClass('btn-success');
                    $(parent_this).children("span[name='follow_icon']").removeClass('glyphicon-ok');
                    $(parent_this).children("span[name='follow_icon']").addClass('glyphicon-plus');
                    $(parent_this).children("span[name='follow_word']").text('关注');
                }
              });
        });

        //收藏或取消收藏,通过on关键字动态添加元素绑定事件
        $("body").on("click", ".favorite_or_unfavorite", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/user_favorite/'+$(this).attr("article_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            console.log(post_url)
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == '403'){
                    //window.location.replace('/blog/login/');
                }
                if(response == 'favorite'){
                    $(parent_this).addClass('gold-color');
                    $(parent_this).removeClass('glyphicon-star-empty');
                    $(parent_this).addClass('glyphicon-star');
                }
                if(response == 'unfavorite'){
                    $(parent_this).removeClass('gold-color');
                    $(parent_this).removeClass('glyphicon-star');
                    $(parent_this).addClass('glyphicon-star-empty');
                }
              });
        });
        //获取关注的用户,通过on关键字动态添加元素绑定事件(暂时没有使用)
        $("body").on("click", "div[name='show_followees']", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/user_followees/'+$(this).attr("user_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == 'noexist'){
                    window.location.replace('/blog/login/');
                }
                else{
                    $("div[name='user_info_show_zone']").html(response);
                }
              });
        });

        //获取用户粉丝,通过on关键字动态添加元素绑定事件(暂时没有使用)
        $("body").on("click", "div[name='show_followers']", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/user_followers/'+$(this).attr("user_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
                if(response == 'noexist'){
                    window.location.replace('/blog/login/');
                }
                else{
                    $("div[name='user_info_show_zone']").html(response);
                }
              });
        });


        //获取用户粉丝,通过on关键字动态添加元素绑定事件(暂时没有使用)
        $("body").on("click", "div[name='show_articles']", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/user_articles/'+$(this).attr("user_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
               $("div[name='user_info_show_zone']").html(response);
              });
        });

        //获取用户收藏,通过on关键字动态添加元素绑定事件(暂时没有使用)
        $("body").on("click", "div[name='show_favorites']", function(event) {
            //阻止默认form提交
            //event.preventDefault();
            //获取form的action参数值
            var post_url = '/blog/user_favorites/'+$(this).attr("user_id");
            //获取form的method参数值
            var request_method = 'get';
            //把当前的this赋值给parent_this
            var parent_this=this
            //ajax请求
            $.ajax({
                url : post_url,
                type: request_method,
            }).done(function(response){
               $("div[name='user_info_show_zone']").html(response);
              });
        });


        //显示用户的全名,通过on关键字动态添加元素绑定事件(暂时没有使用)
        $("body").on("mouseenter", ".follower_name", function(event) {
            $(this).children(".cut_name_dot").hide();
            $(this).children(".get_name_tail").show();
        });
        $("body").on("mouseleave", ".follower_name", function(event) {
            $(this).children(".cut_name_dot").show();
            $(this).children(".get_name_tail").hide();
        });
});