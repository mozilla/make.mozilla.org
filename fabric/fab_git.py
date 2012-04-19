import time
from fabric.api import task, cd, env, run, execute, local
from fabric.operations import sudo

@task
def tag():
    if not ('release_git_tag' in env):
        create_tag_name()
    local('git tag %s' % env.release_git_tag)
    local('git push --tags')

@task
def clone():
    repo_path = '%s/repo' % env.releases_path

    run('rm -rf %s' % repo_path)
    run('git clone %s %s' % (env.repo_url, repo_path))

    with cd(repo_path):
        run('git submodule update --init --recursive')

@task
def update():
    execute(tag)
    with cd('%s/repo' % env.releases_path):
        run('git reset --hard && git fetch --tags')
        run('git checkout %s' % env.release_git_tag)
        run('git submodule update --init --recursive')

def local_commit_sha1():
    sha1 = local("git log -n1 --oneline | awk '{ print $1 }'", capture = True)
    return sha1

def create_tag_name():
    time_portion = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    env.release_git_tag = '%s-%s' % (time_portion, local_commit_sha1())

