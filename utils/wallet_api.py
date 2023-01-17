import requests
import json

class Utils():
    def __init__(self, link, params=None, headers=None):
        self.link = link
        self.params = params
        self.headers = headers
    
    def connect(self):
        response = requests.get(self.link, params=self.params, headers=self.headers)
        
        if response.status_code == 200:
            return self.jsonify(response.text)
        
        return None
    
    def jsonify(self, response):
        return json.loads(response)

# Насоздавал классов, для расширения, можно вырезать

class Wallet(Utils):
    def __init__(self, link, params=None, headers=None):
        self.link = link
        self.params = params
        self.headers = headers

class TonApi(Utils):
    def __init__(self, link, params=None, headers=None):
        self.link = link
        self.params = params
        self.headers = headers