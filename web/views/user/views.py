import logging
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView

from interface.datatype.config import iWebServerBaseConfig
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.views import requires_admin_access, iwebserver_logger

Log = logging.getLogger(__name__)


class iWebServerUserView(GenericAPIView):
    @iwebserver_logger
    @requires_admin_access
    def get(self, request):
        try:
            users = User.objects.filter(is_staff=False).exclude(username='AnonymousUser')
            if('username' in request.query_params):
                users = users.filter(username=request.query_params['username'])
            if ('email' in request.query_params):
                users = users.filter(email=request.query_params['email'])
            return IoTSuccessResponse().GenResponse(data=[{'username': item.username, 'email': item.email, 'userId': item.id, 'isAdmin': item.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))} for item in users])
        except Exception as err:
            Log.exception('iWebServerUserView get err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_msg='internal error')

    # @ha_logger
    # @requires_wechat_auth
    # def post(self, request, wechat_user_info=None):
    #     try:
    #         qr = request.data.get('qr')
    #         sharedCode = request.data.get('sharedCode')
    #         bindding_util = BinddingUtil(wechat_user_info)
    #         if(qr != None):
    #             return bindding_util.bindFromQRCode(qr)
    #         if(sharedCode != None):
    #             return bindding_util.bindFromSharedCode(sharedCode)
    #         return IoTErrorResponse.GenResponse(error_msg='no qr or sharedCode found')
    #     except Exception as err:
    #         Log.exception('KonkeCCUView post err:[' + str(err) + ']')
    #     return IoTErrorResponse.GenResponse(error_msg='internal error')
    #
    # @ha_logger
    # @requires_wechat_auth
    # def delete(self, request, wechat_user_info=None):
    #     try:
    #         return BinddingUtil(wechat_user_info).unind(request.data.get('ccuId'))
    #     except Exception as err:
    #         Log.exception('KonkeCCUView delete err:[' + str(err) + ']')
    #     return IoTErrorResponse.GenResponse(error_msg='internal error')