function follow(username) {
    $.post('/follow',{
        user:username
    }).done(function(response){
        $('#follower_num em').text(response['follower_num'])
        $('#state_alert').show().text(response['state'])
        $('.follow_click').hide()
        $('.unfollow_click').show()
    });
};

function unfollow(username) {
    $.post('/unfollow',{
        user:username
    }).done(function(response){
        $('#follower_num em').text(response['follower_num'])
        $('#state_alert').show().text(response['state'])
        $('.unfollow_click').hide()
        $('.follow_click').show()

    });
};

function translate(sourceElem,destElem,sourceLang,destLang) {
    // $(destElem).html('<img src="{{ url_for('static', filename='loading.gif') }}">');
    $.post('/translate',{
        text:$(sourceElem).text(),
        source_language:sourceLang,
        dest_language:destLang
    }).done(function (response) {
        $(destElem).text(response['text'])
    }).fail(function () {
        $(destElem).text("{{ _('Error: Could not contact server.') }}");
    });
};

function before_star(id) {
    $.post('/star',{
        post_id:id
    }).done(function (response) {
        $('#before_star'+id).hide()
        $('#after_star'+id).show()
        $('#stared_num').text(response['stared_num'])
    })
};

function after_star(id) {
    $.post('/unstar',{
        post_id:id
    }).done(function (response) {
        $('#after_star'+id).hide()
        $('#before_star'+id).show()
        $('#stared_num').text(response['stared_num'])
    })
};

function before_zan(id) {
    $.post('/thumb_up',{
        post_id:id
    }).done(function (response) {
        $('#before_zan'+id).hide()
        $('#after_zan'+id).show()
        $('#after_zan'+id+ ' span').text(response['thumbers_num'])
        $('#thumbed_num').text(response['thumbed_num'])
    })
};

function after_zan(id) {
    $.post('/thumb_down',{
        post_id:id
    }).done(function (response) {
        $('#after_zan'+id).hide()
        $('#before_zan'+id).show()
        $('#before_zan'+id+ ' span').text(response['thumbers_num'])
        $('#thumbed_num').text(response['thumbed_num'])
    })
};

// function get_comment(id) {
//     $.post('/get_comment',{
//         id:id
//     }).done(function (response) {
//         $('#commentForm'+id).toggle()
//     })
// };

function toggle_comment(id) {
    $('#commentForm'+id).toggle();
    $('#commentList'+id).toggle();
}

function post_comment(id) {
    var c=$("#commentData"+id+' '+"textarea").val();
    $.post('/post_comment',{
        id:id,
        comment:c
    }).done(function (response) {
        var a=$("<tr><td width='70px'><img class='img-thumbnail avatarURL' src='' /></td><td><span class='comment_username'></span>（刚刚）说:<span class='body'></span><br></td></tr>")
        $('.avatarURL',a).attr('src',response['avatarURL'])
        $('.comment_username',a).text(response['comment_username'])
        $('.body',a).text(c)

        $('#commentList'+id+' '+'table').prepend(a)
        $("#commentData"+id+' '+"textarea").val("");
        $('#comment'+id+ ' span').text(response['comment_num'])
    })  
};