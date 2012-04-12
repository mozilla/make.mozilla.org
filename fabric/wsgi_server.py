from fabric.api import task

@task
def restart():
    """Currently a no-op until I figure out if mod_wsgi notices changes or not"""
    pass

