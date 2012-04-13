from fabric.api import task, cd, run
from release import latest_release_path

@task
def restart():
    """Currently a no-op until I figure out if mod_wsgi notices changes or not"""
    with cd(latest_release_path()):
        run('touch wsgi/playdoh.wsgi')

