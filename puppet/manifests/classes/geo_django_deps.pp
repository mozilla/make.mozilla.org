# Install PostGIS
class geo_django_deps {
    package { "postgresql-8.4-postgis":
        ensure => installed,
        require => Package['postgresql'];
    }

    package { "gdal-bin":
        ensure => installed;
    }

    package { "libproj-dev":
        ensure => installed;
    }
}
