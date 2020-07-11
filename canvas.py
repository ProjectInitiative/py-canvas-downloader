#!/usr/bin/env python3

import re, pathlib, json, string, validators
import requests as reqs
from os.path import join, dirname
from base64 import b64encode


class Canvas:

    def __init__(self, base_url=None, **kwargs):
        if not validators.url(base_url):
            raise Exception('MalformedURLError','error URL malformed')
        if base_url[-1] != '/':
            self.base_url = ''.join([base_url,'/api/v1/'])
        else:
            self.base_url = ''.join([base_url,'api/v1/'])
        
        if not all (k in kwargs.keys() for k in ('username','password')):
            if not 'access_token' in kwargs.keys():
                raise NotImplementedError()
            else:
                self.access_token = kwargs['access_token']
                self.headers = {'Authorization': str(''.join(['Bearer ', self.access_token]))}
        else:
            self.username = kwargs['username']
            self.password = kwargs['password']
            basic_auth = b64encode(str.encode(''.join([str(self.username), ':', str(self.password)]))).decode("ascii")
            self.headers = {'Authorization': ''.join(['Basic ', str(basic_auth)])}

    def get_courses(self):
        courses_url = ''.join([self.base_url, 'courses/'])
        return self.get_paginated(courses_url)

    def get_course_folders(self, course_id):
        folders_url = ''.join([self.base_url, 'courses/', str(course_id), '/folders/'])
        folders = self.get_paginated(folders_url)
        for folder in folders:
            folder['files'] = self.get_paginated(''.join([str(folders_url), str(folder['id']), '/files']))
        return folders

    def get_folder_files(self, folder_url):
        return self.get_paginated(folder_url)

    def get_course_modules(self, course_id):
        module_url = ''.join([self.base_url, 'courses/', str(course_id), '/modules/'])
        modules = self.get_paginated(module_url)
        for module in modules:
            module['items'] = self.get_paginated(''.join([module_url, str(module['id']), '/items']))
        return modules

    def get_module_items(self, course_id):
        pass

    def get_paginated(self, url, page=None):
        if page == None:
            response = reqs.get(url, headers=self.headers)
            page = 1
        else:
            response = reqs.get(url, headers=self.headers, params={'page': page})
        
        if response.status_code == 200 and self.check_response(response):
            data = json.loads(response.text)
            return data + self.get_paginated(url, page=page+1)
        else:
            return list()
    
    def check_response(self, response):
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
        