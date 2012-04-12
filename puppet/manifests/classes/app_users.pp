# 
# Extra un-privileged users
#

define app_user ( $ensure = present, $uid, $pgroup = users, $groups, $fullname, $home, $shell ) {
  # Grab the username from the resource name 
  $username = $name
  # define the user 
  user { $username:
    ensure => $ensure,
    uid => $uid,
    gid => $pgroup,
    groups => $groups,
    auth_membership => inclusive,
    comment => $fullname,
    home => "${home}",
    shell => $shell,
    allowdupe => false,
  }
}

define app_group ( $ensure = present, $gid ) {
  # make sure the group is there
  group { $name:
    ensure => $ensure,
    gid => $gid,
    name => $name,
    allowdupe => false,
  }
}

define app_dir ( $owner, $group, $mode = 750 ) {
  # Ensure the ownership and perms of the user home 
  file { $name:
    ensure => directory, 
    owner => $owner, group => $group, mode => $mode,
    require => [User[$owner], Group[$group]];
  }
}

class app_users {
  app_group { "wsgi":
    gid => "1100",
  }
  app_group { $app_user:
    gid => "1101",
  }
  app_user { $app_user:
    ensure => "present",
    uid => "1101",
    pgroup => $app_user,
    groups => ['wsgi'],
    fullname => "make.mozilla.org",
    home => $app_root,
    shell => "/bin/bash",
  }
  file { $all_apps_root:
    ensure => directory, 
    owner => "root", group => "root", mode => 755,
  }
  app_dir { $app_root:
    owner => $app_user,
    group => "wsgi"
  }
  file { "${app_root}/.ssh":
    ensure => directory,
    owner => $app_user, group => $app_user, mode => 700,
  }
  file { "${app_root}/.ssh/authorized_keys":
    ensure => present,
    owner => $app_user, group => $app_user, mode => 600,
    source => '/etc/puppet/files/deploy_keys',
    require => File["${app_root}/.ssh"];
  }
}
