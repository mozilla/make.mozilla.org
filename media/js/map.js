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
        cluster: false,
        fit: null,
        filter: null,
        full: false,
        zoom: 13,
        controls: false,
        draggable: false,
        target: '/events/near/?lat=${lat}&lng=${lng}',
        countryTarget: '/events/in/${code}/'
    };

    var c = function(property) {
        return config.hasOwnProperty(property) ? config[property] : default_config[property];
    };

    var container = document.getElementById(c('container')),
        search = document.getElementById(c('search')),
        searchWrapper,
        gmap_script,
        gmap_callback,
        gmap,
        geocoder,
        clusterer,
        searchLocation,
        eventStack = [],
        standardMarkerImage,
        officialMarkerImage,
        shadowMarkerImage;

    if (!container) return false;

    if (navigator.geolocation) {
        (function() {
            var button = $(document.createElement('button'));
            button.addClass('button near-me');
            button.html('Near Me <img src="/media/img/loading.gif" alt="" title="" width="16" height="16">');
            $('.buttons', search.form).append(button);
            button.click(function() {
                button.addClass('loading');
                navigator.geolocation.getCurrentPosition(function(position) {
                    var location = { lat: position.coords.latitude, lng: position.coords.longitude };

                    window.location = c('target').replace(/\${(\w+)}/g, function(match, key) {
                        return location.hasOwnProperty(key) ? location[key] : '';
                    });
                }, function(error) {
                    button.removeClass('loading');
                });
            });
        })();
    }

    if (c('full')) {
        document.getElementById('content').className += ' full';
    }

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
            disableDoubleClickZoom: c('controls'),
            disableDefaultUI: true,
            draggable: c('draggable'),

            zoomControl: c('controls'),
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL,
                position: google.maps.ControlPosition.LEFT_BOTTOM
            }
        });

        if (c('cluster')) {
            clusterer = new MarkerClusterer(gmap, [], {
                styles: [{
                    url: '/media/img/map-cluster.png',
                    height: 55,
                    width: 50,
                    anchor: [18,0],
                    textColor: '#FFF',
                    textSize: 14
                }]
            });
        }

        if (c('fit')) {
            geocode(c('fit'), function(results) {
                if (results && results.length) {
                    var viewport = results[0].geometry.viewport,
                        center = viewport.getCenter();

                    gmap.fitBounds(viewport);

                    gmap.setZoom(gmap.getZoom() + 1);

                    var overlay = new google.maps.OverlayView();
                    overlay.draw = function() {};
                    overlay.setMap(gmap);

                    var projection = overlay.getProjection();

                    if (projection && projection.fromLatLngToContainerPixel) {
                        var current = projection.fromLatLngToContainerPixel(center),
                            target = new google.maps.Point(
                                current.x,
                                current.y - $(search.form.parentNode).offset().top
                            );

                        gmap.setCenter(projection.fromContainerPixelToLatLng(target));
                    }
                }
            });
        }

        standardMarkerImage = new google.maps.MarkerImage(
            '/media/img/map-marker.png',
            new google.maps.Size(50,75),
            new google.maps.Point(0,0),
            new google.maps.Point(25,75)
        );

        officialMarkerImage = new google.maps.MarkerImage(
            '/media/img/map-marker.png',
            new google.maps.Size(50,75),
            new google.maps.Point(50,0),
            new google.maps.Point(25,75)
        );

        shadowMarkerImage = new google.maps.MarkerImage(
            '/media/img/map-marker.png',
            new google.maps.Size(75,25),
            new google.maps.Point(100,50),
            new google.maps.Point(30,25)
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

        if (c('mapFooter')) {
            var footer = document.createElement('div');
            footer.className = 'footer';
            footer.innerHTML = '<div class="constrained">' + c('mapFooter') + '</div>';

            container.className += ' has-footer';
            container.appendChild(footer);
        }

        if (eventStack.length) {
            add_event.apply(null, eventStack);
            eventStack = [];
        }
    }

    gmap_script = document.createElement("script");
    gmap_script.src = "//maps.google.com/maps/api/js?sensor=false&callback=" + gmap_callback;
    document.body.appendChild(gmap_script);

    if (search) {
        search.form.onsubmit = function () {
            if (searchLocation) {
                window.location = c(searchLocation.targetRef).replace(/\${(\w+)}/g, function(match, key) {
                    return searchLocation.hasOwnProperty(key) ? searchLocation[key] : '';
                });
            }
            return false;
        }

        searchWrapper = document.createElement('span');
        search.parentNode.insertBefore(searchWrapper, search);
        searchWrapper.appendChild(search);

        $(search).keypress(function(e) {
            if ( e.which == 10 ) {
                e.preventDefault();
            }
        });

        $(search).autocomplete({
            appendTo: searchWrapper,
            autoFocus: false,
            minLength: 3,
            source: function (request, response) {
                geocode(request.term, function(results) {
                    var data = [];
                    if (results && results.length) {
                        for (var i = 0, l = Math.min(results.length, 6); i < l; ++i) {
                            var components = results[i].address_components,
                                geometry = results[i].geometry,
                                types = results[i].types.join('|');

                            if (types.indexOf('political') == -1) {
                                // skip this item if it's a landmark, feature, etc
                                continue;
                            }

                            var item = {
                                label: results[i].formatted_address,
                                value: results[i].formatted_address,
                            };

                            if (types.indexOf('country') > -1) {
                                item.location = {
                                    targetRef: 'countryTarget',
                                    code: components[0].short_name.toLowerCase()
                                };
                            } else if (types.indexOf('locality') > -1) {
                                // covers 'sublocality' too
                                item.location = {
                                    targetRef: 'target',
                                    lat: geometry.location.lat(),
                                    lng: geometry.location.lng()
                                };
                            }

                            if (item.location) {
                                data.push(item);
                            }
                        }
                    }

                    if (!data.length) {
                        data.push({
                            label: 'No results found',
                            value: null,
                            location: null
                        });
                    }

                    $(search).data('results', data);
                    response(data);
                });
            },
            open: function () {
                var results = $(search).data('results');
                searchLocation = (results &&results.length) ? results[0].location : null;
                $(this).addClass('with-results');
            },
            close: function () {
                $(this).removeClass('with-results');
            },
            select: function (event, ui) {
                searchLocation = ui.item ? ui.item.location : null;
                if (event.keyCode && event.keyCode == 13 && searchLocation) {
                    $(search.form).submit();
                }
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
            request = {
                address: address,
                region: c('filter')
            };
            geocoder.geocode(request, function(results, status) {
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
                            icon: standardMarkerImage,
                            shadow: shadowMarkerImage
                        });

                        if (clusterer) {
                            clusterer.addMarker(marker);
                        }

                        var panel = new InfoBox({
                            content: content,
                            alignBottom: true,
                            pixelOffset: new google.maps.Size(-50, -100),
                            infoBoxClearance: new google.maps.Size(40, 0),
                            closeBoxURL: '/media/img/close.png'
                        });

                        google.maps.event.addListener(panel, 'closeclick', function () {
                            venue.visible = false;
                        });

                        google.maps.event.addListener(panel, 'domready', function () {
                            var box = this.getContent().parentNode,
                                projection = this.getProjection(),
                                location = projection.fromLatLngToContainerPixel(marker.position),
                                targetX = location.x + box.offsetWidth / 2 + (this.pixelOffset_.width||0),
                                targetY = location.y - box.offsetHeight + (this.pixelOffset_.height||0) + (container.offsetHeight / 2)
                                    - $(search.form.parentNode).offset().top - search.form.parentNode.offsetHeight - 40
                                    + container.parentNode.offsetTop,
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
                                }
                            }

                            venue.visible = true;

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
                                    from_epoc = new Date(from_date + ' ' + from_time).getTime(),
                                    to_ts = '',
                                    to_date = months[event.to.getMonth()] + ' ' + event.to.getDate() + ', ' + event.to.getFullYear(),
                                    to_h = event.to.getHours(),
                                    to_m = event.to.getMinutes(),
                                    to_time = (to_h % 12 === 0 ? 12 : to_h % 12) + ':' + (to_m < 10 ? '0' : '') + to_m + ' ' + (to_h < 12 ? 'AM' : 'PM'),
                                    to = from_date === to_date ? to_time : to_date + ' ' + to_time,
                                    to_epoc = new Date(to_date + ' ' + to_time).getTime();

                                // console.log(event.from, event.to);

                                html.push('<li' + (event.official ? ' class="official"' : '') + '>');
                                html.push('<a href="' + event.url + '" class="name">' + event.name + '</a>');
                                html.push('<span class="date"><time class="from" datetime="' + from_ts + '">' + from + '</time>');
                                // events without an end time get imported with an end time 1 minute BEFORE the start date...
                                if (from_epoc < to_epoc) {
                                        html.push('<span> to </span><time class="to" datetime="' + to_ts + '">' + to + '</time>');
                                }
                                html.push('</span>');
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
                    if (event.official) venue.marker.setIcon(officialMarkerImage);
                    venue.marker.setTitle(venue.name + (venue.events.length > 1 ? ' (' + venue.events.length + ')' : '' ));
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
