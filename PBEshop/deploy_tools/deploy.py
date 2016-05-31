import os
import random
from optparse import OptionParser

REPO_URL = 'https://lgajownik@bitbucket.org/lgajownik/tdd.git'
USER_NAME = 'lukasz-gajownik'
PROJECT_NAME = 'PBEshop'
PYTHON_VERSION='3.5'

def deploy(user=USER_NAME,repo=REPO_URL, project=PROJECT_NAME, python_version=PYTHON_VERSION):
    file_abspath = os.path.abspath(__file__)
    domain_folder = os.path.dirname(file_abspath)
    site_folder = '%s/public_python' % (domain_folder)
    domain_name = os.path.basename(domain_folder)
    virtualenv_folder = '/home/%s/.virtualenvs/%s' % (user, domain_name)

    print('file_abspath: ' + file_abspath)
    print('domain_folder: ' + domain_folder)
    print('site_folder: ' + site_folder)
    print('domain_name: ' + domain_name)
    print('virtualenv_folder: ' + virtualenv_folder)
    print('repo: ' + repo)
    print('user: ' + user)

    _create_site_folder_if_neccessary(site_folder)
    _get_latest_source(site_folder, repo)
    _create_directory_structure_if_necessary(site_folder)
    _update_virtualenv(site_folder, virtualenv_folder, domain_name, user, python_version)
    _update_settings(site_folder, project, domain_name)
    _update_static_files(site_folder, virtualenv_folder, python_version)
    _update_database(site_folder, virtualenv_folder, python_version)

def _create_site_folder_if_neccessary(site_folder):
    print('_create_site_folder_if_neccessary')
    if not os.path.exists(site_folder):
        _execude_command('mkdir -p %s' % (site_folder))

def _get_latest_source(site_folder, repo):
    print('_get_latest_source')
    if not os.path.exists(site_folder + '/.git'):
        _execude_command('rm -rf %s' % (site_folder))
        _execude_command('git clone %s %s' % (repo, site_folder))
    else:
        _execude_command('cd %s && git fetch' % (site_folder))
    _execude_command('cd %s' % (site_folder))
    current_commit = os.popen('git log -n 1 --format=%H').read()
    _execude_command('cd %s && git reset --hard %s' % (site_folder, current_commit))

def _create_directory_structure_if_necessary(site_folder):
    print('_create_directory_structure_if_necessary')
    for subfolder in ('public', '../database', 'public/static', 'public/media'):
        if not os.path.exists('%s/%s' % (site_folder, subfolder)):
            _execude_command('mkdir -p %s/%s' % (site_folder, subfolder))

def _update_virtualenv(site_folder, virtualenv_folder, domain_name, user, python_version):
    print('_update_virtualenv')
    if not os.path.exists(virtualenv_folder):
        _execude_command('cd /home/%s/.virtualenvs && virtualenv %s -p /usr/local/bin/python%s' % (user, domain_name,python_version))
    _execude_command('%s/bin/pip%s install -r %s/requirements.txt' % (
        virtualenv_folder, python_version, site_folder
    ))

def _update_settings(site_folder, project, domain_name):
    print('_update_settings')
    settings_path = site_folder + '/%s/settings.py' % (project)
    _inplace_change(settings_path, "DEBUG = True", "DEBUG = False")
    _inplace_change(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (domain_name,)
    )
    secret_key_file = site_folder + '/%s/secret_key.py' % (project)
    if not os.path.exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        _append_to_file(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    _append_to_file(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_static_files(site_folder, virtualenv_folder, python_version):
    print('_update_static_files')
    _execude_command('cd %s && %s/bin/python%s manage.py collectstatic --noinput' % (
        site_folder, virtualenv_folder, python_version
    ))

def _update_database(site_folder, virtualenv_folder, python_version):
    print('_update_database')
    _execude_command('cd %s && %s/bin/python%s manage.py migrate --noinput' % (
        site_folder, virtualenv_folder, python_version
    ))

def _execude_command(command):
    print('Execute: %s' % (command))
    os.system(command)

def _inplace_change(filename, old_string, new_string):
    s = open(filename).read()
    if old_string in s:
        s = s.replace(old_string, new_string)
        f = open(filename, 'w')
        f.write(s)
        f.flush()
        f.close()

def _append_to_file(filename, text):
    with open(filename, "a") as myfile:
        myfile.write(text)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--user",
                  action="store", dest="user", type='string', default=USER_NAME,
                  help="Username on server")
    parser.add_option("--repo",
                  action="store", dest="repo", type='string', default=REPO_URL,
                  help="Repository url (http://repo/file/path.git")
    parser.add_option("--project",
                  action="store", dest="project", type='string', default=REPO_URL,
                  help="Django project name")
    parser.add_option("--python_version",
                      action="store", dest="python_version", type='string', default='3.5',
                      help="Python version (default 3.5)")

    options, args = parser.parse_args()

    deploy(user=options.user, repo=options.repo, project=options.project, python_version=options.python_version)