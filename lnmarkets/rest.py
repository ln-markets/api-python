import os
import hashlib
import hmac
import json
import requests

from urllib.parse import urlencode
from datetime import datetime
from base64 import b64encode

from bech32 import bech32_decode, convertbits
from embit import bip39, bip32
from embit.ec import PrivateKey as EmbitPrivateKey
from binascii import unhexlify, hexlify


def lnurl_decode(lnurl: str) -> str:
    hrp, data = bech32_decode(lnurl)
    try:
        assert hrp
        assert data
    except:
        return None
    bech32_data = convertbits(data, 5, 8, False)
    try:
        assert bech32_data
    except:
        return None
    return bytes(bech32_data).decode()
    
    
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
        
        #  API key auth
        if 'mnemonic' not in options:
            self.key = options.get('key', os.getenv('LNMARKETS_API_KEY'))
            self.secret = options.get('secret', os.getenv('LNMARKETS_API_SECRET'))
            self.passphrase = options.get('passphrase', os.getenv('LNMARKETS_API_PASSPHRASE'))
            self.skip_api_key = options.get('skip_api_key', False)
            self.mnemonic = None
        
        # mnemonic auth
        else:
            self.mnemonic = options['mnemonic']
            self.skip_api_key = True
        
        self.network = options.get('network', os.getenv('LNMARKETS_API_NETWORK', 'mainnet'))
        self.version = options.get('version', os.getenv('LNMARKETS_API_VERSION', 'v2'))
        self.hostname = get_hostname(self.network)
        self.custom_headers = options.get('custom_headers')
        self.full_response = options.get('full_response', False)
        self.debug = options.get('debug', False)
        
        self.session = requests.Session()
        
        if self.mnemonic:
            self.mnemonic_auth()
            
    def renew_cookie(self):
        if self.mnemonic:
            self.logout()
            self.mnemonic_auth()
        
    def logout(self):
        ret = self.session.post(f"https://{self.hostname}/v2/user/logout").status_code
        if ret != 200:
            raise Exception("Cannot logout!")

    def mnemonic_auth(self):
        lnurl = None
        expected = None
        try:
            lnurl = lnurl_decode(self.session.post(f"https://{self.hostname}/v2/lnurl/auth", ).json()['lnurl'])
            
            k1_str = lnurl.split('&hmac=')[0].split('&k1=')[1]
            k1 = unhexlify(k1_str)
            hmac = lnurl.split('&hmac=')[1]
            
            domain = bytes(lnurl.split('//')[1].split('/')[0], 'utf-8')
            derivation = hashlib.sha256(domain).digest()
            
            seed = bip39.mnemonic_to_seed(self.mnemonic)
            root = bip32.HDKey.from_seed(seed).derive(derivation)
            prv: EmbitPrivateKey = root.key
            
            sig = str(prv.sign(k1))
            pub = str(root.to_public().key)
            
            lnurl = lnurl + '&sig=' + sig + '&key=' + pub
            expected = f'https://{self.hostname}/v2/lnurl/auth?tag=login&k1={k1_str}&hmac={hmac}&sig={sig}&key={pub}'
            if lnurl != expected:
                raise Exception("lnurl received don't follow expected pattern!")
            
            # get auth cookie
            ret = self.session.get(lnurl).json()
            
            if ret['status'] != 'OK' or ret['event'] != 'LOGGEDIN':
                raise Exception('Cannot auth using the seed!')
        
        except:
            print(f'lnurl    ={lnurl} ')
            print(f'expected ={expected} ')
            raise Exception('Cannot auth using the seed!')
    
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
            response = self.session.request(method, ressource, headers = headers)
        elif method in ['POST', 'PUT']:
            response = self.session.request(method, ressource, data = json.dumps(params, separators=(',', ':')), headers = headers)
        else:
            return

    def before_request_api(self, method, path, params, credentials):
        return self.request_api(method, path, params, credentials)

    ## Futures 
    
    def futures_add_margin(self, params):
        method = 'POST'
        path = '/futures/add-margin'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_cancel_all(self):
        method = 'DELETE'
        path = '/futures/all/cancel'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials)
    
    def futures_cancel(self, params):
        method = 'POST'
        path = '/futures/cancel'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def futures_cashin(self, params):
        method = 'POST'
        path = '/futures/cash-in'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def futures_close_all(self):
        method = 'DELETE'
        path = '/futures/all/close'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials)
    
    def futures_close(self, params):
        method = 'DELETE'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def futures_get_trades(self, params):
        method = 'GET'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def futures_new_trade(self, params):
        method = 'POST'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def futures_update_trade(self, params):
        method = 'PUT'
        path = '/futures'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    
    def futures_carry_fees(self, params):
        method = 'GET'
        path = '/futures/carry-fees'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def futures_fixing(self, params):
        method = 'GET'
        path = '/futures/history/fixing'
        credentials = False

        return self.before_request_api(method, path, params, credentials)
    

    def futures_index(self, params):
        method = 'GET'
        path = '/futures/history/index'
        credentials = False

        return self.before_request_api(method, path, params, credentials)
    
    def futures_get_leaderboard(self):
        method = 'GET'
        path = '/futures/leaderboard'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)
    
    def futures_get_market(self):
        method = 'GET'
        path = '/futures/market'
        credentials = False
        params = {}

        return self.before_request_api(method, path, params, credentials)
    
    def futures_get_price(self, params):
        method = 'GET'
        path = '/futures/history/price'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def futures_get_ticker(self):
        method = 'GET'
        path = '/futures/ticker'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials)

    
    def futures_get_trade(self, params):
        method = 'GET'
        trade_id = params.get('id')  
        path = f'/futures/trades/{trade_id}'
        credentials = False

        return self.before_request_api(method, path, params, credentials)

    


    ## Options
    
    def options_close_all(self):
        method = 'DELETE'
        path = '/options/close-all'
        credentials = True
        params = {}

        return self.before_request_api(method, path, params, credentials)

    
    def options_close(self, params):
        method = 'DELETE'
        path = '/options'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    

    def options_get_trades(self, params):
        method = 'GET'
        path = '/options'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
        
    
    def options_new_trade(self, params):
        method = 'POST'
        path = '/options'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
    
    def options_update_trade(self, params):
        method = 'PUT'
        path = '/options'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
    
    def options_get_trade(self, params):
        method = 'GET'
        trade_id = params.get('id')  
        path = f'/options/trades/{trade_id}'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
        
    def options_get_volatility(self):
        method = 'GET'
        path = '/options/volatility-index'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials)
    
    def options_get_instrument(self, params):
        method = 'GET'
        path = '/options/instrument'
        credentials = False
        
        return self.before_request_api(method, path, params, credentials)

    def options_get_instruments(self):
        method = 'GET'
        path = '/options/instruments'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials)    
    
    
    def options_get_market(self):
        method = 'GET'
        path = '/options/market'
        credentials = False
        params = {}
        
        return self.before_request_api(method, path, params, credentials)
    
    ## Swap

    def get_swaps(self, params):
        method = 'GET'
        path = '/swap'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)  
    
    def swap(self, params):
        method = 'POST'
        path = '/swap'
        credentials = True
        
        return self.before_request_api(method, path, params, credentials)
    

    ## User

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
    
    def get_new_bitcoin_address(self, params):
        method = 'POST'
        path = '/user/bitcoin/address'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def get_bitcoin_addresses(self):
        method = 'GET'
        path = '/user/bitcoin/address'
        credentials = True
        params={}

        return self.before_request_api(method, path, params, credentials)
    
    def get_deposit(self, params):
        method = 'GET'
        deposit_id = params.get('id')  
        path = f'/user/deposits/{deposit_id}'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def get_deposits(self, params):
        method = 'GET'
        path = '/user/deposit'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

    def new_deposit(self, params):
        method = 'POST'
        path = '/user/deposit'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def get_withdrawal(self, params):
        method = 'GET'
        withdrawal_id = params.get('id')  
        path = f'/user/withdrawals/{withdrawal_id}'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def get_withdrawals(self, params):
        method = 'GET'
        path = '/user/withdraw'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def new_withdraw(self, params):
        method = 'POST'
        path = '/user/withdraw'
        credentials = True

        return self.before_request_api(method, path, params, credentials)
    
    def new_internal_transfer(self, params):
        method = 'POST'
        path = '/user/transfer'
        credentials = True

        return self.before_request_api(method, path, params, credentials)

     ## Oracle
    
    def get_oracle_index(self, params):
        method = 'GET'
        path = '/oracle/index'
        credentials = False
        
        return self.before_request_api(method, path, params, credentials)
    
    def get_oracle_last(self, params):
        method = 'GET'
        path = '/oracle/last-price'
        credentials = False
        
        return self.before_request_api(method, path, params, credentials)
    

    ## Notifications

    def fetch_notifications(self):
        method = 'GET'
        path = '/user/notifications'
        credentials = True
        params = {}
        
        return self.before_request_api(method, path, params, credentials)
    
    def mark_notifications_read(self):
        method = 'PUT'
        path = '/user/notifications/all'
        credentials = True
        params = {}
        
        return self.before_request_api(method, path, params, credentials)
        
    ## App

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
    
   
        
