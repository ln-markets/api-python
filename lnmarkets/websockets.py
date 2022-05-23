import websocket
import os
import secrets
import json

def get_hostname(network):
    hostname = os.environ.get('LNMARKETS_API_HOSTNAME')
    
    if hostname:
        return hostname
    elif network == 'testnet':
        return 'api.testnet.lnmarkets.com'
    else:
        return 'api.lnmarkets.com'

class LNMarketsWebsocket:
    def __init__(self, **options):
        self.ws = None
        self.key = options.get('key', os.getenv('LNMARKETS_API_KEY'))
        self.secret = options.get('secret', os.getenv('LNMARKETS_API_SECRET'))
        self.passphrase = options.get('passphrase', os.getenv('LNMARKETS_API_PASSPHRASE'))
        self.network = options.get('network', os.getenv('LNMARKETS_API_NETWORK', 'mainnet'))
        self.version = options.get('version', os.getenv('LNMARKETS_API_VERSION', 'v1'))
        self.hostname = get_hostname(self.network)
        self.ws = None

    def on_message(self, ws, message):
        print(message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Closed connection")

    def on_open(self, ws):
        print("Opened connection")

    def connect(self):
        self.ws = websocket.WebSocketApp("wss://" + self.hostname,
            on_open = self.on_open,
            on_message = self.on_message,
            on_error = self.on_error,
        )
        self.ws.run_forever()
    
    def subscribe(self, params):
        payload = {
            "jsonrpc": "2.0",
            "method": "subscribe",
            "id": secrets.token_bytes(4).hex(),
            "params": params
        }

        self.ws.send(json.dumps(payload))

    def unsubscribe(self, params):
        payload = {
            "jsonrpc": "2.0",
            "method": "unsubscribe",
            "id": secrets.token_bytes(4).hex(),
            "params": params
        }

        self.ws.send(json.dumps(payload))

    def list_methods(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "__listMethods",
            "id": secrets.token_bytes(4).hex(),
        }

        self.ws.send(json.dumps(payload))

    def list_events(self):
        payload = {
            "jsonrpc": "2.0",
            "method": "__listEvents",
            "id": secrets.token_bytes(4).hex(),
        }

        self.ws.send(json.dumps(payload))
