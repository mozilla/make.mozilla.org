import time
from fabric.api import task, cd, env, run, execute, local, abort


@task
def tag():
    #  fabric deploys out of your current branch - so if you're looking to
    #  deploy to another server we'll stop you right here
    if not (local_branch_name() == env.deploy_branch):
        abort('You\'re not currently in the right branch - if you want to push'
            ' to %s you then jump into your local %s branch (you\'re currently '
            'in %s)' % (env.deploy_env, env.deploy_branch, local_branch_name()))
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


def local_branch_name():
    branch_name = local('git branch | grep "^*" | cut -d" " -f2', capture=True)
    return branch_name


def local_commit_sha1():
    sha1 = local("git log -n1 --oneline | awk '{ print $1 }'", capture=True)
    return sha1


def create_tag_name():
    time_portion = time.strftime("%Y%m%d%H%M%S", time.gmtime())
    env.release_git_tag = '%s-%s' % (time_portion, local_commit_sha1())
