(function($){
    $(function(){

        $('.parallax').parallax();
        $('.button-collapse').sideNav({
            edge: 'right',
        });
        $(".dropdown-button").dropdown({
            belowOrigin: true,
            hover: true
        });
        Materialize.updateTextFields();

    }); // end of document ready
})(jQuery); // end of jQuery name space