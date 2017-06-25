$(document).ready(function(){

$.ajax({
    url: '/api/data/',
    type: 'get', // This is the default though, you don't actually need to always mention it
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

}); 