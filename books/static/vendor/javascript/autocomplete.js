$(document).ready(function(){

$.ajax({
    url: '/api/data/',
    type: 'get',
    success: function(data) {
        book_titles = []
        jQuery.each(data, function(i, val) {
            book_titles.push(val['fields']['book_title'])
            if($.inArray(val['fields']['book_author'], book_titles) === -1) book_titles.push(val['fields']['book_author']);
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

$(function () {
  $('[data-toggle="popover"]').popover()
})

}); 