import json
import time
from json import JSONEncoder

from interface.utils.log_utils import loggerr

Log = loggerr(__name__).getLogger()


class IdmsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class JsonDatatypeBase:
    def to_json(self):
        try:
            return json.dumps(self, cls=IdmsEncoder)
        except Exception:
            return None

    def to_dict(self):
        try:
            return json.loads(json.dumps(self, cls=IdmsEncoder))
        except Exception:
            return None


class IoTBase(JsonDatatypeBase):
    def __init__(self, info=None):
        JsonDatatypeBase.__init__(self)
        if(isinstance(info, str)):
            self.__init__(info=json.loads(info))
            return
        if(isinstance(info, dict)):
            for key, value in info.items():
                if isinstance(value, (list, tuple)):
                   setattr(self, key, [IoTBase(x) if isinstance(x, dict) else x for x in value])
                else:
                   setattr(self, key, IoTBase(value) if isinstance(value, dict) else value)


class RequestRecord(JsonDatatypeBase):
    def __init__(self, request=None, response=None, wechat_user_info=None):
        self.RequestUrl = None
        self.RequestMethod = None
        self.RequestData = None
        self.RequestTimestampMS = int(round(time.time()*1000))
        self.ResponseCode = None
        self.ResponseContent = None
        self.WeChatId = None
        self.WeChatNickName = None

        if(request != None):
            self.RequestUrl = '{}{}'.format(request.META["PATH_INFO"], f'?{request.META["QUERY_STRING"]}' if (request.META["QUERY_STRING"] != '') else '')
            self.RequestMethod = request.method
            self.RequestData = json.dumps(request.data) if(isinstance(request.data, dict)) else str(request.data)

        if(response != None):
            self.ResponseCode = response.status_code
            self.ResponseContent = response.content.decode('utf-8') if(isinstance(response.content, bytes)) else str(response.content)

        if(wechat_user_info != None):
            self.WeChatId = wechat_user_info.openid
            self.WeChatNickName = wechat_user_info.nickName