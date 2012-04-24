class app_dependencies {
  package { "libxml2-dev":
    ensure => present,
    before => Class['app'];
  }
  package { "libxslt1-dev":
    ensure => present,
    before => Class['app'];
  }
}
