/**
 * Created by mahshid on 12/22/2016 AD.
 */
    function searchFunction(elementId) {
        var x = document.getElementById(elementId).value;
        window.location = '/search/' + x +"/";
    }