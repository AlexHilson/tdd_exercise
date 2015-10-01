import random

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

REPO_URL = 'https://github.com/AlexHilson/tdd_exercises.git'

def deploy(site_name):
    site_folder = '/home/%s/sites/%s' % (env.user, site_name)
    source_folder = site_folder + '/superlists'
    _create_directory_if_necessary(site_folder)
    _get_latest_source(site_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(site_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _configure_nginx(site_folder, site_name)
    _configure_gunicorn(site_folder, site_name)


def _create_directory_if_necessary(site_folder):
    run('mkdir -p %s' % (site_folder))


def _get_latest_source(source_folder):
    if exists(source_folder):
        run('rm -r %s' % source_folder)
    run('git clone %s %s' % (REPO_URL, source_folder))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (site_name))
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):  #3
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')  #45


def _update_virtualenv(site_folder):
    virtualenv_folder = site_folder + '/virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder))
    run('%s/bin/pip install -r %s/requirements.txt' % (
        virtualenv_folder, site_folder))


def _update_static_files(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (
        source_folder))


def _update_database(source_folder):
    run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (
        source_folder))


def _configure_nginx(site_folder, site_name):
    config_file = '/etc/nginx/sites-available/%s' % (site_name)
    run('cp %s/deploy_tools/nginx.template.conf /tmp/%s' % (site_folder, site_name))
    sed('/tmp/%s' % (site_name), 'SITENAME', site_name)

    run('sudo rm %s' % (config_file))
    run('sudo rm /etc/nginx/sites-enabled/%s' % (site_name))
    run('sudo mv /tmp/%s %s' % (site_name, config_file))
    run('sudo ln -s %s /etc/nginx/sites-enabled/%s' % (config_file, site_name))
    run('sudo service nginx restart')
    
    
def _configure_gunicorn(site_folder, site_name):
    config_file = '/etc/init/gunicorn-%s.conf' % (site_name)
    run('cp %s/deploy_tools/gunicorn-upstart.template.conf /tmp/%s' % (site_folder, site_name))
    sed('/tmp/%s' % (site_name), 'SITENAME', site_name)
    run('sudo mv /tmp/%s %s' % (site_name, config_file))
    run('sudo start gunicorn-%s' % (site_name))