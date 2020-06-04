#!/usr/bin/env python3

import os
import re
import pathlib
import requests as reqs
from os.path import join, dirname
from dotenv import load_dotenv
import json
import string

dotenv_path = join(dirname(__file__), 'variables.env')
load_dotenv(dotenv_path)

access_token = os.environ.get('ACCESS_TOKEN')
headers = {'Authorization': str('Bearer ' + access_token)}
base_url = ''.join([os.environ.get('CANVAS_LMS_SERVER'), '/api/'])
api_version = 'v1/'

root_path = os.path.join(os.getcwd(), 'courses')

def main():

    url = base_url + api_version + 'courses'

    # get all courses
    courses_list = get_paginated(url)

    for course in courses_list:
        if 'name' in course.keys() and 'id' in course:
            print('Course: ' + course['name'])
            
            # get all modules and folders in each course
            course['folders'] = get_course_folders(course['name'], course['id'])
            course['modules'] = get_course_modules(course['name'], course['id'])

            # create module folder structure
            if course['modules']:
                for module in course['modules']:
                    if 'name' in module.keys():
                        print('\tModule: ' + module['name'])
                        module_path = os.path.join(root_path, format_filename(course['name']), 'modules', format_filename(module['name']))
                        make_folder(module_path)
                        # module['files'] = get_paginated(module['items_url'])
                        # for item in module_path['files']: 
                            # write_file(item[''], module_path)
            
            # create file folder structure
            if course['folders']:
                for folder in course['folders']:
                    if 'name' in folder.keys():
                        print('\tFolder: ' + folder['name'])
                        folder_path = os.path.join(root_path, format_filename(course['name']), 'files', format_filename(folder['name']))
                        make_folder(folder_path)
                        folder['files'] = get_paginated(folder['files_url'])
                        
                        for item in folder['files']:
                            filename = item['display_name']
                            if os.path.isfile(os.path.join(folder_path, filename)):
                                print ('\t\t File: skipping ' + filename + " already exists")
                            else:
                                print('\t\t File: ' + filename)
                                write_file(item['url'], folder_path, format_filename(filename))
    
                
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def get_course_folders(course_name, course_id):
    folders_url = base_url + api_version + 'courses/' + str(course_id) + '/folders'
    folders = get_paginated(folders_url)
    for folder in folders:
        folder['files'] = get_paginated(base_url + api_version + 'folders/' + str(folder['id']) + '/files')
    return folders

def get_course_modules(course_name, course_id):
    module_url = base_url + api_version + 'courses/' + str(course_id) + '/modules'
    modules = get_paginated(module_url)
    for module in modules:
        module['items'] = get_paginated(module_url + '/' + str(module['id']) + '/items')
    return modules


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

def check_response(response):
    # 1. Test if response body contains sth.
    if not response.text:
        return False

    # 2. Handle error if deserialization fails (because of no text or bad format)
    try:
        responses = response.json()
        # ...
    except ValueError:
        # no JSON returned
        return False

    # 3. check that .json() did NOT return an empty dict
    if not responses:
        return False

    return True

def get_paginated(url, page=None):
    if page == None:
        response = reqs.get(url, headers=headers)
        page = 1
    else:
        response = reqs.get(url, headers=headers, params={'page': page})
    
    if response.status_code == 200 and check_response(response):
        data = json.loads(response.text)
        return data + get_paginated(url, page=page+1)
    else:
        return list()

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