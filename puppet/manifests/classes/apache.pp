class apache {
  package { "apache2-dev":
    ensure => present,
    before => File['/etc/apache2/sites-available/playdoh'];
  }

  file { "/etc/apache2/sites-available/playdoh":
    source => "/etc/puppet/files/etc/httpd/conf.d/playdoh.conf",
    owner => "root", group => "root", mode => 0644,
    require => [
        Package['apache2-dev']
    ];
  }

  exec {
    'a2enmod rewrite':
      onlyif => 'test ! -e /etc/apache2/mods-enabled/rewrite.load';
    'a2enmod proxy':
      onlyif => 'test ! -e /etc/apache2/mods-enabled/proxy.load';
    'a2ensite playdoh': 
      require => [Package['apache2-dev'], File['/etc/apache2/sites-available/playdoh']];
  }

  service { "apache2":
    ensure => running,
    enable => true,
    require => [
      Package['apache2-dev'],
      File['/etc/apache2/sites-available/playdoh'],
      Exec['a2ensite playdoh']
    ];
  }
}
