from fabric.api import task, cd, env, run, execute, put
from fabric.operations import sudo
import os, os.path
import fab_git as git

@task
def initial_setup():
    with cd(env.releases_path):
        run('mkdir -p releases')
        run('mkdir -p shared/settings')
        run('mkdir -p shared/partner_media')
        run('mkdir -p virtualenv')
    put_updated_settings()

@task
def symlink():
    symlink_release_path = '%s/current' % env.releases_path
    run('ln -nsf "%s" "%s"' % (latest_release_path(), symlink_release_path))

@task
def create():
    execute(git.update)
    copy_release_over()
    symlink_shared()
    run_pip_install(latest_release_path())
    compress_assets(latest_release_path())

@task
def prune_old():
    releases = release_list()
    if len(releases) > 5:
        old_releases = releases[0:-5]
        for old_release in old_releases:
            run('rm -rf %s' % release_path(old_release))

def put_updated_settings():
    with cd(env.releases_path):
        put(local_settings_path(), 'shared/settings/local.py')

def local_settings_path():
    path = 'make_mozilla/settings/%s.py' % env.deploy_env
    project_root_path = os.path.dirname(env.real_fabfile)
    if os.path.exists(path):
        return path
    else:
        return os.path.join(project_root_path, path)

def release_path(release_tag):
    return '%s/releases/%s' % (env.releases_path, release_tag)

def copy_release_over():
    repo_path = '%s/repo' % env.releases_path
    run('mkdir %s' % latest_release_path())
    run('tar -cf - -C %s . | tar -xpf - -C %s' % (repo_path, latest_release_path()))

def symlink_shared():
    shared_settings_path = '%s/shared/settings/local.py' % env.releases_path
    release_settings_path = '%s/make_mozilla/settings/local.py' % latest_release_path()
    run('ln -sf %s %s' % (shared_settings_path, release_settings_path))

def latest_release_path():
    if env.has_key('release_git_tag'):
        return release_path(env.release_git_tag)
    else:
        return release_path(release_list().pop())

def release_list():
    releases = [x.strip() for x in run('ls -1 %s' % release_path('')).split('\n')]
    releases.sort()
    return releases


def virtualenv_path():
    return '%s/virtualenv' % env.releases_path

def virtualenv_bin_path():
    return '%s/bin' % virtualenv_path()

def virtualenv_python_path():
    return '%s/python' % virtualenv_bin_path()

def virtualenv_pip_path():
    return '%s/pip' % virtualenv_bin_path()

def run_pip_install(release_path):
    with cd(release_path):
        run('%s install -r requirements/compiled.txt' % virtualenv_pip_path())

def compress_assets(release_path):
    with cd(release_path):
        run('%s manage.py compress_assets' % virtualenv_python_path())

