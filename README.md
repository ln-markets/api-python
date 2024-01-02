# LN Markets Python API 

A simple way to connect your Python application to [LN Markets](https://lnmarkets.com/)!

## Install

You can install this package with pip:
```shell
pip3 install ln-markets
```

## Use

You can import the rest class from lnmarkets
```python
from lnmarkets import rest
```
And the websocket class as well
```python
from lnmarkets import websockets
```

## Authentication

> For authentication you need your api **key** **secret** and **passphrase**

Without you will not bet able to authenticate

> :warning: **Never share your API Key, Secret or Passphrase**

## Websocket API

### Configuration

Use the LNMarketsWebsocket and your key / passphrase to instanciate a new api connector: 

```python
options = {'key': 'your_api_key', 
           'secret': 'your_api_secret', 
           'passphrase': 'your_api_passphrase',
           'network': 'testnet'}

lnm = websockets.LNMarketsWebsocket(**options)
lnm.connect()
```

> Check [examples](examples/websocket/README.md) for more details as you'll need to extend this class most of the time.

### Subscription

You can subscribe to LNM Markets public event such as futures last price ('futures:btc_usd:last-price') and index ('futures:btc_usd:index').

## REST API Authentication

### Using API key

Use the LNMarketsRest and your key / passphrase to instanciate a new api connector: 

```python
from lnmarkets import rest

options = {'key': 'your_api_key', 
           'secret': 'your_api_secret', 
           'passphrase': 'your_api_passphrase',
           'network': 'testnet'}

lnm = rest.LNMarketsRest(**options)

lnm.futures_get_ticker()

```

### Using Mnemonic seed

Use the LNMarketsRest with [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki) mnemonic phrase
to instanciate a new api connector: 

```python
from lnmarkets import rest

mnemonic = 'struggle goddess action cheap endorse venue force tomato exercise cactus charge such'

lnm = rest.LNMarketsRest(mnemonic=mnemonic)

lnm.futures_get_ticker()

```

Mnemonic seed auth is a "hack" using the cookie used by LNM WebApp, so for avoid risk of stolen cookie, you should 
logout, when your program stop running:

```python
lnm.logout()
```
The cookie have a lifetime (about 1 week), so if your program running for more than that time you might renew the 
cookie before expiry date (note that it can also be a safety measure tu renew your cookie often to avoid 
stolen cookies risk):

```python
lnm.renew_cookie()
```
## REST API

- [`futures_add_margin`](#futures_add_margin)
- [`futures_cancel_all`](#futures_cancel_all)
- [`futures_close_all`](#futures_close_all)
- [`futures_cancel`](#futures_cancel)
- [`futures_cashin`](#futures_cashin)
- [`futures_close`](#futures_close)
- [`futures_get_trades`](#futures_get_trades)
- [`futures_new_trade`](#futures_new_trade)
- [`futures_update_trade`](#futures_update_trade)
- [`futures_carry_fees`](#futures_carry_fees)
- [`futures_get_price`](#futures_get_price)
- [`futures_fixing`](#futures_fixing)
- [`futures_index`](#futures_index)
- [`futures_get_leaderboard`](#futures_get_leaderboard)
- [`futures_get_ticker`](#futures_get_ticker)
- [`futures_get_market`](#futures_get_market)
- [`options_get_instruments`](#options_get_instruments)
- [`options_get_instrument`](#options_get_instrument)
- [`options_close_all`](#options_close_all)
- [`options_close`](#options_close)
- [`options_get_trades`](#options_get_trades)
- [`options_new_trade`](#options_new_trade)
- [`options_update_trade`](#options_update_trade)
- [`options_get_volatility`](#options_get_volatility)
- [`options_get_market`](#options_get_market)
- [`get_swaps`](#get_swaps)
- [`swap`](#swap)
- get_user
- update_user
- get_new_bitcoin_address
- get_bitcoin_addresses
- get_deposit
- get_deposits
- new_deposit
- get_withdrawal
- get_withdrawals
- new_withdraw
- new_internal_transfer
- get_oracle_index
- get_oracle_last
- fetch_notifications
- mark_notifications_read
- app_configuration
- app_node


[`See the API documentation`](https://docs.lnmarkets.com/api/v2) for more details.


### futures_add_margin

Add more margin to an existing trade.

```yml
amount:
  type: Integer
  required: true
id:
  type: String
  required: true
```

Example:

```python
lnm.futures_add_margin({
    'amount': 20000,
    'id': '249dc818-f8a5-4713-a3a3-8fe85f2e8969'
  })
```

[`POST /futures/add-margin`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_cancel_all

Cancel all opened (not running) trades for this user.

```
# No parameters
```

Example:

```python
lnm.futures_cancel_all()
```

[`DELETE /futures/all/cancel`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_close_all

Close all running trades for this user.

```
# No parameters
```

Example:

```python
lnm.futures_close_all()
```

[`DELETE /futures/all/close`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_cancel

Cancel a specific trade for this user.

```yml
id:
  type: String
  required: true
```

Example:

```python
lnm.futures_cancel_position({
    'id': 'b87eef8a-52ab-2fea-1adc-c41fba870b0f'
  })
```

[`POST /futures/cancel`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_cashin

Cash in a part of the PL of a running trade.

```yml
amount:
  type: Integer
  required: true
id:
  type: String
  required: true
```

Example:

```python
lnm.futures_cashin({
    'amount': 1000,
    'id': "99c470e1-2e03-4486-a37f-1255e08178b1"
  })
```

[`POST /futures/cash-in`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_carry_fees

Get carry-fees history.

```yml
from:
  type: Integer
  required: true

to:
  type: Integer
  required: tue

limit:
  type: Integer
  required: false
  default: 100
```

Example:

```python
lnm.futures_carry_fees({
    'limit': 20
  })
```

[`GET /futures/carry-fees`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_close

Close a specific running trade for this user.

```yml
id:
  type: String
  required: true
```

Example:

```python
lnm.futures_close({
    'id': 'a2ca6172-1078-463d-ae3f-8733f36a9b0e'
  })
```

[`DELETE /futures`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_get_trades

Retrieve all or a part of user's trades.

```yml
type:
  type: String
  required: true
  enum: ['open', 'running', 'closed']
  default: 'open'

from:
  type: Integer
  required: false

to:
  type: Integer
  required: false

limit:
  type: Integer
  required: false
  default: 100
```

Example:

```python
lnm.futures_get_trades({
    'type': 'running'
  })
```

[`GET /futures`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_new_trade

Open a new trade. If type="l", the property price must be included in the request to know when the trade should be filled. You can choose to use the margin or the quantity as a parameter, the other will be calculated with the one you chose.

```yml
type:
  type: String
  required: true
  enum: ['l', 'm']

side:
  type: String
  required: true
  enum: ['b', 's']

margin:
  type: Integer
  required: true

leverage:
  type: Float
  required: true

quantity:
  type: Integer
  required: false

takeprofit:
  type: Integer
  required: false

stoploss:
  type: Integer
  required: false

price:
  type: Float
  required: false
```

Example:

```python
  lnm.futures_new_trade({
    'type': 'm',
    'side': 's',
    'margin': 10000,
    'leverage': 25,
  })
```

[`POST /futures`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_update_trade

Modify stoploss or takeprofit parameter of an existing trade.

```yml
id:
  type: String
  required: true

type:
  type: String
  required: true
  enum: ['takeprofit', 'stoploss']

value:
  type: Float
  required: true
```

Example:

```python
lnm.futures_update_trade({
    'id': 'b87eef8a-52ab-2fea-1adc-c41fba870b0f',
    'type': 'stoploss',
    'value': 13290.5
  })
```

[`PUT /futures`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_get_price

Get Futures price data over time.

```yml
from:
  type: Integer
  required: false

to:
  type: Integer
  required: false

limit: Integer
  required: false
  default: 100
```

Example:

```python
lnm.futures_price({
    'limit': 20
  })
```

[`GET /futures/history/price`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_fixing

Get fixing data history.

```yml
from:
  type: Integer
  required: false

to:
  type: Integer
  required: false

limit:
  type: Integer
  required: false
  default: 100
```

Example:

```python
lnm.futures_fixing({
    'limit': 20
  })
```

[`GET /futures/history/fixing`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_index

Get index history data.

```yml
from:
  type: Integer
  required: false

to:
  type: Integer
  required: false

limit:
  type: Integer
  required: false
  default: 100
```

Example:

```python
lnm.futures_index({
    'limit': 20
  })
```

[`GET /futures/history/index`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_get_ticker

Get the futures ticker.

```
# No parameters
```

Example:

```python
lnm.futures_get_ticker()
```

[`GET /futures/ticker`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_get_leaderboard

Queries the 10 users with the biggest positive PL on a daily, weekly, monthly and all-time basis.

```
# No parameters
```

Example:

```python
lnm.futures_get_leaderboard()
```

[`GET /futures/leaderboard`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### futures_get_market

Get the futures market details.

```
# No parameters
```

Example:

```python
lnm.futures_get_market()
```

[`GET /futures/market`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_get_instruments

Get the options instruments list.

```
# No parameters
```

Example:

```python
lnm.options_get_instruments()
```

[`GET /options/instruments`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_get_instrument

Get a specific option instrument detail.

```yml
instrument_name:
  type: String
  required: true
```

Example:

```python
lnm.options_get_instrument({
    'instrument_name': 'BTC.2024-01-05.43000.C'
  })
```


[`GET /options/instrument`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_close_all

Close all of the user option trades, the PL will be calculated against the current bid or offer depending on the type of the options.

```
# No parameters
```

Example:

```python
lnm.options_close_all()
```

[`DELETE /options/close-all`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_close

Close the user option trade, the PL will be calculated against the current bid or offer depending on the type of the option.

```yml
id:
  type: String
  required: true
```

Example:

```python
lnm.options_close({
    'id': 'a61faebc-7cc9-47e4-a22d-9d3e95c98322'
  })
```

[`DELETE /options`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_get_trades

Get user's options trades.

```yaml
status:
  type: String
  enum: ['running', 'closed']
  default: running
  required: true

from:
  type: Integer
  required: false

to:
  type: Integer
  required: false

limit:
  type: Integer
  required: false
```

Example:

```python
  lnm.options_get_trades({
    limit: 25,
    status: 'closed'
  })
```

[`GET /options`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_new_trade

Create a new options trade

```yaml
side:
  type: String
  enum: ['b']
  required: true

quantity:
  type: Integer
  required: true

settlement:
  type: String
  enum: ['physical', 'cash']
  required: true

instrument_name:
  type: String
  required: true

```

Example:

```python
  lnm.options_new_trade({
    'side': 'b',
    'quantity': 10,
    'settlement': 'physical',
    'instrument_name': 'BTC.2024-01-05.43000.C'
  })
```

[`POST /options`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### options_update_trade

Allows user to update settlement parameter in running option trade.

```yml
id:
  type: String
  required: true

settlement:
  type: String
  required: true
  enum: ['physical', 'cash']
```

Example:

```python
lnm.options_update_trade({
    'id': 'a2ca6172-1078-463d-ae3f-8733f36a9b0e',
    'settlement': 'physical'
  })
```

[`PUT /options`](https://docs.lnmarkets.com/api/v2) documentation for more details.

#### options_get_volatility

Return the volatility

```yml
instrument:
  type: String
  required: false
```

Example:

```python
lnm.options_get_volatility({
    'instrument': 'BTC.2016-01-14.20000.C'
  })
```

[`GET /options/volatility`](https://docs.lnmarkets.com/api/v2) documentation for more details.

#### options_get_market

Get the options market details.

```
# No parameters
```

Example:

```python
lnm.options_get_market()
```

[`GET /options/market`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### get_swaps

Get swap history

```yml
from:
  type: Integer
  required: false
  
to:
  type: Integer
  required: false
  
limit:
  type: Integer
  required: False

```

Example:

```python
  lnm.get_swaps({
    'from': 1669980001000,
    'to': '1669990201000',
    'limit': 100
  })
```

[`GET /swap`](https://docs.lnmarkets.com/api/v2) documentation for more details.

### swap

Swap betweem sats and synthetic USD

```yml
in_asset:
  type: String
  required: true
  enum: ['USD', 'BTC']
  
out_asset:
  type: String
  required: true
  enum: ['USD', 'BTC']

in_amount:
  type: Integer
  required: False

out_amount:
  type: Integer
  required: false

```

Example:

```python
  lnm.swap({
    'in_asset': 'BTC',
    'out_asset': 'USD',
    'out_amount': 100
  })
```

[`POST /swap`](https://docs.lnmarkets.com/api/v2) documentation for more details.
