options = {
  'key': 'YOUR_KEY', 
  'secret': 'YOUR_SECRET', 
  'passphrase': 'YOUR_PASSPHRASE'
}


lnm = LNM_REST_API(**options)
lnm.futures_new_position({'type':'m', 'side': 'b', 'quantity': 1, 'leverage': 50})
