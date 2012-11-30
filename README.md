Local development
=================

In addition to the more specific requirements below you need the standard set of software
to get playdoh installed:

* Xcode (with the Command Line Tools installed)
* mySQL (a playdoh dependancy - though we're not using it for this project)
* node and lessc
* wget

We're using PostGIS + GeoDjango for the DB, so you'll also need the following installed:

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

**Note** The current version of PostGIS in Homebrew is version 2.0.0 - you need to install 1.5.3 (due to a numder of compatibility issues)

Ubuntu
------

For Ubuntu 10.04, see the information in our Puppet config (`./puppet/manifests/dev.pp` and the classes in `./puppet/manifests/classes`)

For Ubuntu release >= 11.10, this should work:

    sudo apt-get install binutils gdal-bin libproj-dev postgresql-9.1-postgis \
         postgresql-server-dev-9.1

Once those are installed, then `pip install -r requirements/compiled.txt` should 
work as expected.

Making it run locally
=====================

Checkout the sourcecode and init the git submodules:

    git clone --recursive git://github.com/mozilla/make.mozilla.org

If at any point you realize you forgot to clone with the recursive flag, you
can fix that by running:

    git submodule update --init --recursive

Once you have all the dependencies installed, you need to create a settings
file.

    cp make_mozilla/settings/local.py{-dist,}

And then edit the settings file to match your needs, here is the section about
the databases:

    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'webmaker',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432',
            'TEST_CHARSET': 'utf8',
            'TEST_COLLATION': 'utf8_general_ci',
        },
    }


Setting up the database
=====================

GeoDjango
---------

GeoDjango is installed as part of Django. You need to take a look at the installation 
instructions at [https://docs.djangoproject.com/en/1.3/ref/contrib/gis/install/#post-installation] 
to get PostGIS configured properly with Django. Ubuntu's version ships with a postgis-template generation script, which you can see used in `./puppet/manifests/classes/postgis.pp`

Once you've installed postgis, you need to create a template for it, and then
create your database with this template. For postgis 1.5:

    cd /tmp && wget https://raw.github.com/django/django/master/docs/ref/contrib/gis/install/create_template_postgis-1.5.sh
    sudo su postgres
    /tmp/create_template_postgis-1.5.sh

And finally create the database:

    createdb -T template_postgis webmaker

Populating it
-------------

    ./manage.py syncdb
    ./manage.py migrate
    

Compiling the assets
--------------------

You also need to compile the assets, be sure to update your settings with the path to your LESS executable:

    LESS_BIN = "/usr/local/bin/lessc"

And then run:

    ./manage.py compress_assets

playdoh: about the framework
============================

This app is built using Mozilla's Playdoh.

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

