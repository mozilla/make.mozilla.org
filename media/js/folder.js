(function() {

    var dbs = document.body.style;

    if (!('WebkitTransform' in dbs)
            && !('MozTransform' in dbs)
            && !('OTransform' in dbs)
            && !('MsTransform' in dbs)
            && !('transform' in dbs)) {
        return;
    }

    var fold = function(image) {
        var folds = (image.className.match(/\bfolds-(\d+)/)||[9]).pop(),
            container = document.createElement('span'),
            parent = image.parentNode,
            width = image.width,
            sectionWidth = width / (folds+1),
            angle = 8 * Math.PI/180,
            scale = 1 / Math.cos(angle);

        container.className = 'folded-container';

        for (var i = 0; i <= folds; ++i) {
            var section = document.createElement('span'),
                img = document.createElement('img'),
                down = !!(i % 2);

            img.src = image.src;
            img.style.marginLeft = (-i * sectionWidth) + 'px';

            section.className = [
                'section',
                i ? (i < folds ? 'mid' : 'last') : 'first',
                down ? 'outer' : 'inner'
            ].join(' ');
            section.style.width = sectionWidth + 'px';
            section.style.WebkitTransform = 'perspective(1000px) scaleX(' + scale + ') skewY(' + (down ? '' : '-') + angle + 'rad)';
            section.style.MozTransform = 'perspective(1000px) scaleX(' + scale + ') skewY(' + (down ? '' : '-') + angle + 'rad)';
            section.style.MsTransform = 'perspective(1000px) scaleX(' + scale + ') skewY(' + (down ? '' : '-') + angle + 'rad)';
            section.style.OTransform = 'perspective(1000px) scaleX(' + scale + ') skewY(' + (down ? '' : '-') + angle + 'rad)';
            section.style.transform = 'perspective(1000px) scaleX(' + scale + ') skewY(' + (down ? '' : '-') + angle + 'rad)';
            section.appendChild(img);

            container.appendChild(section);
        }

        parent.removeChild(image);
        parent.appendChild(container);
    }

    $('img.foldable').each(function() {
        if (this.width) {
            fold(this);
        } else {
            $(this).load(function() {
                fold(this);
            });
        }
    });

})();