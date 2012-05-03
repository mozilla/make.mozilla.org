define create_system_user ($group, $homedir, $shell = "/bin/false") {
  exec { "create-${group}-system-group":
    command => "addgroup --system ${group}",
    unless => "getent group ${group}";
  }

  exec { "create-${name}-system-user":
    command => "adduser --system --disabled-login --ingroup ${group} --home \"${homedir}\" --gecos \"${group} server\" --shell \"${shell}\" ${name}",
    unless => "getent passwd ${name}",
    require => Exec["create-${group}-system-group"];
  }

  file { $homedir:
    ensure => directory,
    mode => '755', owner => $name, group => $group,
    require => Exec["create-$name-system-user"];
  }
}

class redis {
  $redis_version = "2.4.12"
  $redis_sha1 = "dbdcf631aec2caa9ff427fc07b1bf2c57cebb11b"
  $redis_tarball = "redis-${redis_version}.tar.gz"
  $redis_url = "http://redis.googlecode.com/files/${redis_tarball}"
  $redis_tmp_dir = "/tmp/redis-build"
  $redis_tarball_path = "${redis_tmp_dir}/${redis_tarball}"
  $redis_src_dir = "${redis_tmp_dir}/redis-${redis_version}"
  $redis_bin_path = "/usr/local/bin/redis"
  $redis_user = "redis"
  $redis_group = "redis"
  $redis_home_dir = "/var/lib/redis"
  
  file { $redis_tmp_dir:
    ensure => directory;
  }

  exec { "download-redis":
    command => "wget ${redis_url} -O ${redis_tarball_path}",
    creates => $redis_tarball_path,
    require => File[$redis_tmp_dir];
  }

  exec { "clean-redis":
    command => "rm -rf ${redis_tmp_dir}/redis-${redis_version}",
    before => Exec["unpack-redis"];
  }

  exec { "check-redis-sha1":
    command => "[ `sha1sum ${redis_tarball_path} | awk '{ print \$1 }'` = \"${redis_sha1}\" ]",
    require => Exec["download-redis"];
  }

  exec { "unpack-redis":
    command => "tar -xzvf ${redis_tarball_path}",
    cwd => $redis_tmp_dir,
    require => [Exec["check-redis-sha1"], Exec["download-redis"]];
  }

  file { "/etc/redis/redis.conf":
    mode => '755', owner => 'root', group => 'root',
    source => "/etc/puppet/files/redis/redis.conf";
  }

  file { "/etc/redis/puppet-ver":
    mode => '755', owner => 'root', group => 'root',
    content => $redis_sha1;
  }

  file { "/var/log/redis":
    ensure => directory,
    mode => '755', owner => $redis_user, group => $redis_group,
    require => Create_system_user[$redis_user];
  }

  create_system_user { $redis_user:
    group => $redis_group,
    homedir => $redis_home_dir;
  }

  exec { "build-redis":
    cwd => $redis_src_dir,
    command => "make install",
    onlyif => "test \"`cat /etc/redis/puppet-ver`\" != \"$redis_sha1\"",
    require => [Exec["unpack-redis"], File['/etc/redis/redis.conf'], Create_system_user[$redis_user]],
    before => File['/etc/redis/puppet-ver'];
  }

  file { "/etc/init.d/redis-server":
    mode => '755', owner => 'root', group => 'root',
    source => '/etc/puppet/files/redis/redis-server.init',
    require => Exec["build-redis"];
  }

  service { "redis-server":
    ensure => running,
    enable => true,
    hasstatus => true,
    require => [File['/etc/init.d/redis-server'], File['/var/log/redis']];
  }

  file { "/var/lib/funfact":
    content => $::my_fun_fact;
  }
}
