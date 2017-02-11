/**
 * Created by mahshid on 2/11/2017 AD.
 */

function initMap() {
    var uluru = {lat:35.705000898757824, lng: 51.35031223297119};
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: uluru
    });
    var marker = new google.maps.Marker({
      position: uluru,
      map: map
    });
}
