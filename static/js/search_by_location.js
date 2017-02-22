/**
 * Created by mahshid on 2/14/2017 AD.
 */

var token;


function initLocationSearchMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 35.696, lng: 51.351},
        zoom: 14
    });
    var infoWindow = null;


    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
                var pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                var marker = new google.maps.Marker({
                    map: map,
                    position: pos,
                    icon: 'http://icons.iconarchive.com/icons/carlosjj/google-jfk/64/base-map-icon.png',
                    animation: google.maps.Animation.DROP,
                    title: 'مکان فعلی شما'
                });
                marker.addListener('click', toggleBounce);

                function toggleBounce() {
                    if (marker.getAnimation() !== null) {
                        marker.setAnimation(null);
                    } else {
                        marker.setAnimation(google.maps.Animation.BOUNCE);
                    }
                }

                map.setCenter(pos);
                $.ajax({
                    method: 'POST',
                    url: '/ajax/search_by_location/',
                    data: {
                        'lat': pos.lat,
                        'lng': pos.lng,
                        'csrfmiddlewaretoken': token
                    },
                    dataType: 'json',
                    success: function (response) {
                        for (i = 0; i < response.length; i++) {
                            (function (i) {
                                var doctor_id = response[i]['doctorSecretary'];
                                console.log(doctor_id)
                                $.ajax({
                                    method: 'GET',
                                    url: '/doctor_card/' + doctor_id,
                                    success: function (card_response) {
                                        var curr_office_pos = new google.maps.LatLng(
                                            parseFloat(response[i]['lat_position']),
                                            parseFloat(response[i]['lng_position'])
                                        );

                                        // console.log(curr_office_pos);
                                        // console.log(response[i]);
                                        // console.log(card_response);
                                        var office_string ="<div>"+ card_response +"</div>";
                                        var curr_office_marker = new google.maps.Marker({
                                            map: map,
                                            icon: 'http://icons.iconarchive.com/icons/carlosjj/google-jfk/48/maps-icon.png',
                                            animation: google.maps.Animation.DROP,
                                            position: curr_office_pos
                                        });
                                        console.log(doctor_id);
                                        google.maps.event.addListener(curr_office_marker, 'click', (function (content) {
                                            return function () {
                                                var marker_infowindow = new google.maps.InfoWindow({
                                                    map: map,
                                                    maxWidth: 190,
                                                    marginLeft: 0,
                                                    marginRight: 10,
                                                    paddingRight:15,
                                                });
                                                marker_infowindow.setContent(content);
                                                marker_infowindow.open(map, this);
                                            }
                                        }(office_string)));

                                    }
                                })

                            })(i);

                        }
                    }
                });

            }, function () {
                infoWindow = new google.maps.InfoWindow({map: map});
                handleLocationError(true, infoWindow, map.getCenter());
            },
            {timeout: 200000});
    } else {
        // Browser doesn't support Geolocation
        infoWindow = new google.maps.InfoWindow({map: map});
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}


