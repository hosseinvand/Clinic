(function($){
    $(function(){

        $('.parallax').parallax();
        $('.button-collapse').sideNav({edge:"right"});
        $(".dropdown-button").dropdown({
            belowOrigin: true,
            hover: true
        });

    }); // end of document ready
})(jQuery); // end of jQuery name space