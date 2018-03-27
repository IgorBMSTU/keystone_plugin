from keystone_plugin.testing.base import TestKeystoneBase
import requests

class TestKeystoneAuthAndTokens(TestKeystoneBase):
    #requires domain, role and user be created in given order

    def setUp(self):
        super(TestKeystoneAuthAndTokens, self).setUp()
        self.url = self.host + '/v3/auth/'
        self.token = ''
        self.user_id = 'ac74734b-c604-4ba4-ba53-b45f88655fee'
        self.admin_auth()

    def password_scoped(self):
        body = {
            'auth' : {
                'identity' : {
                    'methods' : [ 'password' ],
                    'password' : {
                        'user' : {
                            'name' : 'trustee',
                            'domain' : {
                                'name' : 'admin'
                            },
                            # 'id' : self.user_id,
                            'password' : 'myadminpass'
                        }
                    }
                },
                "scope" : {
                    "project": {
                        'id': 'faee67cd-59e8-4e32-85ab-1c128b627587'
                    }
                }
            }
        }
        self.res = requests.post(self.url + 'tokens', json = body)
        self.checkCode(201)
        self.auth = self.res.headers['X-Subject-Token']

    def trust_scoped(self):
        body = {
            'auth' : {
                'identity' : {
                    'methods' : ['token'],
                    'token' : {
                            # 'id' : self.user_id,
                            'id' : '18dfcb24-29a2-4328-a067-7ef0e3434423'
                    }
                },
                "scope" : {
                     "OS-TRUST:trust": {
                        "id": "41eb9cb6-9f26-4769-80ea-f6ba895a2eea"
                     }
                }
            }
        }
        self.res = requests.post(self.url + 'tokens', json = body)
        self.checkCode(201)
        self.auth = self.res.headers['X-Subject-Token']

    def token_scoped(self):
        # self.auth = 'gAAAAABalrIoWlY330c46LrdKOtcv_2Upai7C8CqlorqvxHAXQunpDjC-ETKPDS63eM0WKxDoozGr3MI0JbsCvM-0uxK_0p-fg=='
        body = {
            "auth": {
                # "scope": {
                #     "project": {
                #         "domain": {
                #             "name": "admin"
                #         },
                #         "name": "admin"
                #
                #     }
                # },
                # "scope" : "unscoped",
                "identity": {
                    "token": {
                        "id" : self.auth
                    },
                    "methods": [
                        "token"
                    ]
                }
            }
        }
        self.res = requests.post(self.url + 'tokens', json = body)
        self.checkCode(201)
        self.token = self.res.headers['X-Subject-Token']

    def get_catalog(self):
        self.res = requests.get(self.url + 'catalog', headers=self.headers)
        self.checkCode(200)

    def get_token(self):
        # subject token
        self.headers ['X-Subject-Token']= 'gAAAAABauna0Ieci81ZDc7eBTsEkXN7aofHlTWNXejFr_JzjHVJ-snC3SHPteGFIpCsuGfSdpx6BrMQH_PEHHSP3CY4QGv2P4nxyKCuUm7BJQgJcxLzlSu_U345Bv25B1OY1N85E51Or'
        # auth token
        self.headers ['X-Auth-Token']= 'gAAAAABauna0CaXqr93kxg8sm3moPrfi2MZVSC_2juzlIMdr6CsTyY24WpOTUyVkD2STm5p3Y6vk9LD80ue_4bG6EsLgxg2klYTuroNRfEY1I77Pt9aDD7SKk6tGqhUxHYT1OJ8hJ8HL'
        self.res = requests.get(self.url + 'tokens', headers = self.headers, params = {'nocatalog':''})
        self.checkCode(200)

    def get_scopes(self):
        headers = {
            "X-Auth-Token" : self.auth
        }
        self.res = requests.get(self.url + 'domains', headers = headers)
        self.checkCode(200)
