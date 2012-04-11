# Install PostGIS
class postgis {
    package { "postgresql-8.4-postgis":
        ensure => installed;
    }

    file { '/usr/share/postgis/create_template_postgis.sh':
        mode => '750',
        owner => root,
        group => root,
        source => 'puppet:///files/usr/share/postgis/create_template_postgis.sh',
        require => Package['postgresql-8.4-postgis', 'postgresql-client'];
    }

    exec { "create_postgis_template":
        command => "/usr/share/postgis/create_template_postgis.sh",
        require => [File['/usr/share/postgis/create_template_postgis.sh'],
                   Package['postgresql-8.4-postgis', 'postgresql-client'], 
                   Service['postgresql']];
    }
}
