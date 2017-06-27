$(document).ready(function(){

$.ajax({
    url: '/api/data/',
    type: 'get',
    success: function(data) {
        book_titles = []
        jQuery.each(data, function(i, val) {
            book_titles.push(val['fields']['book_title'])
        })
        var options = {
            data: book_titles,
            list: {
                match: {
                    enabled: true
                }
            }
        };
        $('#basics').easyAutocomplete(options)
    },
    failure: function(data) { 
        alert('There seems to be a problem.');
    }
});

var ready = false;

if (ready != true) {
    $('.col-9').append('<div class="loader"><i class="fa fa-circle-o-notch fa-spin fa-3x fa-fw"><i>')
}
jQuery(document).ready(function() {
    ready = true
    $('.loader').remove()
});

}); 