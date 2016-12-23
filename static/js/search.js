/**
 * Created by mahshid on 12/22/2016 AD.
 */
    function searchFunction(element) {
        var x = document.getElementById(element).value;
        window.location = '/search/' + x +"/";
    }