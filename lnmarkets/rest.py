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
        self.version = options.get('version', os.getenv('LNMARKETS_API_VERSION', 'v2'))
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

    def request_api(self, method, path, params, credentials = False, format='text'):
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
        
        if format == 'json':
            return response.json()
        elif format is None:
            return response
        else:
            return response.text
    
    def before_request_api(self, method, path, params, credentials, format='text'):
        return self.request_api(method, path, params, credentials, format)

    
    ## Futures 
    
    def futures_add_margin_position(self, params, format='text'):
        method = 'POST'
        path = '/futures/add-margin'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)

    def futures_cancel_all_positions(self, format='text'):
        method = 'DELETE'
        path = '/futures/all/cancel'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials, format)

    def futures_close_all_positions(self, format='text'):
        method = 'DELETE'
        path = '/futures/all/close'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials, format)
    
    def futures_cancel_position(self, params, format='text'):
        method = 'POST'
        path = '/futures/cancel'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)

    def futures_carry_fees_history(self, params, format='text'):
        method = 'GET'
        path = '/futures/carry-fees'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    
    def futures_cashin_position(self, params, format='text'):
        method = 'POST'
        path = '/futures/cash-in'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    def futures_close_position(self, params, format='text'):
        method = 'DELETE'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)

    def futures_get_positions(self, params, format='text'):
        method = 'GET'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    def futures_new_position(self, params, format='text'):
        method = 'POST'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    def futures_update_position(self, params, format='text'):
        method = 'PUT'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
        
    def futures_fixing_history(self, params, format='text'):
        method = 'GET'
        path = '/futures/history/fixing'
        credentials = False

        return self.before_request_api(method, path, params, credentials, format)

    def futures_index_history(self, params, format='text'):
        method = 'GET'
        path = '/futures/history/index'
        credentials = False

        return self.before_request_api(method, path, params, credentials, format)
    
    def futures_price_history(self, params, format='text'):
        method = 'GET'
        path = '/futures/history/price'
        credentials = False

        return self.before_request_api(method, path, params, credentials, format)
    
    def futures_get_ticker(self, format='text'):
        method = 'GET'
        path = '/futures/ticker'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials, format)

    ## Options

    def options_get_expiries(self, format='text'):
        method = 'GET'
        path = '/options/instrument/expiry'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials, format)    
    
    def options_get_configuration(self, format='text'):
        method = 'GET'
        path = '/options/instrument'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials, format)
    
    def options_close_all_positions(self, format='text'):
        method = 'DELETE'
        path = '/options/vanilla/all'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials, format)
    
    def options_close_position(self, params, format='text'):
        method = 'DELETE'
        path = '/options/vanilla'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)

    def options_get_positions(self, params, format='text'):
        method = 'GET'
        path = '/options/vanilla'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials, format)
        
    def options_new_position(self, params, format='text'):
        method = 'POST'
        path = '/options/vanilla'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials, format)

    def options_update_position(self, params, format='text'):
        method = 'PUT'
        path = '/options/vanilla'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials, format)
    
    def options_get_volatility(self, params, format='text'):
        method = 'GET'
        path = '/options/volatility'
        credentials = False
        
        return self.before_request_api(method, path, params, credentials, format)
    

    ## User
    
    def deposit_history(self, params, format='text'):
        method = 'GET'
        path = '/user/deposit'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    def deposit(self, params, format='text'):
        method = 'POST'
        path = '/user/deposit'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    def get_user(self, format='text'):
        method = 'GET'
        path = '/user'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials, format)

    def update_user(self, params, format='text'):
        method = 'PUT'
        path = '/user'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)

    def get_notifications(self, format='text'):
        method = 'GET'
        path = '/user/notifications'
        credentials = True
        params = {}
        
        return self.before_request_api(method, path, params, credentials, format)
    
    def mark_all_notifications_read(self, format='text'):
        method = 'PUT'
        path = '/user/notifications/all'
        credentials = True
        params = {}
        
        return self.before_request_api(method, path, params, credentials, format)
    
    def mark_notifications_read(self, format='text'):
        method = 'PUT'
        path = '/user/notifications'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials, format)
    
    def withdraw_history(self, params, format='text'):
        method = 'GET'
        path = '/user/withdraw'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)
    
    def withdraw(self, params, format='text'):
        method = 'POST'
        path = '/user/withdraw'
        credentials = True

        return self.before_request_api(method, path, params, credentials, format)

    ## Swap
    
    def swap(self, params, format='text'):
        method = 'POST'
        path = '/swap'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials, format)
    
    def swap_history(self, params, format='text'):
        method = 'GET'
        path = '/swap'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials, format)  
    
    ## App

    def app_configuration(self, format='text'):
        method = 'GET'
        path = '/app/configuration'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials, format)

    def app_node(self, format='text'):
        method = 'GET'
        path = '/app/node'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials, format)

    def get_leaderboard(self, format='text'):
        method = 'GET'
        path = '/futures/leaderboard'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials, format)
    
    ## Oracle
    
    def get_oracle(self, params, format='text'):
        method = 'GET'
        path = '/oracle/index'
        credentials = False
        
        return self.before_request_api(method, path, params, credentials, format)
