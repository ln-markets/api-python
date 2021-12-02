# LN Markets Python API 

A simple way to connect your Python application to [LN Markets](https://lnmarkets.com/)!

## Install

You can install this package with pip:
```
pip install LNM_Python_API
```

## Usage

You can import rest class from LNM_Python_API
```
from lnmarkets_python import rest
```

## Authentication

> For authentication you need your api **key** **secret** and **passphrase**

Without you will not bet able to authenticate

> :warning: **Never share your API Key, Secret or Passphrase**

## Configuration

Use the LNM_REST_API() to enter your authentication keys and set the API url: 

lnm = LNM_REST_API()

lnm.set_auth(api_key='copy your api key here',
            api_secret='copy your api secret here',
            passphrase='copy your passphrase here')

lnm.set_url(url = 'https://api.lnmarkets.com/v1')

## REST API

- [`futuresNewPosition`](#futuresNewPosition)
- [`futuresGetPositions`](#futuresGetPositions)
- [`futuresUpdatePosition`](#futuresUpdatePosition)
- [`futuresAddMarginPosition`](#futuresAddMarginPosition)
- [`futuresCancelAllPositions`](#futuresCancelAllPositions)
- [`futuresCancelPosition`](#futuresCancelPosition)
- [`futuresCashinPosition`](#futuresCashinPosition)
- [`futuresCloseAllPosisitions`](#futuresCloseAllPosisitions)
- [`futuresClosePosition`](#futuresClosePosition)
- [`futuresIndexHistory`](#futuresIndexHistory)
- [`futuresBidOfferHistory`](#futuresBidOfferHistory)
- [`futuresFixingHistory`](#futuresFixingHistory)
- [`futuresCarryFeesHistory`](#futuresCarryFeesHistory)
- [`deposit`](#deposit)
- [`depositHistory`](#depositHistory)
- [`futuresHistory`](#futuresHistory)
- [`getAnnouncements`](#getAnnouncements)
- [`getLeaderboard`](#getLeaderboard)
- [`getUser`](#getUser)
- [`apiState`](#apiState)
- [`nodeState`](#nodeState)
- [`updateUser`](#updateUser)
- [`withdraw`](#withdraw)
- [`withdrawHistory`](#withdrawHistory)

#### futuresNewPosition

Open a new position on the market.

```yaml
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

```JS
  await lnm.futuresNewPosition({
    type: 'm',
    side: 's',
    margin: 10000,
    leverage: 25.5,
  })
```

[`POST /futures`](https://docs.lnmarkets.com/api/v1/#create) documentation for more details.

#### futuresGetPositions

Retrieve all or a part of user positions.

```yaml
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

```JS
  await lnm.futuresGetPositions({
    type: 'running'
  })
```

[`GET /futures`](https://docs.lnmarkets.com/api/v1/#history) documentation for more details.

#### futuresUpdatePosition

Modify stoploss or takeprofit parameter of an existing position.

```yaml
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

```JS
  await lnm.futuresUpdatePosition({
    pid: 'b87eef8a-52ab-2fea-1adc-c41fba870b0f',
    type: 'stoploss',
    value: 13290.5
  })
```

[`PUT /futures`](https://docs.lnmarkets.com/api/v1/#update) documentation for more details.

#### addMargin

Add more margin to an existing position.

```yaml
amount:
  type: Integer
  required: true
pid:
  type: String
  required: true
```

Example:

```JS
  await lnm.addMargin({
    amount: 20000,
    pid: '249dc818-f8a5-4713-a3a3-8fe85f2e8969'
  })
```

[`POST /futures/add-margin`](https://docs.lnmarkets.com/api/v1/#add-margin) documentation for more details.

#### futuresCancelAllPositions

Cancel all oponed (not running) positions for this user.

```yaml
# No parameters
```

Example:

```JS
  await lnm.futuresCancelAllPositions()
```

[`DELETE /futures/all/cancel`](https://docs.lnmarkets.com/api/v1/#cancel-all) documentation for more details.

#### futuresCancelPosition

Cancel a particular position for this user.

```yaml
pid:
  type: String
  required: true
```

Example:

```JS
  await lnm.futuresCancelPosition({
    pid: 'b87eef8a-52ab-2fea-1adc-c41fba870b0f'
  })
```

[`POST /futures/cancel`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

#### futuresCashinPosition

Retrieve a part of the general PL of a running position.

```yaml
amount:
  type: Integer
  required: true
pid:
  type: String
  required: true
```

Example:

```JS
  await lnm.futuresCashinPosition({
    amount: 1000,
    pid: "99c470e1-2e03-4486-a37f-1255e08178b1"
  })
```

[`POST /futures/cash-in`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

#### futuresCloseAllPosisitions

Close all running position for this user.

```yaml
# No parameters
```

Example:

```JS
  await lnm.futuresCloseAllPosisitions()
```

[`DELETE /futures/all/close`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

#### futuresClosePosition

Close a particular running position for this user.

```yaml
pid:
  type: String
  required: true
```

Example:

```JS
  await lnm.futuresClosePosition({
    pid: 'a2ca6172-1078-463d-ae3f-8733f36a9b0e'
  })
```

[`DELETE /futures`](https://docs.lnmarkets.com/api/v1/#cancel) documentation for more details.

#### futuresIndexHistory

Get index history data.

```yaml
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

```JS
  await lnm.futuresIndexHistory({
    limit: 20
  })
```

[`GET /futures/history/index`](https://docs.lnmarkets.com/api/v1/#futures-index-history) documentation for more details.

#### futuresBidOfferHistory

Get bid and offer data over time.

```yaml
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

```JS
  await lnm.futuresBidOfferHistory({
    limit: 20
  })
```

[`GET /futures/history/bid-offer`](https://docs.lnmarkets.com/api/v1/#futures-bid-and-offer-history) documentation for more details.

#### futuresFixingHistory

Get fixing data history.

```yaml
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

```JS
  await lnm.futuresFixingHistory({
    limit: 20
  })
```

[`GET /futures/history/fixing`](https://docs.lnmarkets.com/api/v1/#futures-fixing-history) documentation for more details.

#### futuresCarryFeesHistory

Get carry-fees history.

```yaml
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

```JS
  await lnm.futuresCarryFeesHistory({
    limit: 20
  })
```

[`GET /futures/carry-fees`](https://docs.lnmarkets.com/api/v1/#futures-carry-fees-history) documentation for more details.

#### deposit

Add funds to your LN Markets balance.

```yaml
amount:
  type: Integer
  required: true
unit:
  type: String
  required: false
  default: 'sat'
```

Example:

```JS
  await lnm.deposit({
    amount: 25000
  })
```

[`POST /user/deposit`](https://docs.lnmarkets.com/api/v1/#deposit) documentation for more details.

#### depositHistory

Retrieve deposit history for this user.

```yaml
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

```JS
  await lnm.depositHistory({
    limit: 30
  })
```

[`GET /user/deposit`](https://docs.lnmarkets.com/api/v1/#deposit) documentation for more details.

#### getAnnouncements

Retrieve announcements made by LN Markets.

```yaml
# No parameters
```

Example:

```JS
  await lnm.getAnnouncements()
```

[`GET /state/announcemenets`](https://docs.lnmarkets.com/api/v1/#get-the-ln-markets-announcements) documentation for more details.

#### getLeaderboard

Queries the 10 users with the biggest positive PL.

```yaml
# No parameters
```

Example:

```JS
  await lnm.getLeaderboard()
```

[`GET /futures/leaderboard`](https://docs.lnmarkets.com/api/v1/#leaderboard) documentation for more details.

#### getUser

Retrieve user informations.

```yaml
# No parameters
```

Example:

```JS
  await lnm.getUser()
```

[`GET /user`](https://docs.lnmarkets.com/api/v1/#informations) documentation for more details.

#### apiState

Retrieve informations related to LN Markets lnm.

```yaml
# No parameters
```

Example:

```JS
  await lnm.apiState()
```

[`GET /state`](https://docs.lnmarkets.com/api/v1/#api-informations) documentation for more details.

#### nodeState

Show informations about LN Markets lightning node.

```yaml
# No parameters
```

Example:

```JS
  await lnm.nodeState()
```

[`GET /state/node`](https://docs.lnmarkets.com/api/v1/#node-informations) documentation for more details.

#### updateUser

Modify user account parameters.

```yaml
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

```JS
  await lnm.updateUser({
    show_username: true,
    show_leaderboard: true,
    username: 'API-Connector',
  })
```

[`PUT /user`](https://docs.lnmarkets.com/api/v1/#update-user) documentation for more details.

#### withdraw

Move funds from LN Markets to your wallet via BOLT11 invoice.

```yaml
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

```JS
  await lnm.withdraw({
    amount: 1000,
    invoice: 'lntb100u1p0jr0ykpp5ldx3un8ym6z0uwjxd083mp2rcr04d2dv0fkx729ajs62pq9pfjqqdql23jhxapdwa5hg6rywfshwttjda6hgegcqzpgxq92fjuqsp5m6q0fzynu2qr624mzjc285duurhccmkfg94mcdctc0p9s7qkrq8q9qy9qsqp862cjznpey5r76e7amhlpmhwn2c7xvke59srhv0xf75m4ksjm4hzn8y9xy0zs5ec6gxmsr8gj4q23w8ped32llscjcneyjz2afeapqpu4gamz'
  })
```

[`POST /user/withdraw`](https://docs.lnmarkets.com/api/v1/#withdraw-via-invoice) documentation for more details.

#### withdrawHistory

Retrieve user withdraw history.

```yaml
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

```JS
  await lnm.withdrawHistory({
    limit: 25
  })
```

[`GET /user/withdraw`](https://docs.lnmarkets.com/api/v1/#withdraw) documentation for more details.

#### requestAPI

This method is used in case where no wrapper is (yet) available for a particular endpoint.

```yaml
method:
  type: String
  required: true
  enum: ['GET', 'PUT', 'POST', 'DELETE']

path:
  type: String
  required: true

params:
  type: Object
  required: false

credentials:
  type: Boolean
  required: false
  default: false
```

Example:

```JS
  await lnm.requestAPI({
    method: 'GET',
    path: '/user',
    credentials: true
  })
```


### Methods
