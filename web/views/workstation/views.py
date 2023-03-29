import json
import logging
from rest_framework.generics import GenericAPIView
from interface.views import requires_wechat_auth, ha_logger

Log = logging.getLogger(__name__)


class KonkeCCUView(GenericAPIView):
    @requires_wechat_auth
    def get(self, request, wechat_user_info=None):
        try:
            return IoTSuccessResponse().GenResponse(data=BinddingUtil(wechat_user_info).getCCUList())
        except Exception as err:
            Log.exception('KonkeCCUView get err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_msg='internal error')

    @ha_logger
    @requires_wechat_auth
    def post(self, request, wechat_user_info=None):
        try:
            qr = request.data.get('qr')
            sharedCode = request.data.get('sharedCode')
            bindding_util = BinddingUtil(wechat_user_info)
            if(qr != None):
                return bindding_util.bindFromQRCode(qr)
            if(sharedCode != None):
                return bindding_util.bindFromSharedCode(sharedCode)
            return IoTErrorResponse.GenResponse(error_msg='no qr or sharedCode found')
        except Exception as err:
            Log.exception('KonkeCCUView post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_msg='internal error')

    @ha_logger
    @requires_wechat_auth
    def delete(self, request, wechat_user_info=None):
        try:
            return BinddingUtil(wechat_user_info).unind(request.data.get('ccuId'))
        except Exception as err:
            Log.exception('KonkeCCUView delete err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_msg='internal error')