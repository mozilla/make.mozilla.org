from fabric.api import task, cd, env, run, local, cd, lcd, put
from fabric.operations import sudo
import uuid

@task
def setup():
    sudo('apt-get update')
    sudo('apt-get install puppet')

@task
def apply():
    tarball_path = '/tmp/make-moz-%s.tar.gz' % uuid.uuid4().hex
    with lcd('puppet'):
        local('tar czf %s .' % tarball_path)
    put(tarball_path, tarball_path)
    local('rm %s' % tarball_path)
    sudo('rm -rf /etc/puppet/manifests')
    sudo('rm -rf /etc/puppet/files')
    with cd('/etc/puppet'):
        sudo('tar -xzf %s' % tarball_path)
    run('rm %s' % tarball_path)
    sudo('puppet /etc/puppet/manifests/dev.pp')



