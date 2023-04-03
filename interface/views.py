import json
import logging
from functools import wraps

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from interface.config import iWebServerBaseConfig
from interface.datatype.datatype import IoTErrorResponse, AuthResponseInfo, IoTSuccessResponse
from interface.models import RequestRecordInfo
from interface.utils.UserControlUtils import UserUtils
from interface.utils.tools import ParasUtil

Log = logging.getLogger(__name__)

def iwebserver_logger_f(func):
    @wraps(func)
    def wrapped_function(request):
        response = func(request)
        if(iWebServerBaseConfig.IWEBSERVER_REQUEST_RECORD_ENABLE):
            request_record = RequestRecordInfo()
            request_record.from_request_and_response(request=request, response=response)
            Log.debug(request_record.to_json())
            request_record.save()
        return response
    return wrapped_function


def iwebserver_logger_c(func):
    @wraps(func)
    def wrapped_function(o, request):
        response = func(o, request)
        if(iWebServerBaseConfig.IWEBSERVER_REQUEST_RECORD_ENABLE):
            request_record = RequestRecordInfo()
            request_record.from_request_and_response(request=request, response=response)
            Log.debug(request_record.to_json())
            request_record.save()
        return response
    return wrapped_function

def requires_admin_access(func):
    @wraps(func)
    def decorated(o, request):
        if(request.user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
            return func(o, request)
        user = User.objects.filter(pk=request.user.pk).last()
        if(user != None and user.has_perm('interface.{}'.format(iWebServerBaseConfig.IWEBSERVER_PERMISSION_ADMIN_ACCESS))):
            return func(o, request)
        return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_NO_ADMIN_PERMISSION, error_msg='only admin can access')
    return decorated


@require_POST
def access_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))

        if(ParasUtil.is_missing_paras(request_data, ['username', 'password'])):
            return IoTErrorResponse.GenParasErrorResponse()

        username = request_data['username']
        password = request_data['password']

        Log.info('request username is {}'.format(username))

        if(User.objects.filter(username=username).last() == None):
            Log.error('user {} not presenced'.format(username))
            return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_USER_NOT_PRESENCED, error_msg='user not presenced')

        user_util = UserUtils(username, password)
        if(user_util.auto_login(request)):
            refresh = RefreshToken.for_user(user_util.get_user())
            return AuthResponseInfo(access=str(refresh.access_token), refresh=str(refresh)).GenResponse()
        return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_INVALID_PASSWORD, error_msg='invalid password')
    except Exception as err:
        Log.exception('access_token post err:[' + str(err) + ']')
    return IoTErrorResponse.GenResponse()

@require_POST
def refresh_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        Log.info('got request info is {}'.format(request_data))
        if ('refresh' not in request_data):
            return IoTErrorResponse.GenParasErrorResponse()
        return IoTSuccessResponse().GenResponse(data={'access': str(RefreshToken(token=request_data['refresh']).access_token)})
    except TokenError as err:
        Log.exception('refresh_token TokenError err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_INVALID_REFRESH_TOKEN, error_msg='invalid refresh token')
    except Exception as err:
        Log.exception('refresh_token post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse()

def dashboard(request):
    return redirect('forbidden')

def forbidden(request):
    return render(request, 'forbidden.html', {})