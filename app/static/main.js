function follow(username) {
    $.post('/follow',{
        user:username
    }).done(function(response){
        $('#follower_num').text(response['follower_num'])
        $('#state_alert').show().text(response['state'])
        $('.follow_click').hide()
        $('.unfollow_click').show()
    });
};

function unfollow(username) {
    $.post('/unfollow',{
        user:username
    }).done(function(response){
        $('#follower_num').text(response['follower_num'])
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

function before_zan(id) {
    $.post('/thumb_up',{
        post_id:id
    }).done(function (response) {
        $('#before_zan'+id).hide()
        $('#after_zan'+id).show()
        $('#after_zan'+id+ ' span').text(response['thumbers_num'])
    }).fail(function (response,status) {
        alert(status)
    })
}

function after_zan(id) {
    $.post('/thumb_down',{
        post_id:id
    }).done(function (response) {
        $('#after_zan'+id).hide()
        $('#before_zan'+id).show()
        $('#before_zan'+'id'+ ' span').text(response['thumbers_num'])
        
    })
}