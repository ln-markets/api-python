options = {
  'key': 'your_api_key', 
  'secret': 'your_api_secret', 
  'passphrase': 'your_api_passphrase'
}

lnm = rest.LNMarketsRest(**options)
lnm.futures_new_position({'type':'m', 'side': 'b', 'quantity': 1, 'leverage': 50})
