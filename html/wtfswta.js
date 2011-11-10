$(document).ready(function() {
    var base_url = document.location.protocol+'//'+document.location.host;
    (function($) {
        $.fn.topic = function() {
            var elem = $(this);
            elem.html('').addClass('load');
            $.ajax({
                url: base_url+'/api/1/topics/',
                dataType: 'json',
                success: function(data) {
                    elem.removeClass('load').html(data.data[0]['topic']);
                },
                error: function() {
                    $('#topic-error').addClass('show');
                }
            });
            return this;
        }
    })(jQuery)

    $('#topic').topic();
    $('h2 a').click(function() {
        $('#topic').topic();
    });

    $('a.close').click(function() {
        $(this).parent('div').removeClass('show');
    });
});
