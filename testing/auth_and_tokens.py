from keystone_plugin.testing.base import TestKeystoneBase
import requests

class TestKeystoneAuthAndTokens(TestKeystoneBase):
    #requires domain, role and user be created in given order

    def setUp(self):
        super(TestKeystoneAuthAndTokens, self).setUp()
        self.url = self.host + '/v3/auth/'
        self.auth = ''
        self.token = ''
        self.user_id = '62260c42-4ccb-41ec-a631-998bfb0119d4'

    def password_unscoped(self):
        body = {
            'auth' : {
                'identity' : {
                    'methods' : [ 'password' ],
                    'password' : {
                        'user' : {
                            # 'name' : 'admin',
                            # 'domain' : {
                            #     'name' : 'Default'
                            # },
                            'id' : self.user_id,
                            'password' : 'myadminpass'
                        }
                    }
                }
            }
        }
        self.res = requests.post(self.url + 'tokens', json = body)
        self.checkCode(201)
        self.auth = self.res.headers['X-Subject-Token']

    def token_scoped(self):
        body = {
            'auth' : {
                'identity' : {
                    'methods' : [ 'token' ],
                    'token' : {
                        'id' : self.auth
                    }
                },
                'scope' : {
                    'domain' : {
                        'name' : 'Default'
                    }
                }
            }
        }
        self.res = requests.post(self.url + 'tokens', json = body)
        self.checkCode(201)
        self.token = self.res.headers['X-Subject-Token']

    def get_catalog(self):
        self.password_unscoped()
        headers = {
            "X-Auth-Token" : self.auth
        }
        self.res = requests.get(self.url + 'catalog', headers=headers)
        self.checkCode(200)

    def get_token(self):
        self.password_unscoped()
        # self.token_scoped()
        headers = {
            "X-Auth-Token" : self.auth,
            "X-Subject-Token": self.auth
        }
        self.res = requests.get(self.url + 'tokens', headers = headers)
        self.checkCode(200)

    def get_scopes(self):
        self.password_unscoped()
        headers = {
            "X-Auth-Token" : self.auth
        }
        self.res = requests.get(self.url + 'domains', headers = headers)
        self.checkCode(200)
