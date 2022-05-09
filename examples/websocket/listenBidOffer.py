class LNMarketsWebsocketWrapper(LNMarketsWebsocket):
    def __init__(self, **options):
        super().__init__(**options)
    
    def on_open(self, ws):
        print("Opened connection")
        self.subscribe(["futures/market/bid-offer"])

options = {
  'key': 'your_api_key', 
  'secret': 'your_api_secret', 
  'passphrase': 'your_api_passphrase'
}

lnmarkets = LNMarketsWebsocket()
lnmarkets.connect()
