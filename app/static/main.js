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

function follow(username) {
    $.post('/follow',{
        user:username
    }).done(function(response){
        $(#follower_num).text(response['follower_num'])
        $(#alert-info).text(response['state'])
    });
};

function unfollow(username) {
    $.post('/unfollow',{
        user:username
    }).done(function(response){
        $(#follower_num).text(response['follower_num'])
        $(#alert-info).text(response['state'])
    });
};