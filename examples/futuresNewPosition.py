
lnm = LNM_REST_API()

lnm.set_auth(api_key='copy your api key here'
            api_secret='copy your api secret here',
            passphrase='copy your passphrase here')
            
lnm.set_url(url = 'https://api.lnmarkets.com/v1')

lnm.futuresNewPosition({'type':'m', 'side': 'b', 'quantity': 1, 'leverage': 50})
