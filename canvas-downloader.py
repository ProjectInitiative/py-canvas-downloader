#!/usr/bin/env python3

import os, re, pathlib, json, string, keyring, argparse
import requests as reqs
from os.path import join, dirname
from configparser import ConfigParser

from canvas import Canvas
from config import get_config

if os.name == 'nt':
    from keyring.backends import Windows
    keyring.set_keyring(Windows.WinVaultKeyring())

root_path = os.path.join(os.getcwd(), 'courses')
home = str(pathlib.Path.home())
config_file = os.path.join(home, '.config', 'canvas-downloader', 'config.ini')

def main():
    global root_path
    global home
    global config_file


    #TODO: add in the ability to add multiple servers
    parser = argparse.ArgumentParser(description='download data from a canvas server')
    parser.add_argument('--output', '-o',
                    dest='output_path',
                    help='output course files to specified directory')
    parser.add_argument('--nocache', '-n',
                    action='store_true',
                    help='run program with no cached data')
    parser.add_argument('--nomodules', '-m',
                    action='store_true',
                    help='run program without downloading modules')
    parser.add_argument('--nofiles', '-f',
                    action='store_true',
                    help='run program with downloading files and folders')
    parser.add_argument('--verbose', '-v',
                    action='store_true',
                    help='verbosely run program')
    

    options = parser.parse_args()
    if options.nocache:
        configs = get_config(cacheless=True)
    else:
        configs = get_config()

    if options.output_path != None:
        if os.path.isdir(options.output_path):
            root_path = os.path.join(os.path.abspath(options.output_path), 'courses')
        else:
            raise argparse.ArgumentTypeError(f"readable_dir:{options.output_path} is not a valid path")

    if options.nofiles and options.nomodules:
        exit(0)



    access_token = keyring.get_password('system', configs.get('main', 'server_name'))
    canvas = Canvas(configs.get('main', 'base_url'), access_token=access_token)

    # get all courses
    courses_list = canvas.get_courses()

    for course in courses_list:
        if 'name' in course.keys() and 'id' in course:
            print('Course: ' + course_name(course))

            # get all modules and folders in each course
            course['folders'] = canvas.get_course_folders(course['id'])
            course['modules'] = canvas.get_course_modules(course['id'])

            # create module folder structure
            if course['modules'] and not options.nomodules:
                for module in course['modules']:
                    if 'name' in module.keys():
                        print('\tModule: ' + module['name'])
                        module_path = os.path.join(root_path, format_filename(course_name(course)), 'modules', format_filename(module['name']))
                        make_folder(module_path)
                        module['items'] = canvas.get_module_items(module['items_url'])
                        # module['files'] = get_paginated(module['items_url'])
                        # for item in module_path['files']: 
                            # write_file(item[''], module_path)
            
            # create file folder structure
            if course['folders'] and not options.nofiles:
                for folder in course['folders']:
                    if 'name' in folder.keys():
                        print('\tFolder: ' + folder['name'])
                        folder_path = os.path.join(root_path, format_filename(course_name(course)), 'files', format_filename(folder['name']))
                        make_folder(folder_path)
                        folder['files'] = canvas.get_folder_files(folder['files_url'])
                        
                        for item in folder['files']:
                            filename = item['display_name']
                            if os.path.isfile(os.path.join(folder_path, format_filename(filename))):
                                if options.verbose:
                                    print ('\t\t File: skipping ' + filename + " already exists")
                            else:
                                if options.verbose:
                                    print('\t\t File: ' + filename)
                                write_file(item['url'], folder_path, format_filename(filename))
    

def course_name(course):
    name = course['original_name']
    if name == None:
        return course['name']
    return name


def make_folder(dir):
    try:
        pathlib.Path(dir).mkdir(parents=True, exist_ok=True)
    except OSError:
        print ('Creation of the directory %s failed' % dir)

def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.
 
    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.
    
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename\*?=([^;]+)', cd, flags=re.IGNORECASE)
    fname = fname[0].strip().strip('"')
    # fname = re.findall('filename=(.+)', cd)
    # fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname

def url_join(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))

def write_file(url, dir, filename):
    r = reqs.get(url, allow_redirects=True)
    # filename = get_filename_from_cd(r.headers.get('content-disposition'))
    open(os.path.join(str(dir), filename.replace('"','')), 'wb').write(r.content)

if __name__ == '__main__':
    main()