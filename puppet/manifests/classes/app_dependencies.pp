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
    ensure => present,
    before => Class['app'];
  }

  service { "redis-server":
    ensure => running,
    enable => true,
    require => Package['redis-server'];
  }
}
