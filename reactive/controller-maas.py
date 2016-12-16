from os import remove
import requests
from shutil import copyfile

from charms.reactive import when_not, hook, set_state
from charmhelpers.core.hookenv import status_set, charm_dir
from charmhelpers.core.host import service_restart


@when_not('controller-maas.installed')
def install():
    api_dir = requests.get('http://localhost:5000').json()['message']['api_dir']
    copyfile('{}/files/controller_maas.py'.format(charm_dir()), '{}/api/controller_maas.py'.format(api_dir))
    service_restart('sojobo-api')
    status_set('active', 'data copied')
    set_state('controller-maas.installed')


@hook('stop')
def remove_controller():
    api_dir = requests.get('http://localhost:5000').json()['message']['api_dir']
    remove('{}/api/controller_maas.py'.format(api_dir))
    service_restart('sojobo-api')
