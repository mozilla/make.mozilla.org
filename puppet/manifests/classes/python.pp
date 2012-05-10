# Install python
class pil_dependencies {
  package {
    ["libfreetype6-dev", "libjpeg62-dev"]:
      ensure => installed;
  }
}

class python {
  package {
    ["python2.6-dev", "python2.6", "libapache2-mod-wsgi", "python-wsgi-intercept", "python-pip", "python-virtualenv"]:
      ensure => installed;
  }
  include pil_dependencies
}
