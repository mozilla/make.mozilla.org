class celery {
  $celery_user = 'celery'
  $celery_group = 'celery'
  $celery_home_dir = '/var/lib/celery'

  file { "/var/log/celery":
    owner => $celery_user, group => $celery_group, mode => '755',
    require => Class['app_users'],
    ensure => directory;
  }
  
  file { "/var/run/celery":
    ensure => directory;
  }

  file { "/etc/celery":
    owner => 'root', group => 'root', mode => '755',
    ensure => directory;
  }

  create_system_user { $celery_user:
    group => $celery_group,
    homedir => $celery_home_dir;
  }

  file { "/etc/celery/celeryd.conf":
    owner => 'root', group => 'root', mode => '755',
    require => File['/etc/celery'],
    source => '/etc/puppet/files/celery/celeryd.conf';
  }

  file { "/etc/init.d/celeryd":
    owner => 'root', group => 'root', mode => '755',
    require => [File['/etc/celery/celeryd.conf'], File['/var/run/celery'], File['/var/log/celery'], Create_system_user[$celery_user]],
    source => '/etc/puppet/files/celery/celeryd.init';
  }

  service { "celeryd":
    ensure => running,
    hasstatus => true,
    require => [File['/etc/init.d/celeryd'], Service['redis-server']];
  }
}
