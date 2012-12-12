from fabric.api import task, cd, env, run, local, cd, lcd, put, settings, execute
from fabric.operations import sudo
import uuid, StringIO
from release import local_settings_path


@task
def setup():
    with settings(user=env.puppet_user):
        sudo('apt-get update')
        sudo('apt-get install puppet')
    execute(facts)


@task
def apply():
    with settings(user=env.puppet_user):
        tarball_path = '/tmp/make-moz-%s.tar.gz' % uuid.uuid4().hex
        with lcd('puppet'):
            local('tar czf %s .' % tarball_path)
        put(tarball_path, tarball_path)
        local('rm %s' % tarball_path)
        sudo('rm -rf /etc/puppet/manifests')
        sudo('rm -rf /etc/puppet/files')
        sudo('rm -rf /etc/puppet/templates')
        with cd('/etc/puppet'):
            sudo('tar -xzf %s' % tarball_path)
        run('rm %s' % tarball_path)
        sudo('puppet -d /etc/puppet/manifests/dev.pp')


@task
def facts():
    with settings(user=env.puppet_user):
        import imp
        env_settings = imp.load_source('env_settings', local_settings_path())
        db_user = env_settings.DATABASES['default']['USER']
        db_pass = env_settings.DATABASES['default']['PASSWORD']
        facts = """require 'facter'

Facter.add("db_user") do 
  setcode do 
    "%s"
  end
end

Facter.add("db_pass") do
  setcode do
    "%s"
  end
end
""" % (db_user, db_pass)
        fact_io = StringIO.StringIO(facts)
        fact_tmp_path = '/tmp/make-moz-facts-%s.rb' % uuid.uuid4().hex
        fact_dir = '/var/lib/puppet/lib/facter'
        fact_path = '%s/make_moz_db.rb' % fact_dir
        put(fact_io, fact_tmp_path)
        sudo('mkdir -p %s' % fact_dir)
        sudo('mv %s %s' % (fact_tmp_path, fact_path))
        sudo('chown root:root %s' % fact_path)
        sudo('chmod 700 %s' % fact_path)
