if (document && document.querySelectorAll) {
	(function () {
		function initTicker ($elem) {
			var $$titles = $elem.querySelectorAll('dt'),
			    $$metas = $elem.querySelectorAll('dd'),
			    $navigator = document.createElement('ol'),
			    $$navItems = [],
			    label = $elem.getAttribute('data-label'),
			    currentIndex = 0,
			    timeout;

			var select = function (index) {
				clearTimeout(timeout);

				currentIndex = index % $$navItems.length;

				for (var i = 0, l = $$navItems.length; i < l; ++i) {
					$$titles[i].className = $$titles[i].className.replace(/\s*\bactive\b/, '');
					$$metas[i].className = $$metas[i].className.replace(/\s*\bactive\b/, '');
					$$navItems[i].className = $$metas[i].className.replace(/\s*\bactive\b/, '');

					if (i === currentIndex) {
						$$titles[i].className += ' active';
						$$metas[i].className += ' active';
						$$navItems[i].className += ' active';
					}
				}

				timeout = setTimeout(function() {
					select(currentIndex+1);
				}, 10000);
			}

			for (var i = 0, l = $$titles.length; i < l; ++i) {
				if (label) {
					$$titles[i].setAttribute('data-label', label);
					$$metas[i].setAttribute('data-label', label);
				}

				var title = $$titles[i].innerText,
				    $navItem = document.createElement('li');

				$navItem.title = title;
				$navItem.innerHTML = '<span>'+title+'</span>';
 				$navItem.setAttribute('tabIndex', '0');

				$navItem.onclick = $navItem.onfocus = (function(index) {
					return function() {
						select(index);
					}
				})(i);

				$$navItems.push($navItem);

				$navigator.appendChild($navItem);
			}

			$elem.appendChild($navigator);
			$elem.className += ' enabled';

			select(0);
		}

		var $$tickers = document.querySelectorAll('.meta-ticker');

		for (var i = 0, l = $$tickers.length; i < l; ++i) {
			initTicker($$tickers[i]);
		}
	})();
}
