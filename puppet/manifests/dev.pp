#
# make.mozilla.org dev puppet stuff
#
import 'classes/*.pp'

$all_apps_root = '/var/webapps'
$app_root = '/var/webapps/make.mozilla.org'

# You can make these less generic if you like, but these are box-specific
# so it's not required.
$db = "make_mozilla"
$db_user = "mozilla"

Exec {
    path => "/usr/local/bin:/usr/bin:/usr/sbin:/sbin:/bin",
}

class dev {
  include postgresql
  include geo_django_deps
  include apache
  include app
}

include dev
