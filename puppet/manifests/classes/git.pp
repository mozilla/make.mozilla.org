# ensure Git is installed

class git {
  package { "git-core":
    ensure => present,
  }
}
