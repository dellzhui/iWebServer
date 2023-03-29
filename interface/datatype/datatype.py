import json
import logging
import time
from json import JSONEncoder

from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

from interface.utils.log_utils import loggerr

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

    def GenResponse(self, data=None):
        result = {'success': True, 'data': data if (data != None) else self.to_dict()}
        Log.info('IoTSuccessResponse gen success response is {}'.format(result))
        return JsonResponse(data=result, status=HTTP_200_OK)


class IoTErrorResponse(JsonDatatypeBase):
    def __init__(self, error_code=-1, error_msg=None):
        JsonDatatypeBase.__init__(self)
        self.success = False
        self.error_code = error_code
        self.error_msg = error_msg

    @staticmethod
    def GenResponse(error_code=-1, error_msg=None):
        result = IoTErrorResponse(error_code=error_code, error_msg=error_msg).to_dict()
        Log.info('IoTErrorResponse gen error response is {}'.format(result))
        return JsonResponse(data=result, status=HTTP_500_INTERNAL_SERVER_ERROR)


class AuthResponseInfo(IoTSuccessResponse):
    def __init__(self, access=None, refresh=None):
        self.access = access
        self.refresh = refresh
        IoTSuccessResponse.__init__(self)