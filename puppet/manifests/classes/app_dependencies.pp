class app_dependencies {
  package { "libxml2-dev":
    ensure => present,
    before => Class['app'];
  }

  package { "libxslt1-dev":
    ensure => present,
    before => Class['app'];
  }

  package { "redis-server":
    ensure => purged,
    before => [Class['app'], Exec['download-redis']];
  }
}
