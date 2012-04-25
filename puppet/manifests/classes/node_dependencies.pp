define npm {
  # install node module with npm
  exec { "npm install $name -g":
    creates => "/usr/lib/node_modules/$name",
    require => Package['npm'];
  }
}

class node_dependencies {
  npm { "less": }
  npm { "uglify-js": }
}
