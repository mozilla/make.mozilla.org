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

  file { "/var/lib/redis":
    ensure => directory,
    mode => '750', owner => $redis_user, group => $redis_group,
    require => Exec['create-redis-system-user'];
  }

  file { "/var/log/redis":
    ensure => directory,
    mode => '755', owner => $redis_user, group => $redis_group,
    require => Exec['create-redis-system-user'];
  }

  exec { "create-redis-system-group":
    command => "addgroup --system ${redis_group}",
    unless => "getent group ${redis_group}";
  }

  exec { "create-redis-system-user":
    command => "adduser --system --disabled-login --ingroup ${redis_group} --home /var/lib/redis --gecos \"${redis_group} server\" --shell /bin/false ${redis_user}",
    unless => "getent passwd ${redis_user}",
    require => Exec["create-redis-system-group"];
  }

  exec { "build-redis":
    cwd => $redis_src_dir,
    command => "make install",
    onlyif => "test \"`cat /etc/redis/puppet-ver`\" != \"$redis_sha1\"",
    require => [Exec["unpack-redis"], File['/var/lib/redis'], File['/etc/redis/redis.conf']],
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
}
