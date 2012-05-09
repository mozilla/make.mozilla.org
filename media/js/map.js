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

	var months = ['January', 'February', 'March', 'April', 'May', 'June',
	        'July', 'August', 'September', 'October', 'November', 'December'],
	    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

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
	    searchLocation,
	    eventStack = [],
	    standardMarker,
	    largeMarker;

	if (!container) return false;

	gmap_callback = 'gmcb_'+(""+Math.random()).substr(2);
	window[gmap_callback] = function () {
		delete window[gmap_callback];

		InfoBox.init();

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

		standardMarker = new google.maps.MarkerImage(
			'/media/img/map-marker.png',
			new google.maps.Size(16,16),
			new google.maps.Point(0,0),
			new google.maps.Point(8,8)
		);

		largeMarker = new google.maps.MarkerImage(
 			'/media/img/map-marker.png',
			new google.maps.Size(32,32),
			new google.maps.Point(16,0),
			new google.maps.Point(16,16)
		);

		google.maps.event.addListener(gmap, 'zoom_changed', function () {
			for (var key in venue_cache) {
				if (venue_cache.hasOwnProperty(key)) {
					if (venue_cache[key].visible) {
						google.maps.event.trigger(venue_cache[key].marker, 'click');
					}
				}
			}
		});

		if (eventStack.length) {
			add_event.apply(null, eventStack);
			eventStack = [];
		}
	}

	gmap_script = document.createElement("script");
	gmap_script.src = "http://maps.google.com/maps/api/js?sensor=false&callback=" + gmap_callback;
	document.body.appendChild(gmap_script);

	if (search) {
		search.form.onsubmit = function () {
			if (searchLocation) {
				window.location = c('target').replace(/\${(\w+)}/g, function(match, key) {
					return searchLocation.hasOwnProperty(key) ? searchLocation[key] : '';
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
				searchLocation = ui.item ? ui.item.location : null;
			},
			change: function (event, ui) {
				searchLocation = ui.item ? ui.item.location : null;
			}
		});
	}

	var address_cache = {},
	    venue_cache = {};

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

	function add_event (event) {
		if (!gmap) {
			eventStack.push.apply(eventStack, arguments);
		} else {
			for (var i = 0, l = arguments.length; i < l; ++i) {
				(function(event) {
					var address = event.address,
					    lat = event.latitude,
					    lng = event.longitude,
					    venue_hash = (Math.round(lat * 10000) / 10000) + ':' + (Math.round(lng * 10000) / 10000),
					    venue = venue_cache[venue_hash];

					if (!venue) {
						var content = document.createElement("div");

						var marker = new google.maps.Marker({
							position: new google.maps.LatLng(lat, lng),
							map: gmap,
							icon: standardMarker
						});

						var panel = new InfoBox({
							content: content,
							alignBottom: true,
							pixelOffset: new google.maps.Size(-50, -32),
							infoBoxClearance: new google.maps.Size(40, 40),
							closeBoxURL: '/media/img/close.png'
						});

						google.maps.event.addListener(panel, 'closeclick', function () {
							marker.setIcon(standardMarker);
						});

						google.maps.event.addListener(panel, 'domready', function () {
							var box = this.getContent().parentNode,
							    projection = this.getProjection(),
							    location = projection.fromLatLngToContainerPixel(marker.position),
							    targetX = location.x + box.offsetWidth / 2 + (this.pixelOffset_.width||0),
							    targetY = location.y - box.offsetHeight + (this.pixelOffset_.height||0) + (container.offsetHeight / 2)
							        - $(search.form).offset().top - search.form.offsetHeight - 40,
							    target = projection.fromContainerPixelToLatLng(new google.maps.Point(targetX, targetY));
							
							gmap.panTo(target);
						});

						venue = {
							name: null,
							address: address,
							events: [],
							latitude: lat,
							longitude: lng,
							marker: marker,
							panel: panel,
							visible: false
						};

						geocode(address, function(results) {
							if (results && results.length) {
								venue.address = results[0].formatted_address;
								if (venue.visible) {
									google.maps.event.trigger(marker, 'click');
								}
							}
						});

						google.maps.event.addListener(marker, 'click', function() {
							for (var key in venue_cache) {
								if (venue_cache.hasOwnProperty(key)) {
									venue_cache[key].visible = false;
									venue_cache[key].panel.close();
									venue_cache[key].marker.setIcon(standardMarker);
								}
							}

							venue.visible = true;
							marker.setIcon(largeMarker);

							var html = [];

							if (venue.name) {
								html.push('<h3>'+venue.name+'</h3>');
								html.push('<h4>'+venue.address+'</h4>');
							} else {
								// Shouldn't happen, as venues *should* have names, but just in case...
								html.push('<h3>'+venue.address+'</h3>');
							}

							html.push('<ol>');

							for (var i = 0, l = venue.events.length; i < l; ++i) {
								var event = venue.events[i],
								    from_ts = '',
								    from_date = months[event.from.getMonth()] + ' ' + event.from.getDate() + ', ' + event.from.getFullYear(),
								    from_h = event.from.getHours(),
								    from_m = event.from.getMinutes(),
								    from_time = (from_h % 12 === 0 ? 12 : from_h % 12) + ':' + (from_m < 10 ? '0' : '') + from_m + ' ' + (from_h < 12 ? 'AM' : 'PM'),
								    from = from_date + ' ' + from_time,
								    to_ts = '',
								    to_date = months[event.to.getMonth()] + ' ' + event.to.getDate() + ', ' + event.to.getFullYear(),
								    to_h = event.to.getHours(),
								    to_m = event.to.getMinutes(),
								    to_time = (to_h % 12 === 0 ? 12 : to_h % 12) + ':' + (to_m < 10 ? '0' : '') + to_m + ' ' + (to_h < 12 ? 'AM' : 'PM'),
								    to = from_date === to_date ? to_time : to_date + ' ' + to_time;

								// console.log(event.from, event.to);

								html.push('<li' + (event.official ? ' class="official"' : '') + '>');
								html.push('<a href="' + event.url + '" class="name">' + event.name + '</a>');
								html.push('<span class="date"><time class="from" datetime="' + from_ts + '">' + from + '</time><span> to </span><time class="to" datetime="' + to_ts + '">' + to + '</time></span>');
								html.push('<a href="' + event.type.url + '" class="type">' + event.type.name + '</a>');
								html.push('</li>');
							}

							html.push('</ol>');

							content.innerHTML = html.join('\n');
							panel.open(gmap,marker);
						});

						venue_cache[venue_hash] = venue;
					}

					venue.name = venue.name || event.venue;
					venue.events.push(event);
					venue.marker.setTitle(venue.name + (venue.events.length > 1 ? ' (' + venue.events.length + ')' : '' ));
					google.maps.event.trigger(venue.marker, 'click');
				})(arguments[i]);
			}
		}
	}

	return {
		center: center_map,
		geocode: geocode,
		add_event: add_event
	};

})(window.map_config || {});