import os

from urllib.parse import urlencode
from datetime import datetime
from base64 import b64encode
from requests import request

import hashlib
import hmac
import json

def get_hostname(network):
    hostname = os.environ.get('LNMARKETS_API_HOSTNAME')
    
    if hostname:
        return hostname
    elif network == 'testnet':
        return 'api.testnet.lnmarkets.com'
    else:
        return 'api.lnmarkets.com'

class LNMarketsRest():
    def __init__(self, **options):
        self.key = options.get('key', os.getenv('LNMARKETS_API_KEY'))
        self.secret = options.get('secret', os.getenv('LNMARKETS_API_SECRET'))
        self.passphrase = options.get('passphrase', os.getenv('LNMARKETS_API_PASSPHRASE'))
        self.network = options.get('network', os.getenv('LNMARKETS_API_NETWORK', 'mainnet'))
        self.version = options.get('version', os.getenv('LNMARKETS_API_VERSION', 'v1'))
        self.hostname = get_hostname(self.network)
        self.custom_headers = options.get('custom_headers')
        self.full_response = options.get('full_response', False)
        self.debug = options.get('debug', False)
        self.skip_api_key = options.get('skip_api_key', False)
    
    def _request_options(self, **options):
        credentials = options.get('credentials')
        method = options.get('method')
        path = options.get('path')
        params = options.get('params')
        opts = { 'headers': { 'Content-Type': 'application/json' } }
  
        if self.custom_headers:
          opts['headers'].update(**self.custom_headers)

        if method in ['GET', 'DELETE']:
            data = urlencode(params)
        elif method in ['POST', 'PUT']:
            data = json.dumps(params, separators=(',', ':'))
            
        if credentials and not self.skip_api_key:
            if not self.key:
                'You need an API key to use an authenticated route'
            elif not self.secret:
                'You need an API secret to use an authenticated route'
            elif not self.passphrase:
                'You need an API passphrase to use an authenticated route'
            
            ts = str(int(datetime.now().timestamp() * 1000))

                     
            payload = ts + method + '/' + self.version + path + data
            hashed = hmac.new(bytes(self.secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).digest()
            signature = b64encode(hashed)
            
            opts['headers']['LNM-ACCESS-KEY'] = self.key
            opts['headers']['LNM-ACCESS-PASSPHRASE'] = self.passphrase
            opts['headers']['LNM-ACCESS-TIMESTAMP'] = ts
            opts['headers']['LNM-ACCESS-SIGNATURE'] = signature
        opts['ressource'] = 'https://' + self.hostname + '/' + self.version + path

        if method in ['GET', 'DELETE'] and params:
            opts['ressource'] += '?' + data
        return opts

    def request_api(self, method, path, params, credentials = False):
        options = {
          'method': method,
          'path': path,
          'params': params,
          'credentials': credentials
        }

        opts = self._request_options(**options)
        ressource = opts.get('ressource')
        headers = opts.get('headers')

        if method in ['GET', 'DELETE']:
            response = request(method, ressource, headers = headers)
        elif method in ['POST', 'PUT']:
            response = request(method, ressource, data = json.dumps(params, separators=(',', ':')), headers = headers)
        return response.text
    
    def before_request_api(self, method, path, params, credentials):
        return self.request_api(method, path, params, credentials)

    def futures_get_ticker(self):
        method = 'GET'
        path = '/futures/ticker'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def futures_new_position(self, params):
        method = 'POST'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_update_position(self, params):
        method = 'PUT'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_close_position(self, params):
        method = 'DELETE'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_close_all_positions(self):
        method = 'DELETE'
        path = '/futures/all/close'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def futures_cancel_position(self, params):
        method = 'POST'
        path = '/futures/cancel'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_cancel_all_positions(self):
        method = 'DELETE'
        path = '/futures/all/cancel'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def futures_cashin_position(self, params):
        method = 'POST'
        path = '/futures/cash-in'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_add_margin_position(self, params):
        method = 'POST'
        path = '/futures/add-margin'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_get_positions(self, params):
        method = 'GET'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_bid_offer_history(self, params):
        method = 'GET'
        path = '/futures/history/bid-offer'
        credentials = False

        return self.before_request_api(method, path, params, credentials)

    def futures_index_history(self, params):
        method = 'GET'
        path = '/futures/history/index'
        credentials = False

        return self.before_request_api(method, path, params, credentials)

    def futures_fixing_history(self, params):
        method = 'GET'
        path = '/futures/history/fixing'
        credentials = False

        return self.before_request_api(method, path, params, credentials)

    def futures_carry_fees_history(self, params):
        method = 'GET'
        path = '/futures/carry-fees'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def get_user(self):
        method = 'GET'
        path = '/user'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def update_user(self, params):
        method = 'PUT'
        path = '/user'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def deposit(self, params):
        method = 'POST'
        path = '/user/deposit'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def deposit_history(self, params):
        method = 'GET'
        path = '/user/deposit'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def withdraw(self, params):
        method = 'POST'
        path = '/user/withdraw'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def withdraw_history(self, params):
        method = 'GET'
        path = '/user/withdraw'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def app_configuration(self):
        method = 'GET'
        path = '/app/configuration'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def app_node(self):
        method = 'GET'
        path = '/app/node'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def get_leaderboard(self):
        method = 'GET'
        path = '/futures/leaderboard'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def get_announcements(self):
        method = 'GET'
        path = '/app/announcements'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def get_lnurl_auth(self):
        method = 'POST'
        path = '/lnurl/auth'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)

    def lnurlAuth(self, params):
        method = 'GET'
        path = '/lnurl/auth'
        credentials = False
        
        return self.before_request_api(method, path, params, credentials)
    
    def options_get_positions(self, params):
        method = 'GET'
        path = '/options/vanilla'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
        
    def options_new_position(self, params):
        method = 'POST'
        path = '/options/vanilla'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)

    def options_get_volatility(self):
        method = 'GET'
        path = '/options/volatility'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials)
    
    def options_get_configuration(self):
        method = 'GET'
        path = '/options/instrument'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials)
    
    def swap(self, params):
        method = 'POST'
        path = '/swap'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
    
    def swap_history(self, params):
        method = 'GET'
        path = '/swap'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)  
