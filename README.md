make.mozilla.org
================

This app is built using Mozilla's Playdoh.

We're using PostGIS + GeoDjango for the DB, so you'll also need the following installed

* Postgresql 8.4 +
* PostGIS >= 1.4 && < 2.0
* Geos
* Proj4
* GDAL

Mac OS X
--------

With [Homebrew][brew], installing PostGIS and GDAL will install all you need:

    brew update
    brew install postgis gdal

[brew]: http://mxcl.github.com/homebrew/

Ubuntu
------

For Ubuntu 10.04, see the information in our Puppet config (`./puppet/manifests/dev.pp` and the classes in `./puppet/manifests/classes`)

For Ubuntu release >= 11.10, this should work:

    sudo apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis \
         postgresql-server-dev-9.1

Once those are installed, then `pip install -r requirements/compiled.txt` should 
work as expected.

GeoDjango
---------

GeoDjango is installed as part of Django. You need to take a look at the installation 
instructions at [https://docs.djangoproject.com/en/1.3/ref/contrib/gis/install/#post-installation] 
to get PostGIS configured properly with Django. Ubuntu's version ships with a postgis-template generation script, which you can see used in `./puppet/manifests/classes/postgis.pp`

playdoh
-------

Mozilla's Playdoh is a web application template based on [Django][django].

Patches are welcome! Feel free to fork and contribute to this project on
[github][gh-playdoh].

Full Playdoh [documentation][docs] is available as well.

[django]: http://www.djangoproject.com/
[gh-playdoh]: https://github.com/mozilla/playdoh
[docs]: http://playdoh.rtfd.org/


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://creativecommons.org/licenses/BSD/

