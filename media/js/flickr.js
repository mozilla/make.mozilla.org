(function() {
    var api = function(method, request, callback) {
        var data = {
            api_key: 'b939e5bd8aa696db965888a31b2f1964',
            method: 'flickr.' + method,
            format: 'json'
        };

        for (var property in request) {
            if (request.hasOwnProperty(property)
                    && 'method|dataset|context'.indexOf(property) == -1) {
                data[property] = request[property];
            }
        }

        $.ajax('https://secure.flickr.com/services/rest/', {
            data: data,
            dataType: 'jsonp',
            jsonp: 'jsoncallback',
            success: function(data) {
                if (data.stat === 'ok') {
                    callback(data[request.dataset]);
                }
            }
        });
    }

    var printf = function(format, data) {
        return format.replace(/%{([\w-]+(?:,[\w-]+)*)}/g, function(match, keys) {
            for (var i = 0, keys = keys.split(','), l = keys.length; i < l; ++i) {
                if (data.hasOwnProperty(keys[i]) && data[keys[i]] !== null) {
                    return data[keys[i]];
                }
            }
            return '';
        });
    }

    var generateTag = function(photo) {
        var href = photo.url_sq,
            title = photo.title,
            link = printf('http://www.flickr.com/photos/%{pathalias,owner}/%{id}/%{context}', photo),
            img = '<img src="' + href + '" alt="' + title + '" title="' + title + '">';

        return '<a href="' + link + '">' + img + '</a>';
    }

    $('a.flickr-link').each(function(index, link) {
        var url = link.getAttribute('href'),
            $container = $('#' + link.getAttribute('for')).addClass('loading');

        if (url && $container.length) {
            api('urls.lookupUser', {url:url,dataset:'user'}, function(data) {
                var meta = url.match(/^.*\/photos\/([\w-]+)\/(sets\/\w+|galleries\/\w+|favorites|)\/?.*$/);
                    name = meta[1],
                    meta = (meta[2]||'').split('/'),
                    store = meta[0],
                    key = meta[1];

                var user = {
                    id: data.id,
                    displayname: data.username._content,
                    name: name
                };

                var request = {
                    media: 'photos',
                    extras: ['url_sq', 'path_alias'].join(',')
                };

                switch (store) {
                    case 'sets':
                        request.method = 'photosets.getPhotos';
                        request.dataset = 'photoset';
                        request.photoset_id = key;
                        request.context = 'set-' + key;
                        break;
                    case 'galleries':
                        request.method = 'galleries.getPhotos';
                        request.dataset = 'photos';
                        request.gallery_id = user.id.split('@')[0] + '-' + key;
                        request.context = 'gallery-' + user.name + '-' + key;
                        break;
                    case 'favorites':
                        request.method = 'favorites.getPublicList';
                        request.dataset = 'photos';
                        request.user_id = user.id;
                        request.context = 'faves-' + user.name;
                        break;
                    default:
                        $container.removeClass('loading');
                        return;
                }

                api(request.method, request, function(data) {
                    var photos = data.photo,
                        html = [],
                        context = request.context ? 'in/' + request.context + '/' : '',
                        count = Math.min(8, photos.length)
                        loaded = 0;

                    photos.sort(function() { return Math.random() - 0.5; });

                    for (var i = 0; i < count; ++i) {
                        photos[i].context = context;
                        html.push(generateTag(photos[i]));
                    }

                    $container.html('<ul><li>' + html.join('</li><li>') + '</li></ul>')
                        .find('img').load(function(){
                            if (++loaded === count) {
                                $container.removeClass('loading');
                            }
                        });
                })
            });
        }
    });
})();