# Create the bare DB, set up the basic app install path

class app {
  require app_users

  exec { 'create_db_user':
    command => "sudo -u postgres createuser -D -R -S ${app_user}",
    unless => "sudo -u $app_user psql -l",
    logoutput => true,
    require => [Class['postgis'], Package['postgresql-client']];
  }

  exec { "create_db":
    command => "sudo -u postgres createdb -O ${app_user} -T template_postgis ${db}",
    unless  => "sudo -u postgres psql -l | awk '{ print \$1 }' | grep '^${db}$'",
    logoutput => true,
    require => [Class['postgis'], Exec["create_db_user"]];
  }

  exec { "create_virtualenv":
    command => "sudo -u ${app_user} virtualenv --no-site-packages ${app_root}/virtualenv",
    onlyif => 'test ! -e ${app_root}/virtualenv/bin/python',
    require => [Class['python'], File[$app_root], User[$app_user]];
  }
}
