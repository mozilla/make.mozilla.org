# Install python
class python {
  package {
    ["python2.6-dev", "python2.6", "libapache2-mod-wsgi", "python-wsgi-intercept", "python-pip", "python-virtualenv"]:
      ensure => installed;
  }
}
