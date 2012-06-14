class apache {
  package { "apache2-prefork-dev":
    ensure => present,
    before => File['/etc/apache2/sites-available/playdoh'];
  }

  $server_aliases = $fqdn ? {
    'make-dev1.vm.labs.scl3.mozilla.com' => ['make-dev.mozillalabs.com'],
    'make-stage1.vm.labs.scl3.mozilla.com' => ['make-stage.mozillalabs.com'],
    'make-prod1.vm.labs.scl3.mozilla.com' => ['webmaker.org'],
    default => [],
  }

  file { "/etc/apache2/sites-available/playdoh":
    content => template("/etc/puppet/templates/apache.conf.erb"),
    owner => "root", group => "root", mode => 0644,
    notify  => Service['apache2'],
    require => [
        Package['apache2-prefork-dev']
    ];
  }

  exec {
    'a2enmod rewrite':
      onlyif => 'test ! -e /etc/apache2/mods-enabled/rewrite.load';
    'a2enmod proxy':
      onlyif => 'test ! -e /etc/apache2/mods-enabled/proxy.load';
    'a2dissite default && /etc/init.d/apache2 graceful':
      onlyif => 'test -L /etc/apache2/sites-enabled/000-default';
    'a2ensite playdoh':
      require => [Package['apache2-prefork-dev'], File['/etc/apache2/sites-available/playdoh']],
      onlyif => 'test ! -L /etc/apache2/sites-enabled/playdoh';
  }

  service { "apache2":
    ensure => running,
    enable => true,
    require => [
      Package['apache2-prefork-dev'],
      File['/etc/apache2/sites-available/playdoh'],
      Exec['a2ensite playdoh']
    ];
  }
}
