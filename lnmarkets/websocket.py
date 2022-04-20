import asyncio
import websockets
import json
import pandas as pd
import datetime as dt
import time

from urllib.parse import urlencode
from datetime import datetime
from base64 import b64encode

import hashlib
import hmac
import json

class LNMarketsWebsocket:

    def __init__(self, key, secret, passphrase, live):

        if not live:
            self.url = 'wss://api.testnet.lnmarkets.com'
        elif live:
            self.url = 'wss://api.lnmarkets.com'
        else:
            raise Exception('live must be a bool, True=real, False=paper')

        self.key = key
        self.secret = secret
        self.passphrase = passphrase

        timestamp = str(int(datetime.now().timestamp() * 1000))

        method = 'auth/api-key'
        payload = timestamp + method

        hashed = hmac.new(bytes(secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).digest()
        signature = b64encode(hashed)

        params = {
            'timestamp': timestamp,
            'signature': signature.decode(),
            'passphrase': self.passphrase,
            'key': self.key}

        self.auth_creds = {
            "jsonrpc": "2.0",
            "method": 'auth/api-key',
            "id": '1',
            "params": params
        }

        # check auth works
        self.test_creds()

        self.msg = {
            "jsonrpc": "2.0",
            "method": None,
            "id": '1',
            "params": None
            }

    async def pub_api(self, msg):
        async with websockets.connect(self.url) as websocket:
            res_count = 0
            await websocket.send(msg)
            while True:
                response = await websocket.recv()
                res_count += 1
                print(response)
                if res_count == 5:
                    break
            return json.loads(response)

    # async def priv_api(self, msg):
    #     async with websockets.connect(self.url) as websocket:
    #         await websocket.send(json.dumps(self.auth_creds))
    #         while websocket.open:
    #             response = await websocket.recv()
    #             await websocket.send(msg)
    #             response = await websocket.recv()
    #             break
    #         return json.loads(response)
    
    async def auth_api(self, msg):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(msg)
            response = await websocket.recv()
            print(response)
            return json.loads(response)
    

    @staticmethod
    def async_loop(api, message):
        return asyncio.run(api(message))
    
    def test_creds(self):
        response = self.async_loop(self.auth_api, json.dumps(self.auth_creds))
        if 'error' in response:
            raise Exception(f"Auth failed with error {response['error']}")
        else:
            print("Auth creds are good, it worked")

    

# market data methods

    def sub_futures_bid_offer(self):
        self.msg["method"] = "subscribe"
        self.msg["params"] = ["futures/market/bid-offer"]
        data = self.async_loop(self.pub_api, json.dumps(self.msg))
        return data
        
    def sub_futures_index(self):
        self.msg['method'] = 'subscribe'
        self.msg['params'] = ["futures/market/index"]
        data = self.async_loop(self.pub_api, json.dumps(self.msg))
        return data
    
    def sub_options_forwards(self):
        self.msg['method'] = 'subscribe'
        self.msg['params'] = ["options/data/forwards"]
        data = self.async_loop(self.pub_api, json.dumps(self.msg))
        return data
        
        
    def sub_options_volcurve(self):
        self.msg['method'] = 'subscribe'
        self.msg['params'] = ["options/data/volatility-curve"]
        data = self.async_loop(self.pub_api, json.dumps(self.msg))
        return data
    
    def sub_options_ordermap(self):
        self.msg['method'] = 'subscribe'
        self.msg['params'] = ["options/data/ordermap"]
        data = self.async_loop(self.pub_api, json.dumps(self.msg))
        return data

    def sub_options_volatility(self):
        self.msg['method'] = 'subscribe'
        self.msg['params'] = ["options/market/volatility"]
        data = self.async_loop(self.pub_api, json.dumps(self.msg))
        return data


if __name__ == '__main__': 
    key = '<your_key>' 
    secret = '<your_secret>'
    passphrase = '<your_passphrase>'

    ws_client = LNMarketsWebsocket(key = key, secret = secret, passphrase = passphrase, live=True)
    
    ws_client.sub_futures_bid_offer()
