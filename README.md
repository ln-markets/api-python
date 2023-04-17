# LN Markets Python API 

A simple way to connect your Python application to [LN Markets](https://lnmarkets.com/)!

## Install

You can install this package with pip:
```shell
pip3 install ln-markets

## Usage

You can import rest class from ln_markets
```python
from lnmarkets import rest
```
And the websocket one as well!
```python
from lnmarkets import websockets

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
           'passphrase': 'your_api_passphrase'}

lnm = websockets.LNMarketsWebsocket(**options)
lnm.connect()
```

> Check [examples](examples/websocket/README.md) for more details as you'll need to extend this class most of the time.

### Subscription

You can subscribe to LNM Markets public event such as futures bid offer, index and options data.

## REST API

### Configuration

Use the LNMarketsRest and your key / passphrase to instanciate a new api connector: 

```python
options = {'key': 'your_api_key', 
           'secret': 'your_api_secret', 
           'passphrase': 'your_api_passphrase'}

lnm = rest.LNMarketsRest(**options)

lnm.futures_get_ticker()

```
## REST API

- [`futures_add_margin_position`](#futures_add_margin_position)
- [`futures_cancel_all_positions`](#futures_cancel_all_positions)
- [`futures_close_all_positions`](#futures_close_all_positions)
- [`futures_cancel_position`](#futures_cancel_position)
- [`futures_carry_fees_history`](#futures_carry_fees_history)
- [`futures_cashin_position`](#futures_cashin_position)
- [`futures_close_position`](#futures_close_position)
- [`futures_get_positions`](#futures_get_positions)
- [`futures_new_position`](#futures_new_position)
- [`futures_update_position`](#futures_update_position)
- [`futures_bid_offer_history`](#futures_bid_offer_history)
- [`futures_fixing_history`](#futures_fixing_history)
- [`futures_index_history`](#futures_index_history)
- [`futures_get_configuration`](#futures_get_configuration)
- [`futures_get_ticker`](#futures_get_ticker)
- [`options_get_expiries`](#options_get_expiries)
- [`options_get_configuration`](#options_get_configuration)
- [`options_close_all_positions`](#options_close_all_positions)
- [`options_close_position`](#options_close_position)
- [`options_get_positions`](#options_get_positions)
- [`options_new_position`](#options_new_position)
- [`options_update_position`](#options_update_position)
- [`options_get_volatility`](#options_get_volatility)
- [`deposit_history`](#deposit_history)
- [`deposit`](#deposit)
- [`get_user`](#get_user)
- [`update_user`](#update_user)
- [`get_notifications`](#get_notifications)
- [`mark_notifications_read`](#mark_notifications_read)
- [`withdraw_history`](#withdraw_history)
- [`withdraw`](#withdraw)
- [`swap`](#swap)
- [`swap_history`](#swap_history)
- [`app_configuration`](#app_configuration)
- [`app_node`](#app_node)
- [`get_leaderboard`](#get_leaderboard)
- [`get_oracle`](#get_oracle)

### futures_add_margin_position

Add more margin to an existing position.

```yml
amount:
  type: Integer
  required: true
pid:
  type: String
  required: true
```

Example:

```python
lnm.futures_add_margin_position({
    'amount': 20000,
    'pid': '249dc818-f8a5-4713-a3a3-8fe85f2e8969'
  })
```

[`POST /futures/add-margin`](https://docs.lnmarkets.com/api/v1/#add-margin) documentation for more details.

### futures_cancel_all_positions

Cancel all opened (not running) positions for this user.

```
# No parameters
```

Example:

```python
lnm.futures_cancel_all_positions()
```

[`DELETE /futures/all/cancel`](https://docs.lnmarkets.com/api/v1/#cancel-all) documentation for more details.

### futures_close_all_posisitions

Close all running position for this user.

```
# No parameters
```

Example:

```python
lnm.futures_close_all_positions()
```

[`DELETE /futures/all/close`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

### futures_cancel_position

Cancel a particular position for this user.

```yml
pid:
  type: String
  required: true
```

Example:

```python
lnm.futures_cancel_position({
    'pid': 'b87eef8a-52ab-2fea-1adc-c41fba870b0f'
  })
```

[`POST /futures/cancel`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

### futures_carry_fees_history

Get carry-fees history.

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
lnm.futures_carry_fees_history({
    'limit': 20
  })
```

[`GET /futures/carry-fees`](https://docs.lnmarkets.com/api/v1/#futures-carry-fees-history) documentation for more details.

### futures_cashin_position

Retrieve a part of the general PL of a running position.

```yml
amount:
  type: Integer
  required: true
pid:
  type: String
  required: true
```

Example:

```python
lnm.futures_cashin_position({
    'amount': 1000,
    'pid': "99c470e1-2e03-4486-a37f-1255e08178b1"
  })
```

[`POST /futures/cash-in`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

### futures_close_position

Close a particular running position for this user.

```yml
pid:
  type: String
  required: true
```

Example:

```python
lnm.futures_close_position({
    'pid': 'a2ca6172-1078-463d-ae3f-8733f36a9b0e'
  })
```

[`DELETE /futures`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

### futures_get_positions

Retrieve all or a part of user positions.

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
lnm.futures_get_positions({
    'type': 'running'
  })
```

[`GET /futures`](https://docs.lnmarkets.com/api/v1/#history) documentation for more details.

### futures_new_position

Open a new position on the market.

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
  required: false

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
  lnm.futures_new_position({
    'type': 'm',
    'side': 's',
    'margin': 10000,
    'leverage': 25.5,
  })
```

[`POST /futures`](https://docs.lnmarkets.com/api/v1/#create) documentation for more details.

### futures_update_position

Modify stoploss or takeprofit parameter of an existing position.

```yml
pid:
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
lnm.futures_update_position({
    'pid': 'b87eef8a-52ab-2fea-1adc-c41fba870b0f',
    'type': 'stoploss',
    'value': 13290.5
  })
```

[`PUT /futures`](https://docs.lnmarkets.com/api/v1/#update) documentation for more details.

### futures_bid_offer_history

Get bid and offer data over time.

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
lnm.futures_bid_offer_history({
    'limit': 20
  })
```

[`GET /futures/history/bid-offer`](https://docs.lnmarkets.com/api/v1/#futures-bid-and-offer-history) documentation for more details.

### futures_fixing_history

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
lnm.futures_fixing_history({
    'limit': 20
  })
```

[`GET /futures/history/fixing`](https://docs.lnmarkets.com/api/v1/#futures-fixing-history) documentation for more details.

### futures_index_history

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
lnm.futures_index_history({
    'limit': 20
  })
```

[`GET /futures/history/index`](https://docs.lnmarkets.com/api/v1/#futures-index-history) documentation for more details.


### futures_get_configuration

Get the configuration related to futures trading on the platform.

```
# No parameters
```

Example:

```python
lnm.futures_get_configuration()
```

[`GET /futures/instrument`](https://docs.lnmarkets.com/api/v1/#tag/Futures/paths/~1futures~1instrument/get) documentation for more details.

### futures_get_ticker

Get the futures ticker.

```
# No parameters
```

Example:

```python
lnm.futures_get_ticker()
```

[`GET /futures/ticker`](https://docs.lnmarkets.com/api/v1/#tag/Futures/paths/~1futures~1ticker/get) documentation for more details.

### options_get_expiries

Get the options expiries.

```
# No parameters
```

Example:

```python
lnm.options_get_expiries()
```

[`GET /options/instrument/expiry`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1instrument~1expiry/get) documentation for more details.

### options_get_configuration

Get the options configuration.

```
# No parameters
```

Example:

```python
lnm.options_get_configuration()
```

[`GET /options/instrument`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1instrument~1expiry/get) documentation for more details.

### options_close_all_positions

Close all of the user option trades, the PL will be calculated against the current bid or offer depending on the type of the options.

```
# No parameters
```

Example:

```python
lnm.options_close_all_positions()
```

[`DELETE /options/vanilla/all`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1vanilla~1all/delete) documentation for more details.

### options_close_position

Close the user option trade, the PL will be calculated against the current bid or offer depending on the type of the option.

```yml
id:
  type: String
  required: true
```

Example:

```python
lnm.options_close_position({
    'id': 'a61faebc-7cc9-47e4-a22d-9d3e95c98322'
  })
```

[`DELETE /options/vanilla`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1vanilla/delete) documentation for more details.

### options_get_positions

Get user's vanilla options trades.

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
  lnm.options_get_positions({
    limit: 25,
    status: 'closed'
  })
```

[`GET /options/vanilla`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1vanilla/get) documentation for more details.

### options_new_position

Create a new options trade

```yaml
side:
  type: String
  enum: ['b']
  required: true

type:
  type: String
  enum: ['c', 'p']
  required: true

quantity:
  type: Integer
  required: true

strike:
  type: Integer
  required: true

settlement:
  type: String
  enum: ['physical', 'cash']
  required: true
```

Example:

```python
  lnm.options_new_position({
    limit: 25,
    status: 'closed'
  })
```

[`POST /options/vanilla`](https://docs.lnmarkets.com/api/v1) documentation for more details.

### options_update_position

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
lnm.options_update_position({
    'pid': 'a2ca6172-1078-463d-ae3f-8733f36a9b0e',
    'settlement': 'physical'
  })
```

[`PUT /options/vanilla`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1vanilla/put) documentation for more details.

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

[`GET /options/volatility`](https://docs.lnmarkets.com/api/v1/#tag/Options/paths/~1options~1volatility/get) documentation for more details.

### deposit_history

Retrieve deposit history for this user.

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
```

Example:

```python
lnm.deposit_history({
    'limit': 30
  })
```

[`GET /user/deposit`](https://docs.lnmarkets.com/api/v1/#deposit) documentation for more details.

### deposit

Add funds to your LN Markets balance.

```yml
amount:
  type: Integer
  required: true
unit:
  type: String
  required: false
  default: 'sat'
```

Example:

```python
lnm.deposit({
    'amount': 25000
  })
```

[`POST /user/deposit`](https://docs.lnmarkets.com/api/v1/#deposit) documentation for more details.

### get_user

Retrieve user informations.

```
# No parameters
```

Example:

```python
lnm.get_user()

[`GET /user`](https://docs.lnmarkets.com/api/v1/#informations) documentation for more details.

### update_user

Modifies account parameters.

```yml
show_leaderboard:
  type: boolean
  required: false
use_taproot_addresses:
  type: boolean
  required: false
username:
  type: string
  required: false
auto_withdraw_enabled:
  type: boolean
  required: false
auto_withdraw_lightning_address:
  type: string
  required: false
nostr_pubkey
  type: string
  required: false
```

Example:

```python
lnm.update_user({
    'show_leaderboard': true,
    'username': 'crypto-king',
    'nostr_pubkey': 'bfef3e7ac61fa5450f80f346579234cbb06891e910d1a208b91bf0fd40ab3cc6'
  })
```

[`PUT /user`](https://docs.lnmarkets.com/api/v1/#tag/User/paths/~1user/put) documentation for more details.

### get_notifications

Get notifications for a user

```
# No parameters
```

Example:

```python
lnm.get_notifications()
```

[`GET /user/notifications`](https://docs.lnmarkets.com/api/v1/#tag/User/paths/~1user~1notifications/get) documentation for more details.

### mark_notifications_read

Mark notification as read

```yml
ids:
  type: 	
  array of strings 
  required: true
```

Example:

```python
lnm.mark_notifications_read({"ids": 
    ['497f6eca-6276-4993-bfeb-53cbbbba6f08']
})
```

[`PUT /user/notifications`](https://docs.lnmarkets.com/api/v1/#tag/User/paths/~1user~1notifications/put) documentation for more details.

### withdraw_history

Retrieve user withdraw history.

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
```

Example:

```python
lnm.withdraw_history({
   'limit': 25
  })
```

[`GET /user/withdraw`](https://docs.lnmarkets.com/api/v1/#withdraw) documentation for more details.

### withdraw

Move funds from LN Markets to your wallet via BOLT11 invoice.

```yml
amount:
  type: Integer
  required: true

unit:
  type: String
  required: false
  default: 'sat'

invoice:
  type: String
  required: true
```

Example:

```python
lnm.withdraw({
    'amount': 1000,
    'invoice': 'lntb100u1p0jr0ykpp5ldx3un8ym6z0uwjxd083mp2rcr04d2dv0fkx729ajs62pq9pfjqqdql23jhxapdwa5hg6rywfshwttjda6hgegcqzpgxq92fjuqsp5m6q0fzynu2qr624mzjc285duurhccmkfg94mcdctc0p9s7qkrq8q9qy9qsqp862cjznpey5r76e7amhlpmhwn2c7xvke59srhv0xf75m4ksjm4hzn8y9xy0zs5ec6gxmsr8gj4q23w8ped32llscjcneyjz2afeapqpu4gamz'
  })
```

[`POST /user/withdraw`](https://docs.lnmarkets.com/api/v1/#withdraw-via-invoice) documentation for more details.

### swap

Swap betweem sats and synthetic assets

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

[`POST /swap`](https://docs.lnmarkets.com/api/v1/#tag/Swap/paths/~1swap/post) documentation for more details.

### swap_history

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
  lnm.swap_history({
    'from': 1669980001000,
    'to': '1669990201000',
    'limit': 100
  })
```

[`GET /swap_history`](https://docs.lnmarkets.com/api/v1/#tag/Swap/paths/~1swap/get) documentation for more details.

#### app_configuration

Retrieves the configuration of LN Markets

```
# No parameters
```

Example:

```python
lnm.app_configuration()
```

[`GET /app/configuration`](https://docs.lnmarkets.com/api/v1/#tag/App/paths/~1app~1configuration/get) documentation for more details.

#### app_node

Show informations about LN Markets lightning node.

```
# No parameters
```

Example:

```python
lnm.app_node()
```

[`GET /app/node`](https://docs.lnmarkets.com/api/v1/#tag/App/paths/~1app~1node/get) documentation for more details.

### get_leaderboard

Queries the 10 users with the biggest positive PL.

```
# No parameters
```

Example:

```python
lnm.get_leaderboard()
```

[`GET /futures/leaderboard`](https://docs.lnmarkets.com/api/v1/#leaderboard) documentation for more details.

### get_oracle

Useful for oracles

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
  lnm.get_oracle({
    'from': 1669980001000,
    'to': '1669990201000',
    'limit': 100
  })
```

[`GET /oracle/index`](https://docs.lnmarkets.com/api/v1/#tag/Oracle) documentation for more details.


