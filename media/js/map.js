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
		search: 'input-location',
		latitude: location[0],
		longitude: location[1],
		zoom: 13,
		controls: false,
		draggable: false,
		target: '/events/near/?lat=${lat}&lng=${lng}'
	};

	var c = function(property) {
		return config.hasOwnProperty(property) ? config[property] : default_config[property];
	};

	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(function(location) {
			var lat = location.coords.latitude,
			    lng = location.coords.longitude;

			default_config.latitude = lat;
			default_config.longitude = lng;
			center_map(lat, lng);
		});
	}

	var container = document.getElementById(c('container')),
	    search = document.getElementById(c('search')),
	    searchWrapper,
	    gmap_script,
	    gmap_callback,
	    gmap,
	    geocoder,
	    location;

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
	gmap_script.src = "http://maps.google.com/maps/api/js?sensor=false&callback=" + gmap_callback;
	document.body.appendChild(gmap_script);

	if (search) {
		search.form.onsubmit = function () {
			if (location) {
				window.location = c('target').replace(/\${(\w+)}/g, function(match, key) {
					return location.hasOwnProperty(key) ? location[key] : '';
				});
			}
			return false;
		}

		searchWrapper = document.createElement('span');
		search.parentNode.insertBefore(searchWrapper, search);
		searchWrapper.appendChild(search);

		$(search).autocomplete({
			appendTo: searchWrapper,
			autoFocus: true,
			delay: 100,
			source: function (request, response) {
				geocode(request.term, function(results) {
					var data = [];
					for (var i = 0, l = Math.min(results.length, 6); i < l; ++i) {
						data.push({
							label: results[i].formatted_address,
							value: results[i].formatted_address,
							location: {
								lat: results[i].geometry.location.lat(),
								lng: results[i].geometry.location.lng()
							}
						});
					}
					response(data);
				});
			},
			open: function () {
				$(this).addClass('with-results');
			},
			close: function () {
				$(this).removeClass('with-results');
			},
			select: function (event, ui) {
				location = ui.item ? ui.item.location : null;
			},
			change: function (event, ui) {
				location = ui.item ? ui.item.location : null;
			}
		});

		/*
		search.setAttribute("autocomplete", "off");
		search.form.onsubmit = function () {
			
		}

		searchWrapper = document.createElement('span');
		search.parentNode.insertBefore(searchWrapper, search);
		searchWrapper.appendChild(search);

		search.onkeyup = function () {
			clearTimeout(searchTimer);

			var address = search.value;

			searchResults && searchResults.parentNode && searchResults.parentNode.removeChild(searchResults);

			searchTimer = setTimeout(function() {
				if (address && search.value === address) {
					geocode(address, function(results) {

						if (results) {
							searchResults = document.createElement('ol');
							for (var i = 0, l = results.length; i < l; ++i) {
								var node = document.createElement('li'),
								    result = results[i],
								    data = {},
								    label,
								    location = result.geometry.location,
								    lat = location.lat(),
								    lng = location.lng();

								for (var i = 0, l = result.address_components.length; i < l; ++i) {
									data[result.address_components[i].types[0]] = result.address_components[i];
								}

								node.innerHTML = result.formatted_address + ' (' + lat + ', ' + lng + ')';
								searchResults.appendChild(node);
								console.log(result, data);
							}
							searchWrapper.appendChild(searchResults);
						}
					});
				}
			},100);
		}
		*/
	}

	var address_cache = {};

	function center_map (lat, lng) {
		if (!gmap) return false;
		gmap.setCenter(new google.maps.LatLng(lat,lng));
		return true;
	};

	function geocode (address, callback) {
		if (address_cache.hasOwnProperty(address)) {
			callback(address_cache[address], address);
		} else if (geocoder) {
			geocoder.geocode({address:address}, function(results, status) {
				if (status === google.maps.GeocoderStatus.OK) {
					address_cache[address] = results;
				} else {
					address_cache[address] = null;
				}
				callback(address_cache[address]);
			});
		} else {
			callback(null, address);
		}
	};

	return {
		center: center_map,
		geocode: geocode
	};

})(window.map_config || {});