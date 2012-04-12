# Install PostGIS
class postgis {
    package { "postgresql-8.4-postgis":
        ensure => installed;
    }

    file { '/usr/share/postgis':
      ensure => directory,
      owner => "root", group => "root", mode => 755,
    }

    file { '/usr/share/postgis/create_template_postgis.sh':
        mode => '755',
        owner => 'root',
        group => 'root',
        source => '/etc/puppet/files/usr/share/postgis/create_template_postgis.sh',
        require => [Package['postgresql-8.4-postgis', 'postgresql-client'],
                   File['/usr/share/postgis']];
    }

    exec { "fix_up_pg_encoding":
      command => "pg_dropcluster --stop 8.4 main && pg_createcluster --start -e UTF-8 8.4 main",
      unless => "sudo -u postgres psql -d template1 -c 'SHOW SERVER_ENCODING' | grep UTF8",
      require => Package['postgresql'];
    }

    exec { "create_postgis_template":
        command => "sudo -u postgres /usr/share/postgis/create_template_postgis.sh",
        unless  => "sudo -u postgres psql -l | awk '{ print $1 }' | grep '^template_postgis$'",
        require => [File['/usr/share/postgis/create_template_postgis.sh'],
                   Package['postgresql-8.4-postgis', 'postgresql-client'], 
                   Service['postgresql'],
                   Exec['fix_up_pg_encoding']];
    }
}
