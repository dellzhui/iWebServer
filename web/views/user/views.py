import logging
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView

from interface.datatype.config import iWebServerBaseConfig
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.utils.UserControlUtils import UserUtils
from interface.utils.tools import ParasUtil
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
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    @requires_admin_access
    def post(self, request):
        try:
            if(ParasUtil.is_missing_paras(request.data, ['email', 'username', 'password', 'confrimPassword'])):
                return IoTErrorResponse.GenParasErrorResponse()

            if(request.data['password'] == '' or request.data['password'] != request.data['confrimPassword']):
                Log.error('password not match')
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_PASSWORD_NOT_MATCH, error_msg='password not match')

            user = User.objects.filter(is_staff=False).exclude(username='AnonymousUser').filter(username=request.data['username']).last()
            if(user != None):
                Log.error('user {} already presenced'.format(request.data['username']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_USERNAME_ALREADY_PRESENCED, error_msg='username {} already presenced'.format(request.data['username']))

            user = User.objects.filter(is_staff=False).exclude(username='AnonymousUser').filter(email=request.data['email']).last()
            if (user != None):
                Log.error('email {} already presenced'.format(request.data['email']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_EMAIL_ALREADY_PRESENCED, error_msg='username {} already presenced'.format(request.data['email']))

            User.objects.create_user(username=request.data['username'], password=request.data['password'], email=request.data['email'])
            return IoTSuccessResponse().GenResponse()
        except Exception as err:
            Log.exception('iWebServerUserView post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    @requires_admin_access
    def put(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['userId'])):
                return IoTErrorResponse.GenParasErrorResponse(error_msg='missing userId')
            if (ParasUtil.is_missing_paras(request.data, ['password', 'confrimPassword'])):
                return IoTErrorResponse.GenParasErrorResponse()

            if (request.data['password'] == '' or request.data['password'] != request.data['confrimPassword']):
                Log.error('password not match')
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_PASSWORD_NOT_MATCH, error_msg='password not match')

            user = User.objects.filter(is_staff=False).exclude(username='AnonymousUser').filter(id=request.query_params['userId']).last()
            if (user == None):
                Log.error('user {} not presenced'.format(request.query_params['userId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_USER_NOT_PRESENCED, error_msg='user not presenced')

            if(user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
                Log.error('can not change admin user')
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_CHANGING_ADMIN_USER, error_msg='can not remove admin user')

            user.set_password(request.data['password'])
            user.save()
            return IoTSuccessResponse().GenResponse()
        except Exception as err:
            Log.exception('iWebServerUserView put err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

    @iwebserver_logger
    @requires_admin_access
    def delete(self, request):
        try:
            if (ParasUtil.is_missing_paras(request.query_params, ['userId'])):
                return IoTErrorResponse.GenParasErrorResponse()

            user = User.objects.filter(is_staff=False).exclude(username='AnonymousUser').filter(id=request.query_params['userId']).last()
            if (user == None):
                Log.error('user {} not presenced'.format(request.query_params['userId']))
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_USER_NOT_PRESENCED, error_msg='user not presenced')

            if (user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
                Log.error('can not change admin user')
                return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_CHANGING_ADMIN_USER, error_msg='can not remove admin user')

            # TODO: clear all
            user.workstations.clear()
            user.rooms.clear()
            user.delete()
            return IoTSuccessResponse().GenResponse()
        except Exception as err:
            Log.exception('iWebServerUserView put err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()
