# Create the bare DB, set up the basic app install path

class app {
  require app_users
  
  exec { 'create_db_user':
    command => "createuser -D -R -S ${db_user}",
    unless => "psql -U ${db_user} -l 2&>1 > /dev/null",
    require => Package['postgresql-client'];
  }

  exec { "create_db":
    command => "createdb -O ${db_user} -T template_postgis ${db}",
    unless  => "psql -l | awk '{ print $1 }' | grep '^${db}$'",
    require => Exec["create_db_user"];
  }
}
