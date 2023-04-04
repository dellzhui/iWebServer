import json
import logging
import requests

Log = logging.getLogger(__name__)


class HTTPRequestUtil:
    def __init__(self, base_url=None):
        self._BASE_URL = base_url

    def do_get(self, url, timeout=30):
        try:
            result = requests.get('{}{}'.format(self._BASE_URL, url), timeout=timeout).json()
            Log.debug('HTTPRequestUtil do_get result is {}'.format(result))
            return result
        except Exception as err:
            Log.exception('HTTPRequestUtil do_get err:[' + str(err) + ']')
        return None

    def do_post(self, url, data=None, timeout=30):
        try:
            result_ori = requests.post('{}{}'.format(self._BASE_URL, url), json=data, timeout=timeout)
            try:
                result = result_ori.json()
            except Exception:
                result = json.loads(result_ori.text)
            Log.debug('HTTPRequestUtil do_post result is {}'.format(result))
            return result
        except Exception as err:
            Log.exception('HTTPRequestUtil do_post err:[' + str(err) + ']')
        return None

    def do_delete(self, url, timeout=30):
        try:
            result = requests.delete('{}{}'.format(self._BASE_URL, url), timeout=timeout).json()
            Log.info('HTTPRequestUtil do_delete result is {}'.format(result))
            return result
        except Exception as err:
            Log.exception('HTTPRequestUtil do_delete err:[' + str(err) + ']')
        return None

    def do_put(self, url, data=None, timeout=30):
        try:
            result = requests.put('{}{}'.format(self._BASE_URL, url), json=data, timeout=timeout).json()
            Log.info('HTTPRequestUtil do_put result is {}'.format(result))
            return result
        except Exception as err:
            Log.exception('HTTPRequestUtil do_put err:[' + str(err) + ']')
        return None
