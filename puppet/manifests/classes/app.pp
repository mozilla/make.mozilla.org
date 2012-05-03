# Create the bare DB, set up the basic app install path

class app {
  require app_users

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
    minute => [5,15,25,35,45,55];
  }
}
