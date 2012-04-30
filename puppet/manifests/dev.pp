#
# make.mozilla.org dev puppet stuff
#
import 'classes/*.pp'

$all_apps_root = '/var/webapps'
$app_root = '/var/webapps/make.mozilla.org'
$app_user = 'make_mozilla'
$db = "make_mozilla"

Exec {
    path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {
  include git
  include postgresql
  include python
  include geo_django_deps
  include postgis
  include apache
  include app_dependencies
  include app
  include nodejs
  include node_dependencies
  include redis
}

include dev
