import site, os, os.path
from fabric.api import task, env, execute

site.addsitedir(os.path.abspath('fabric'))

import db, release, puppet, wsgi_server
import fab_git as git


env.releases_path = '/var/webapps/make.mozilla.org'
env.repo_url = 'git://github.com/rossbruniges/make.mozilla.org.git'
env.forward_agent = True
env.puppet_user = env.user
env.user = 'make_mozilla'
hosts = {
    'dev': ['make.constituentparts.com'],
    'development': ['make-dev1.vm1.labs.sjc1.mozilla.com'],
    'production': ['make-prod1.vm.labs.scl3.mozilla.com'],
    'staging': []
}
env.deploy_env = os.getenv('TO', 'development')
env.hosts = hosts[env.deploy_env]

def perform_release(migrate = False, setup = False):
    execute(release.create)
    execute(release.symlink)
    if setup:
        execute(db.setup)
    if migrate:
        execute(db.migrate)
    execute(wsgi_server.restart)
    execute(release.prune_old)

@task
def deploy():
    perform_release()

@task
def deploy_with_migrations():
    perform_release(migrate = True)

@task
def setup():
    execute(release.initial_setup)
    execute(git.clone)

@task
def deploy_cold():
    execute(setup)
    perform_release(migrate = True, setup = True)

@task
def update_settings():
    release.put_updated_settings()
    execute(wsgi_server.restart)
