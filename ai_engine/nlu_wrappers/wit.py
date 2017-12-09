from wit import Wit
import requests
import os
import logging
import json


class WitException(Exception):
    pass


class WitClient(object):
    WIT_URL = os.getenv('WIT_URL', 'https://api.wit.ai')
    WIT_API_VERSION = os.getenv('WIT_API_VERSION', '08.12.2017')

    def __init__(self, access_token):
        self.access_token = access_token
        self.logger = logging.getLogger(__name__)
        self.headers = {'authorization': 'Bearer ' + access_token,
                        'accept': 'application/vnd.wit.' + WIT_API_VERSION + '+json'}

    def request(self, method, path, params, **kwargs):
        url = WIT_URL + path
        response = requests.request(
            method, url, params=params, headers=self.headers, **kwargs)
        if rsp.status_code > 200:
            raise WitError('Wit responded with status: ' + str(rsp.status_code) +
                           ' (' + rsp.reason + ')')
        json = rsp.json()
        if 'error' in json:
            raise WitError('Wit responded with an error: ' + json['error'])
        return json

    def get_entities(self, msg, thread_id, n=None, msg_id=None, context=None, verbose=None):
        params = {"thread_id": thread_id, "q": msg}
        if verbose is not None:
            params["verbose"] = verbose
        if n is not None:
            params['n'] = n
        if context:
            params['context'] = json.dumps(cotext)
        if msg_id:
            params['msg_id'] = msg_id
        response = requests("GET", "/message", params)
        return response

    def message(self, msg, thread_id):
        enitities = self.get_entities(msg, thread_id)["entities"]

if __name__ == '__main__':
    wit = WitWrapper("TLR66JM2JILRMTGJMSF5PZPNRDPZJYYZ")
    examples = [{"text": "Weather in Tokio", "entities": [
        {"entity": 'intent', "value": "temperature_get"}]}]
    wit.train(example)
