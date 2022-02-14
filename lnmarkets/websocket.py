import websocket

from urllib.parse import urlencode
from datetime import datetime
from base64 import b64encode

import hashlib
import hmac
import json

import sys
import websocket
import threading
import ssl
from time import sleep


BASE_URL = 'wss://api.lnmarkets.com'
    
class LNMarketsWebsocket(object):
    _connection_attempt = 0
    _max_connection_attempts = 5
    is_open = threading.Event()
                
    def connect(self, base_url=None, api_key=None, api_secret=None, api_passphrase=None):
        '''Connect to LNM websockets'''
        print("----------- CONNECTING TO WS --------------")
        
        if not base_url:
            base_url = BASE_URL
        
        self.key = key
        self.secret = secret
        self.passphrase = passphrase
       
        self.is_authenticated = False
        self.is_connecting = threading.Event()
        self.__connect(base_url)
        
    def __connect(self, base_url):
        '''Connect to the websocket in a thread.'''
        if self._connection_attempt == self._max_connection_attempts:
            print("Max connection attempt limit reached")
            sys.exit(1)

        if self._connection_attempt > 0:
            sleep(1)

        self._connection_attempt += 1

        print("Starting thread")

        ssl_defaults = ssl.get_default_verify_paths()
        sslopt_ca_certs = {'ca_certs': ssl_defaults.cafile}
        self.ws = websocket.WebSocketApp(base_url,
                                         on_message=self.on_message,
                                         on_close=self.on_close,
                                         on_open=self.on_open,
                                         on_error=self.on_error,
                                         on_pong=self.on_pong,
                                         )
        self.is_connecting.set()
        self.wst = threading.Thread(
            target=lambda: self.ws.run_forever(ping_interval=10, ping_timeout=5))
        self.wst.daemon = True
        self.wst.start()

        print("Started WS thread")
        self.is_connecting.clear()
        self.is_open.set()
    
    
    def auth(self):
        timestamp = str(int(datetime.now().timestamp() * 1000))

        method = 'auth/api-key'
        payload = timestamp + method

        hashed = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).digest()
        signature = b64encode(hashed)

        params =  {'timestamp': timestamp,
                   'signature': signature.decode(),
                   'passphrase': passphrase,
                   'key': key}
        json_msg = json.dumps({
            'jsonrpc': '2.0',
            'method': method,
            'params': params})
        
        self.ws.send(json_msg)
        
    def sub_futures_bid_offer(self):
        msg = {'jsonrpc': '2.0',
               'method': 'subscribe',
               'params': ["futures/market/bid-offer"]
        }
        json_msg = json.dumps(msg)
        self.ws.send(json_msg)
        
    def sub_futures_index(self):
        msg = {'jsonrpc': '2.0',
               'method': 'subscribe',
               'params': ["futures/market/index"]
        }
        json_msg = json.dumps(msg)
        self.ws.send(json_msg)
    
    def sub_options_forwards(self):
        msg = {'jsonrpc': '2.0',
               'method': 'subscribe',
               'params': ["options/data/forwards"]
        }
        json_msg = json.dumps(msg)
        self.ws.send(json_msg)
        
    def sub_options_volcurve(self):
        msg = {'jsonrpc': '2.0',
               'method': 'subscribe',
               'params': ["options/data/volcurve"]
        }
        json_msg = json.dumps(msg)
        self.ws.send(json_msg)
    
    def sub_options_ordermap(self):
        msg = {'jsonrpc': '2.0',
               'method': 'subscribe',
               'params': ["options/data/ordermap"]
        }
        json_msg = json.dumps(msg)
        self.ws.send(json_msg)
    
    def exit(self):
        sys.exit(1)

    def on_pong(self, _arg1, _arg2):
        print("------------------- RECEIVED PONG -----------------")

    def on_ping(self):
        print("-------------------- RECEIVED PING ----------------")

    def on_close(self, _event, _event2):
        print("------------------- CLOSE WS -------------------")
        self.is_open.clear()

    def on_open(self, _event):
        '''This is where all the initialisation logic should be. If you don't subscribe to anything
        or don't authenticate to the session the WS will kick you out automatically after 10s.'''
        print("------------------- OPEN WS -------------------")
        if self.api_key and self.api_passphrase and self.api_secret:
            self.auth()

    def on_error(self, exception_obj, something_else):
        print("------------------- ERROR WS -------------------")
        print("{}".format(something_else))
        self.is_open.clear()

    def on_message(self, _msg, msg):
        print(msg)
        msg = json.loads(msg)
        t = msg["type"]
        data = msg["data"]
        if t == AUTHENTICATE:
            if data["message"] == "success":
                print("Authenticated Successfully!")
                self.is_authenticated = True
            else:
                print("Auth Unsuccessful: {}".format(data))
                self.is_authenticated = False
                self.__reset()

        elif t == ERROR:
            print("{}".format(msg["message"]))
        else:
            print("Unhandled type: {}".format(msg))

    def __reset(self):
        self.exited = False
        self._error = None
        self.is_open.clear()
        
if __name__ in "__main__":
    import time
    ws_client = LNMarketsWebsocket()
    ws_client.connect(BASE_URL)
