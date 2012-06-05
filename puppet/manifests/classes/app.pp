# Create the bare DB, set up the basic app install path

class app {
  exec { "create_db":
    command => "sudo -u postgres createdb -O ${::db_user} -T template_postgis ${db}",
    unless  => "sudo -u postgres psql -l | awk '{ print \$1 }' | grep '^${db}$'",
    logoutput => true,
    require => [Class['postgis'], Exec["create_db_user"]];
  }

  exec { "create_virtualenv":
    command => "sudo -u ${app_user} virtualenv --no-site-packages ${app_root}/virtualenv",
    onlyif => "test ! -e ${app_root}/virtualenv/bin/python",
    require => [Class['python'], File[$app_root], User[$app_user]];
  }

  cron { "import_bsd_events":
    command => "cd ${app_root}/current && ${app_root}/virtualenv/bin/python manage.py cron import_bsd_events",
    user => $app_user,
    minute => [5,15,25,35,45,55],
    require => [File[$app_root], User[$app_user]];
  }

  cron { "update_site_feeds":
    command => "cd ${app_root}/current && ${app_root}/virtualenv/bin/python manage.py cron update_site_feeds",
    user => $app_user,
    minute => [5,35],
    require => [File[$app_root], User[$app_user]];
  }

  define reap_bsd_events ( $minutes ) {
    cron { "reap_bsd_events_${name}":
      command => "cd ${app_root}/current && ${app_root}/virtualenv/bin/python manage.py cron reap_bsd_events $name",
      user => $app_user,
      minute => $minutes,
      require => [File[$app_root], User[$app_user]];
    }
  }
  reap_bsd_events { "1":
    minutes => [3,23,43];
  }
  reap_bsd_events { "2":
    minutes => [8,28,48];
  }
  reap_bsd_events { "3":
    minutes => [13,33,53];
  }
  reap_bsd_events { "4":
    minutes => [18,38,58];
  }
}
