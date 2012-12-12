from fabric.api import task, cd, run
from release import latest_release_path


@task
def restart():
    with cd(latest_release_path()):
        run('touch wsgi/playdoh.wsgi')
