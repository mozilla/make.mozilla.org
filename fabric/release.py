from fabric.api import task, cd, env, run
from fabric.operations import sudo

@task
def initial_setup():
    with cd(env.releases_path):
        run('mkdir -p releases')
        run('mkdir -p shared')

@task
def symlink():
    symlink_release_path = '%s/current' % env.release_path
    run('ln -sf "%s" "%s"' % current_release(), symlink_release_path)
