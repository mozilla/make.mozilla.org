var map = (function (config) {

	var location = [
		[ 37.387807, -122.082656], // Mountain View
		[-36.866596,  174.777106], // Auckland
		[ 39.909901,  116.434050], // Beijing
		[ 51.510718,   -0.127072], // London
		[ 48.871356,    2.343891], // Paris
		[ 37.789031, -122.389326], // San Francisco
		[ 35.685021,  139.738455], // Tokyo
		[ 43.647523,  -79.394025], // Toronto
		[ 49.282076, -123.107774]  // Vancouver
	].sort(function() {return 0.5 - Math.random()})[0];

	var default_config = {
		container: 'map-container',
		latitude: location[0],
		longitude: location[1],
		zoom: 13,
		controls: false,
		draggable: false
	}

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(location) {
			var lat = location.coords.latitude,
			    lng = location.coords.longitude;

			default_config.latitude = lat;
			default_config.longitude = lng;
			map.center(lat, lng);
		});
	}

	var c = function(property) {
		return config.hasOwnProperty(property) ? config[property] : default_config[property];
	}

	var container = document.getElementById(c('container')),
	    gmap_script,
	    gmap_callback,
	    gmap,
	    geocoder;

	if (!container) return false;

	gmap_callback = 'gmcb_'+(""+Math.random()).substr(2);
	window[gmap_callback] = function () {
		delete window[gmap_callback];

		geocoder = new google.maps.Geocoder();

		gmap = new google.maps.Map(container, {
			zoom: c('zoom'),
			center: new google.maps.LatLng(c('latitude'), c('longitude')),
			mapTypeId: google.maps.MapTypeId.ROADMAP,

			scrollwheel: false,
			keyboardShortcuts: false,
			disableDoubleClickZoom: true,
			disableDefaultUI: true,
			draggable: c('draggable'),

			zoomControl: c('controls'),
			zoomControlOptions: {
				style: google.maps.ZoomControlStyle.SMALL,
				position: google.maps.ControlPosition.LEFT_BOTTOM
			}
		});
	}

	gmap_script = document.createElement("script");
	gmap_script.src = "http://maps.google.com/maps/api/js?sensor=false&language=sk&callback=" + gmap_callback;
	document.body.appendChild(gmap_script);

	return {
		center: function (lat, lng) {
			if (!gmap) return false;
			gmap.setCenter(new google.maps.LatLng(lat,lng));
			return true;
		},
		geocode: function (address, callback) {
			
		}
	}

})(window.map_config || {});