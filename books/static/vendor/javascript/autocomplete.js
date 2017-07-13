$(window).on("load", function(){

$.ajax({
    url: '/api/data/',
    type: 'get',
    success: function(data) {
        book_titles = []
        jQuery.each(data, function(i, val) {
            book_titles.push(val['fields']['book_title'])
            if($.inArray(val['fields']['book_author'], book_titles) === -1) book_titles.push(val['fields']['book_author']);
        })
    $( function() {

        $("#tags").autocomplete({
            source: function(request, response) {
                var results = $.ui.autocomplete.filter(book_titles, request.term);

                response(results.slice(0, 10));
            },
            focus: function (event, ui) {
                          $(".ui-helper-hidden-accessible").hide();
                          event.preventDefault();
                      },
            messages: {
                noResults: '',
                results: function() {}
            }
        });
      });
        },
    failure: function(data) { 
        alert('There seems to be a problem.');
    }
});

 

$(function () {
  $('[data-toggle="popover"]').popover()
})

}); 