# Get postgres up and running
class postgresql {
    package { "postgresql":
        ensure => installed;
    }

    package { "postgresql-client":
        ensure => installed;
    }

    package { "libpq-dev":
        ensure => installed,
        require => Package['postgresql'];
    }

    service { "postgresql":
        name => 'postgresql-8.4',
        ensure => running,
        enable => true,
        hasstatus => true,
        require => [Package['postgresql'], Package['postgresql-client']];
    }

    exec { "create_db_user":
        command => "sudo -u postgres psql -c \"CREATE ROLE ${::db_user} NOSUPERUSER NOCREATEDB NOCREATEROLE PASSWORD '${::db_pass}' LOGIN;\";",
        unless => "sudo -u postgres psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='${::db_user}';\" | grep 1",
        require => Service['postgresql'];
    }
}
