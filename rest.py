import datetime
import requests
import hashlib
import hmac
import base64
import urllib.parse
import json

class LNM_REST_API():
    """ the LNM API Class"""
    def __init(self):
        """ Initialize LNM API Class"""
        self.url = 'https://api.lnmarkets.com/v1'
    
    def set_url(self, url):
        """REST API URL"""
        self.url = url
            
    def set_auth(self, api_key, api_secret, passphrase):
        """API Key Authentication"""
        self.api_key = api_key
        self.api_secret = api_secret
        self.passphrase = passphrase
    
    def request_lnm(self, method, path, params):
        
        timestamp = str(int(datetime.datetime.now().timestamp()*1000))
        
        url2 = self.url + path
        path = '/v1' + path
        
        if ((method == 'GET') | (method == 'DELETE')):
            url_parts = list(urllib.parse.urlparse(url2))
            query = dict(urllib.parse.parse_qsl(url_parts[4]))
            query.update(params)
            url_parts[4] = urllib.parse.urlencode(query)
            data = url_parts[4]

        elif ((method == 'POST') | (method == 'PUT')):
            data = json.dumps(params, separators=(',', ':'))

        payload = timestamp + method + path + data

        hashed = hmac.new(bytes(self.api_secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hashed)

        headers = {
            'Content-Type': 'application/json',
            'LNM-ACCESS-KEY': self.api_key,
            'LNM-ACCESS-PASSPHRASE':  self.passphrase,
            'LNM-ACCESS-SIGNATURE': signature,  
            'LNM-ACCESS-TIMESTAMP': timestamp,
        }

        if ((method == 'GET') | (method == 'DELETE')):
            response = requests.request(method = method, url = urllib.parse.urlunparse(url_parts), headers=headers)
            
        elif ((method == 'POST') | (method == 'PUT')):
            response = requests.request(method = method, url = url2, data = data, headers=headers)
            
        return (response.text)
    
    def futuresNewPosition(self, params):
        method = 'POST'
        path = '/futures'
        return self.request_lnm(method, path, params)

    def futuresUpdatePosition(self, params):
        method = 'PUT'
        path = '/futures'
        return self.request_lnm(method, path, params)

    def futuresClosePosition(self, params):
        method = 'DELETE'
        path = '/futures'
        return self.request_lnm(method, path, params)

    def futuresCloseAllPositions(self, params):
        method = 'DELETE'
        path = '/futures/all/close'
        return self.request_lnm(method, path, params)

    def futuresCancelPosition(self, params):
        method = 'POST'
        path = '/futures/cancel'
        return self.request_lnm(method, path, params)

    def futuresCancelAllPositions(self, params):
        method = 'DELETE'
        path = '/futures/all/cancel'
        return self.request_lnm(method, path, params)

    def futuresCashinPosition(self, params):
        method = 'POST'
        path = '/futures/cash-in'
        return request_lnm(method, path, params)

    def futuresAddMarginPosition(self, params):
        method = 'POST'
        path = '/futures/add-margin'
        return self.request_lnm(method, path, params)

    def futuresGetPositions(self, params):
        method = 'GET'
        path = '/futures'
        return self.request_lnm(method, path, params)

    def futuresBidOfferHistory(self, params):
        method = 'GET'
        path = '/futures/history/bid-offer'
        return self.request_lnm(method, path, params)

    def futuresIndexHistory(self, params):
        method = 'GET'
        path = '/futures/history/index'
        return self.request_lnm(method, path, params)

    def futuresFixingHistory(self, params):
        method = 'GET'
        path = '/futures/history/fixing'
        return self.request_lnm(method, path, params)

    def futuresCarryFeesHistory(self, params):
        method = 'GET'
        path = '/futures/carry-fees'
        return self.request_lnm(method, path, params)

    def getUser(self):
        method = 'GET'
        path = '/user'
        params = {}
        return self.request_lnm(method, path, params)

    def updateUser(self, params):
        method = 'PUT'
        path = '/user'
        return self.request_lnm(method, path, params)

    def deposit(self, params):
        method = 'POST'
        path = '/user/deposit'
        return self.request_lnm(method, path, params)

    def depositHistory(self, params):
        method = 'GET'
        path = '/user/deposit'
        return self.request_lnm(method, path, params)

    def withdraw(self, params):
        method = 'POST'
        path = '/user/withdraw'
        return self.request_lnm(method, path, params)

    def withdrawHistory(self, params):
        method = 'GET'
        path = '/user/withdraw'
        return self.request_lnm(method, path, params)

    def apiState(self):
        method = 'GET'
        path = '/state'
        params = {}
        return self.request_lnm(method, path, params)

    def nodeState(self):
        method = 'GET'
        path = '/state/node'
        params = {}
        return self.request_lnm(method, path, params)

    def getLeaderboard(self):
        method = 'GET'
        path = '/futures/leaderboard'
        params = {}
        return self.request_lnm(method, path, params)

    def getAnnouncements(self):
        method = 'GET'
        path = '/state/announcements'
        params = {}
        return self.request_lnm(method, path, params)

    def getLnurlAuth(self):
        method = 'POST'
        path = '/lnurl/auth'
        params = {}
        return self.request_lnm(method, path, params)

    def lnurlAuth(self):
        method = 'GET'
        path = '/lnurl/auth'
        params = {}
        return self.request_lnm(method, path, params)


    
