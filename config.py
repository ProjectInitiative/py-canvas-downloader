from configparser import ConfigParser
import pathlib, os, validators, keyring

def _prompt_base_url():
    while True:
        base_url = input('Please enter the base URL of the Canvas LMS server:: ')
        if not validators.url(base_url):
            print('URL not valid, please try again')
        else:
            return base_url

def _prompt_server_name():
    return input('Please enter a name for this Canvas LMS server:: ')

def _prompt_access_token():
    return input('Please enter you Canvas LMS access token:: ')

def get_config(cacheless=False):
    home = str(pathlib.Path.home())
    config_file = os.path.join(home,'.config','canvas-downloader','config.ini')

    if cacheless:
        if os.path.exists(config_file):
            os.remove(config_file)

    config = ConfigParser()
    config.read(config_file)


    if not config.has_section('main'):
        config.add_section('main')
    
    if not config.has_option('main', 'base_url'):
        config.set('main', 'base_url', _prompt_base_url())
    
    if not config.has_option('main', 'server_name'):
        server_name = _prompt_server_name()
        config.set('main', 'server_name', server_name)
        keyring.set_password('system', server_name, _prompt_access_token())

    if not os.path.isfile(config_file):
        directory = pathlib.Path(config_file).parent.absolute()
        if not os.path.exists(directory):
            os.makedirs(directory)
        open(config_file, 'w+').close()
    
    with open(config_file, 'w') as f:
        config.write(f)
    
    return config