import site, os, os.path
from fabric.api import task, env, execute

site.addsitedir(os.path.abspath('fabric'))

import db, git, release, puppet

env.releases_path = '/var/webapps/make.mozilla.org'
hosts = {
    'development': ['make.constituentparts.com'],
    'production': [],
    'staging': []
}
env.hosts = hosts[os.getenv('TO', 'development')]

def perform_release(migrate = False):
    execute(release.create)
    execute(release.symlink)
    if migrate:
        execute(db.migrate)
    execute(wsgi_server.restart)

def do_deployment(migrate = False):
    execute(git.update)
    perform_release(migrate)

@task
def deploy():
    do_deployment()

@task
def deploy_with_migrations():
    do_deployment()

@task
def setup():
    execute(release.initial_setup)
    execute(git.clone)

@task
def deploy_cold():
    execute(setup)
    perform_release(migrate = True)
