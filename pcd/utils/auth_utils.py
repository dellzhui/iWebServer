import json

from django.contrib.auth.models import User

from interface.utils.http_util import HTTPRequestUtil
from interface.utils.log_utils import loggerr
from pcd.config import iWebServerConfig

Log = loggerr(__name__).getLogger()


class AuthRequestUtil(HTTPRequestUtil):
    def __init__(self, base_url=iWebServerConfig.IWEBSERVER_AUTH_BASE_URL):
        super().__init__(base_url=base_url)

    def __is_successful_response(self, result):
        try:
            return result['authenticated'] == True and result['currentUser']['email'] != None and result['currentUser']['email'] != ''
        except Exception:
            return False

    def get_user(self, jsessionId: str, host: str):
        try:
            # https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#haYXk8pb7sMGR5Hjmk3NAX
            result = self.do_get(url='/sys/login/status/{}/{}'.format(jsessionId, host))

            '''
            {
                "jsessionid": "f45cde6c-49ba-44b9-8b50-8e1bc886f968",
                "currentUser": {
                    "username": "ygtest003",
                    "nickname": "测试员工3",
                    "phone": "18612345678",
                    "telephone": "",
                    "email": "ygtest003@chinaunicom.cn",
                    "info": null,
                    "birthday": null,
                    "sex": 0
                },
                "timeout": 18000000,
                "authenticated": true
            }
            '''
            if (result == None or not self.__is_successful_response(result)):
                return None
            Log.info('got result is {}'.format(json.dumps(result)))
            return User.objects.filter(username=result['currentUser']['username'], email=result['currentUser']['email']).last()
        except Exception as err:
            Log.exception('get_user err:[' + str(err) + ']')
        return None
