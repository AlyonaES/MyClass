
# SafeConfigParser is a class
from ConfigParser import SafeConfigParser
import os
import json
import requests
import time
import sys

#to pars our config file we create class Config
class Config:
    def __init__(self):
        #here we create object of class SafeConfigParser
        self.parser = SafeConfigParser()
        if os.path.isfile('config.ini'):
            self.parser.read('config.ini')
        else:
            print('No config.ini found under root folder.')
            # shut down python
            sys.exit()

        # SOZDAEM INSTANCE CLASA PARSER I ZADAEM IH CHEREZ PEREMENNIE, CHTOBI POLUCHIT' DOSTUP K METODAM I ATTRIBUTAM ETOGO KLASSA
        self.domain = self.parser.get('Server', 'domain')
        self.admin_login = self.parser.get('Server', 'admin')
        self.password = self.parser.get('Server', 'password')
        self.test_path = self.parser.get('Server', 'test_path')
f = Config()
print(f.admin_login)

#
class Response:
    def __init__(self):
        self.http_code = None
        # tut mi sozdaem object classa dict, json eto prosto chast' imeni, moget bit luboe: self.body = dict()
        self.json = dict()
        self.headers = dict()

class Calls:
    def __init__(self):
        self.config = Config()
        # esli net json, on vidast strochku 'noJson'
        self.no_json = 'noJson'

    def create_folder(self, folder_name, domain= None, username=None, password=None, content_type=None, accept=None, method=None, test_path = None):
        if domain is None:
            #berem iz config
            domain = self.config.domain
        if content_type is None:
            content_type = 'application/json'
        if username is None:
            username = self.config.admin_login
        if password is None:
            password = self.config.password
        if method is None:
            method = 'POST'
        if accept is None:
            accept = 'application/json'
        if test_path is None:
            test_path = '/Shared/smoke_test/'

        endpoint = '/public-api/v1/fs/'
        url = domain + endpoint + test_path + folder_name
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = accept
        # eto body:
        data = dict()
        data['action'] = 'add_folder'
        # transform python v json
        data = json.dumps(data)


        # Python sdelaet request s zadannimi parametrami i zapishet resultat, poluchenniy s servere v object r
        #r = response. request method returns response
        r = requests.request(
            url = url,
            auth = (username, password),
            headers = headers,
            data = data,
            method = method)
        # ? CHTO MI DELAEM V ETOM TRY/EXCEPT:
        try:
            json_resp = json.loads(r.content)
        except ValueError:
            if method == 'OPTIONS':
                json_resp = r.content
            else:
                json_resp = self.no_json
        # ? CHTO DELAET SLEDUYUSHAYA STROKA:
        r.json = json_resp
        response = Response()
        response.http_code = r.status_code
        # ? CHTO DELAET SLEDUYUSHAYA STROKA(OTKUDA/ZACHEM JSON?):
        response.json = r.json
        response.headers = r.headers
        return response

    # ? ZACHEM NAM ETOT RANDOM NAME> PROSTO CHTOBI NAZIVAT' SOZDAVAEMAI PAPKI? NUGNA LI NAM ETA FUNCTION V DELETE METHOD, KOTORIY MI V KONTSE SDELALI?
    @staticmethod
    def get_random_name():
        return 'dynamic_name_%s' % str(time.time()).replace('.', '')

    def delete_folder(self, folder_name, domain= None, username=None, password=None, content_type=None, accept=None, method=None, test_path = None):
            if domain is None:
                #berem iz config
                domain = self.config.domain
            if content_type is None:
                content_type = 'application/json'
            if username is None:
                username = self.config.admin_login
            if password is None:
                password = self.config.password
            if method is None:
                method = 'DELETE'
            if accept is None:
                accept = 'application/json'
            if test_path is None:
                test_path = '/Shared/smoke_test/'

            endpoint = '/public-api/v1/fs/'
            url = domain + endpoint + test_path + folder_name
            headers = dict()
            headers['Content-Type'] = 'application/json'
            headers['Accept'] = accept



            # Python sdelaet request s zadannimi parametrami i zapishet resultat, poluchenniy s servere v object r
            r = requests.request(
                url = url,
                auth = (username, password),
                headers = headers,
                method = method
        )
            try:
                json_resp = json.loads(r.content)
            except ValueError:
                if method == 'OPTIONS':
                    json_resp = r.content
                else:
                    json_resp = self.no_json

            r.json = json_resp
            response = Response()
            response.http_code = r.status_code
            response.json = r.json
            response.headers = r.headers
            return response
