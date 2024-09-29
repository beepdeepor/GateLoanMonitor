# coding: utf-8
import requests
import time
import hashlib
import hmac
import json
import datetime
import traceback
def gen_sign(method, url, query_string=None, payload_string=None):
    key = 'replace with gate api key'        # api_key
    secret = 'replace with gate secret key'     # api_secret
    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}
if __name__ == "__main__":
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    url = '/loan/multi_collateral/currency_quota'
    # replace AERO with the target currency you wanna monitor
    query_param = 'type=borrow&currency=AERO'
    while True:
        sign_headers = gen_sign('GET', prefix + url, query_param)
        headers.update(sign_headers)
        try:
            r = requests.request('GET', host + prefix + url + "?" + query_param, headers=headers)
            data = r.json()
            print(datetime.datetime.now(), data)
            left_borrowable_amt = float(data[0].get('left_quota', 0))
            if left_borrowable_amt >= 500:
                # send email or msg to notify yourself here
            time.sleep(6)
        except Exception as e:
            print(f"Exception occurred during get loan info: {e}")
            traceback.print_exc()
            time.sleep(6)
    print("exit process")
