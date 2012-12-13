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

$(document).ready(function() {
    $('.timestamp').timeago()
    setInterval(update, interval)
});