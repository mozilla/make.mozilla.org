class nodejs {
  package { "python-software-properties":
    ensure => present;
  }

  exec { 'add-node-ppa':
    command => 'add-apt-repository ppa:chris-lea/node.js && apt-get update',
    creates => '/etc/apt/sources.list.d/chris-lea-node.js-lucid.list',
    require => Package['python-software-properties'];
  }

  package { 'nodejs':
    ensure => 'present';
  }

  package { 'npm':
    ensure => 'present',
    require => Package['nodejs'];
  }
}
