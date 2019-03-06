import random
from fabric.contrib.files import append, exists
from fabric.api import *
from fabric.network import ssh
import paramiko
import sys
import logging
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


env.use_ssh_config=False
ssh.util.log_to_file("C:/Users/Mikołaj/.ssh/paramiko.log", 10)



#env.ssh_config_path = 'C:/Users/Mikołaj/.ssh/config.py'

#REPO_URL = 'https://github.com/omn88.superlists.git'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("superlists-staging.dobririba.pl", username="mikiwro",allow_agent=True, look_for_keys=True, key_filename='C:/Users/Mikołaj/.ssh/id_rsa')




  

def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'  
    run(f'mkdir -p {site_folder}')  
    with cd(site_folder):  
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
		
def _get_latest_source():
    if exists('.git'):  
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} .')  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}')  

def _update_virtualenv():
    if not exists('goatvenv/bin/pip'):  
        run(f'python3.6 -m venv goatvenv')
    run('./virtualenv/bin/pip install -r requirements.txt')  
	
def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')  
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')  
    if 'DJANGO_SECRET_KEY' not in current_contents:  
        new_secret = ''.join(random.SystemRandom().choices(  
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')
		
def _update_static_files():
    run('./goatvenv/bin/python manage.py collectstatic --noinput')  

def _update_database():
    run('./goatvenv/bin/python manage.py migrate --noinput') 