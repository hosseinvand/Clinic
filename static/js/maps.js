/**
 * Created by mahshid on 2/11/2017 AD.
 */

function initMap() {
    var uluru = {lat: 35.705000898757824, lng: 51.35031223297119};
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: uluru
    });
    var marker = new google.maps.Marker({
        position: uluru,
        map: map
    });
    google.maps.event.trigger(map, 'resize');

}

//
// $('#officeinfo').on('shown', function () {
//     initMap(); // google map init function
// });

// $('#tab2').on('active', function () {
//     initMap(); // google map init function
// });


//<![CDATA[

// global "map" variable
var map = null;
var marker = null;


// A function to create the marker and set up the event window function
function createMarker(latlng) {
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
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
        var clicked_lat = event.latLng.lat();
        var clicked_lng = event.latLng.lng();

        document.getElementById("lat").value = clicked_lat;
        document.getElementById("lng").value = clicked_lng;

        console.log(clicked_lat);
        console.log(clicked_lng);

    });


}


//]]>
