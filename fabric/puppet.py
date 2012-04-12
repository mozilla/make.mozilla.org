from fabric.api import task, cd, env, run, local, cd, lcd, put, settings
from fabric.operations import sudo
import uuid

@task
def setup():
    with settings(user = env.puppet_user):
        sudo('apt-get update')
        sudo('apt-get install puppet')

@task
def apply():
    with settings(user = env.puppet_user):
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
        sudo('puppet -d /etc/puppet/manifests/dev.pp')



