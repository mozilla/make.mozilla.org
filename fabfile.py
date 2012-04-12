import site, os, os.path
from fabric.api import task, env, execute

site.addsitedir(os.path.abspath('fabric'))

import db, git, release, puppet, wsgi_server

env.releases_path = '/var/webapps/make.mozilla.org'
env.repo_url = 'git://github.com/fidothe/make.mozilla.org.git'
env.puppet_user = env.user
env.user = 'mozilla'
hosts = {
    'development': ['make.constituentparts.com'],
    'production': [],
    'staging': []
}
env.hosts = hosts[os.getenv('TO', 'development')]

def perform_release(migrate = False, setup = False):
    execute(release.create)
    execute(release.symlink)
    if setup:
        execute(db.setup)
    if migrate:
        execute(db.migrate)
    execute(wsgi_server.restart)

@task
def deploy():
    perform_release()

@task
def deploy_with_migrations():
    perform_release()

@task
def setup():
    execute(release.initial_setup)
    execute(git.clone)

@task
def deploy_cold():
    # execute(setup)
    perform_release(migrate = True, setup = True)
