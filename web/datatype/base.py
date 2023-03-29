import logging
from django.http import JsonResponse
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK
from interface.datatype.datatype import JsonDatatypeBase

Log = logging.getLogger(__name__)


class IoTSuccessResponse(JsonDatatypeBase):
    def __init__(self):
        JsonDatatypeBase.__init__(self)
    
    def GenResponse(self, data=None):
        result = {'success': True, 'data': data if(data != None) else self.to_dict()}
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
