var map = null;
var marker = null;


// A function to create the marker and set up the event window function
function createMarker(latlng) {
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        icon: 'http://icons.iconarchive.com/icons/carlosjj/google-jfk/48/maps-icon.png',
        animation: google.maps.Animation.DROP,
        zIndex: Math.round(latlng.lat() * -100000) << 5
    });

    google.maps.event.trigger(marker, 'click');
    return marker;
}


function initOfficeMap() {
    // create the map
    var myOptions = {
        zoom: 11,
        center: {lat: 35.6929946320988, lng: 51.39129638671875},
        mapTypeControl: true,
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
        navigationControl: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("googleMap"),
        myOptions);

    google.maps.event.addListener(map, 'click', function (event) {
        //call function to create marker
        if (marker) {
            marker.setMap(null);
            marker = null;
        }
        marker = createMarker(event.latLng);
        console.log(marker);
        var clicked_lat = event.latLng.lat();
        var clicked_lng = event.latLng.lng();

        document.getElementById("lat").value = clicked_lat;
        document.getElementById("lng").value = clicked_lng;

        console.log(clicked_lat);
        console.log(clicked_lng);

    });


}