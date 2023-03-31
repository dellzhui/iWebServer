import json
import logging
from json import JSONEncoder

from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from interface.config import iWebServerBaseConfig

# Log = loggerr(__name__).getLogger()
Log = logging.getLogger(__name__)


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


class IoTSuccessResponse(JsonDatatypeBase):
    def __init__(self):
        JsonDatatypeBase.__init__(self)

    def GenJson(self, data=None, requestId=None):
        result = {'success': True, 'data': data if (data != None) else self.to_dict()}
        if(requestId != None):
            result['requestId'] = requestId
        Log.info('GenJson gen success response is {}'.format(result))
        return result

    def GenResponse(self, data=None, requestId=None):
        return JsonResponse(data=self.GenJson(data=data, requestId=requestId), status=HTTP_200_OK)


class IoTErrorResponse(JsonDatatypeBase):
    def __init__(self, error_code=-1, error_msg=None):
        JsonDatatypeBase.__init__(self)
        self.success = False
        self.errorCode = error_code
        self.errorMsg = error_msg

    @staticmethod
    def GenJson(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_SERVER_INTERNAL_ERROR, error_msg='server internal error', requestId=None):
        result = IoTErrorResponse(error_code=error_code, error_msg=error_msg).to_dict()
        if(requestId != None):
            result['requestId'] = requestId
        Log.info('GenJson gen error response is {}'.format(result))
        return result

    @staticmethod
    def GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_SERVER_INTERNAL_ERROR, error_msg='server internal error', requestId=None):
        return JsonResponse(data=IoTErrorResponse.GenJson(error_code=error_code, error_msg=error_msg, requestId=requestId), status=HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def GenParasErrorResponse(error_msg='invalid paras', requestId=None):
        return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_INVALID_PARAS, error_msg=error_msg, requestId=requestId)


class AuthResponseInfo(IoTSuccessResponse):
    def __init__(self, access=None, refresh=None):
        self.access = access
        self.refresh = refresh
        IoTSuccessResponse.__init__(self)