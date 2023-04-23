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
            return result['authenticated'] == True and result['currentUser']['info']['email'] != None and result['currentUser']['info']['email'] != ''
        except Exception:
            return False

    def get_user(self, jsessionId: str):
        try:
            # https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#haYXk8pb7sMGR5Hjmk3NAX
            result = self.do_post(url='/sys/login/status/{}/{}'.format(jsessionId, iWebServerConfig.IWEBSERVER_AUTH_LOCAL_HOST))

            '''
            {
                "jsessionid": "48a39a23-58c0-4cb1-b8cc-10d2ce52a301",
                "currentUser": {
                    "username": "zhangs12",
                    "nickname": "张三",
                    "phone": "",
                    "telephone": "",
                    "email": "",
                    "birthday": null,
                    "sex": 1,
                    "info": {
                        "code": "0980870",
                        "name": "张三",
                        "mobile": "18510369819",
                        "userName": "zhangs12",
                        "email": "zhangs12@chinaunicom.cn",
                        "gender": "M",
                        "birthday": "1992/3/13",
                        "post": "",
                        "dptName": "智能技术研究部-科研环境",
                        "dptCode": "830247140",
                        "type": "1"
                    }
                },
                "timeout": 1800000,
                "authenticated": true
            }
            '''
            if (result == None or not self.__is_successful_response(result)):
                return None
            Log.info('got result is {}'.format(json.dumps(result)))
            return User.objects.filter(username=result['currentUser']['info']['userName'], email=result['currentUser']['info']['email']).last()
        except Exception as err:
            Log.exception('get_user err:[' + str(err) + ']')
        return None
