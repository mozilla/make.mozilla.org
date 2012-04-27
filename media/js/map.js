var map = (function (config) {

	var default_config = {
		container: 'map-container',
		latitude: 0,
		longitude: 0,
		zoom: 12,
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