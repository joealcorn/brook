var interval = 1000 * 45; // 45 Seconds
function update() {
    $.getJSON('/update', function(data) {
        if (data.amount != 0){
            var html = '';

            for (i in data.events) {
                html += '<li class="wrap-event '+ data.events[i].service + '"><div>' + data.events[i].html +'</div></li>';
            };
            $('#brook').prepend(html);
            $('.timestamp').timeago('refresh');
        };
    });
};

function set_min_height() {
    var padding = parseInt($('.panel').css('padding-top')) + parseInt($('.panel').css('padding-bottom'))
    
    if (window.innerHeight - padding < $('#left-panel').outerHeight() - padding) {
        $('#right-panel').css('min-height', $('#left-panel').outerHeight() - padding + 'px')
    } else {
        $('#right-panel').css('min-height', window.innerHeight - padding + 'px')
    }
};

$(window).resize(set_min_height)

$(document).ready(function() {
    $('.timestamp').timeago()
    set_min_height()
    setInterval(update, interval)
});