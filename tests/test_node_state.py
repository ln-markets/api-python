lnm = LNM_REST_API()

lnm.set_auth(api_key='copy your api key here'
            api_secret='copy your api secret here',
            passphrase='copy your passphrase here')
            
lnm.set_url(url = 'https://api.lnmarkets.com/v1')

def test_node_state():
    method = 'GET'
    path = '/v1/state/node'
    params = {}
    timestamp = str(int(datetime.datetime.now().timestamp()*1000))
    #print(timestamp)

    url = "https://api.lnmarkets.com/v1/state/node"
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    data = url_parts[4]
    #print(urlparse.urlunparse(url_parts))

    payload = timestamp + method + path + data
    #print(payload)

    hashed = hmac.new(bytes(api_secret, 'utf-8'), bytes(payload, 'utf-8'), sha256).digest()

    signature = base64.b64encode(hashed)


    headers = {
        'Content-Type': 'application/json',
        'LNM-ACCESS-KEY': api_key,
        'LNM-ACCESS-PASSPHRASE': passphrase,
        'LNM-ACCESS-SIGNATURE': signature,  
        'LNM-ACCESS-TIMESTAMP': timestamp,
    }

    response = requests.request(method = method, url = urlparse.urlunparse(url_parts), headers=headers)

    assess (response.status_code == 200)
