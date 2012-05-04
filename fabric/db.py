from fabric.api import task, cd, env, run, execute
from fabric.operations import sudo

from release import latest_release_path, virtualenv_python_path

@task
def migrate():
    execute(setup)
    with cd(latest_release_path()):
        run('%s manage.py migrate' % virtualenv_python_path())

def setup():
    with cd(latest_release_path()):
        run('%s manage.py syncdb' % virtualenv_python_path())

