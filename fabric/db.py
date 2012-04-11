from fabric.api import task, cd, env, run
from fabric.operations import sudo

@task
def noop():
    print "NADA"
