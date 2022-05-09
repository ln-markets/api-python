# Extending websocket class

Since the default behaviour of this class is to only connect to the websocket without anything else, you'll need to extend it to customize its behaviour.

Here is the list of the function you might want to modify:

```python
  on_open(self, ws)
```

> This one is triggered once the websocket is connected, `self` is the class itself, `ws` is the instance that issued the event.

```python
  on_message(self, ws, message)
```

> By default, this event will only print the received message.

```python
  on_error(self, ws)
```

> By default, this event will only print the received error.

For example if you want to make your websocket to subscribe to `futures/market/bid-offer` you'll do something like...

```python
class LNMarketsWebsocketCustom(LNMarketsWebsocket):
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

lnmarkets = LNMarketsWebsocketCustom(**options)
lnmarkets.connect()

```

You can use `self.subscribe()`, `self.unsubscribe()`, `self.list_methods()`, `self.list_events()` to your liking as well!
