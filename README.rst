# LN Markets Python API 

A simple way to connect your Python application to [LN Markets](https://lnmarkets.com/)!

## Install

You can install this package with pip:
```
pip install ln-markets
```

## Usage

You can import rest class from ln_markets
```
from lnmarkets import rest
```

## Authentication

> For authentication you need your api **key** **secret** and **passphrase**

Without you will not bet able to authenticate

> :warning: **Never share your API Key, Secret or Passphrase**

## Configuration

Use the LNMarketsRest and your key / passphrase to instanciate a new api connector: 

```python
options = {'key': 'your_api_key', 
           'secret': 'your_api_secret', 
           'passphrase': 'your_api_passphrase'}

lnm = LNMarketsRest(**options)

lnm.futures_get_ticker()

```
## REST API

- [`futures_new_position`](#futures_new_position)
- [`futures_get_positions`](#futures_get_positions)
- [`futures_update_position`](#futures_update_position)
- [`futures_add_margin_position`](#futures_add_margin_position)
- [`futures_cancel_all_positions`](#futures_cancel_all_positions)
- [`futures_cancel_position`](#futures_cancel_position)
- [`futures_cashin_position`](#futures_cashin_position)
- [`futures_close_all_positions`](#futures_close_all_positions)
- [`futures_close_position`](#futures_close_position)
- [`futures_index_history`](#futures_index_history)
- [`futures_bid_offer_history`](#futures_bid_offer_history)
- [`futures_fixing_history`](#futures_fixing_history)
- [`futures_carry_fees_history`](#futures_carry_fees_history)
- [`deposit`](#deposit)
- [`deposit_history`](#deposit_history)
- [`futures_history`](#futures_history)
- [`get_announcements`](#get_announcements)
- [`get_leaderboard`](#get_leaderboard)
- [`get_user`](#get_user)
- [`api_state`](#api_state)
- [`node_state`](#node_state)
- [`update_user`](#update_user)
- [`withdraw`](#withdraw)
- [`withdraw_history`](#withdraw_history)

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

### add_margin

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
lnm.add_margin({
    'amount': 20000,
    'pid': '249dc818-f8a5-4713-a3a3-8fe85f2e8969'
  })
```

[`POST /futures/add-margin`](https://docs.lnmarkets.com/api/v1/#add-margin) documentation for more details.

### futures_cancel_all_positions

Cancel all oponed (not running) positions for this user.

```
# No parameters
```

Example:

```python
lnm.futures_cancel_all_positions()
```

[`DELETE /futures/all/cancel`](https://docs.lnmarkets.com/api/v1/#cancel-all) documentation for more details.

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

### get_announcements

Retrieve announcements made by LN Markets.

```
# No parameters
```

Example:

```python
lnm.get_announcements()
```

[`GET /state/announcemenets`](https://docs.lnmarkets.com/api/v1/#get-the-ln-markets-announcements) documentation for more details.

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

### get_user

Retrieve user informations.

```
# No parameters
```

Example:

```python
lnm.getUser()
```

[`GET /user`](https://docs.lnmarkets.com/api/v1/#informations) documentation for more details.

#### node_state

Show informations about LN Markets lightning node.

```
# No parameters
```

Example:

```python
lnm.node_state()
```

[`GET /state/node`](https://docs.lnmarkets.com/api/v1/#node-informations) documentation for more details.

#### update_user

Modify user account parameters.

```yml
show_leaderboard:
  type: Boolean
  required: false

show_username:
  type: Boolean
  required: false

username:
  type: String
  required: false

email:
  type: String
  required: false

resend_email:
  type: Boolean
  required: false
```

Example:

```python
lnm.update_user({
    'show_username': True,
    'show_leaderboard': True,
    'username': 'API-Connector',
  })
```

[`PUT /user`](https://docs.lnmarkets.com/api/v1/#update-user) documentation for more details.

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
