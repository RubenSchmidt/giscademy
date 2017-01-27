from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['ec2-52-214-159-209.eu-west-1.compute.amazonaws.com']
env.user = 'ubuntu'
env.shell = "/bin/bash -l -i -c"
env.venv = 'giscademy'
env.masterbranch = 'master'


def pull_latest():
    if confirm("You are about to pull the branch {}. Do you want to continue?".format(env.masterbranch)):
        run("git checkout {}".format(env.masterbranch))
        run("git reset --hard")
        run("git pull")


def collect_staticfiles():
    run('./manage.py collectstatic --no-input')


def install_requirements():
    run('pip install -r requirements.txt')


def migrate():
    run('./manage.py migrate')


def restart_uwsgi():
    sudo('service uwsgi restart')


def deploy():
    with cd('/home/ubuntu/giscademy'), prefix('workon {}'.format(env.venv)):
        pull_latest()
        install_requirements()
        migrate()
        collect_staticfiles()
        restart_uwsgi()
