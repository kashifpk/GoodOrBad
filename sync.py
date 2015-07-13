from kivy.network.urlrequest import UrlRequest

import hashlib
import json

#url_base = 'http://192.168.1.4:6543'
url_base = 'http://sync.compulife.com.pk'
sync_url = url_base + '/sync/good_or_bad/deeds'
sync_load_url = url_base + '/load/good_or_bad/deeds'


def sync_data(deeds, settings, on_success=None, on_error=None, on_failure=None):
    
    req_data = {
        'user_id': settings['user_id'],
        'password': hashlib.sha1(settings['password']).hexdigest()
        }

    deeds_list = []
    for deed in deeds:
        deeds_list.append(deed.to_dict())
    
    req_data['deeds'] = deeds_list
    
    params = json.dumps(req_data)
    
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}

    req = UrlRequest(
        sync_url,
        req_body=params,
        req_headers=headers,
        on_success=on_success,
        on_error=on_error,
        on_failure=on_failure
    )

def load_sync_data(settings, on_success=None, on_error=None, on_failure=None):
    req_data = {
        'user_id': settings['user_id'],
        'password': hashlib.sha1(settings['password']).hexdigest()
        }

    params = json.dumps(req_data)
    
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}

    req = UrlRequest(
        sync_load_url,
        req_body=params,
        req_headers=headers,
        on_success=on_success,
        on_error=on_error,
        on_failure=on_failure
    )
