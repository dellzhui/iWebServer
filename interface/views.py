import json
import logging
from functools import wraps
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from rest_framework_simplejwt.tokens import RefreshToken
from interface.datatype.config import iWebServerBaseConfig
from interface.datatype.datatype import IoTErrorResponse, AuthResponseInfo, IoTSuccessResponse
from interface.models import RequestRecordInfo
from interface.utils.UserControlUtils import UserUtils

Log = logging.getLogger(__name__)


def iwebserver_logger(func):
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
        return IoTErrorResponse.GenResponse(error_msg='only admin can access')
    return decorated


@require_POST
def access_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        username = request_data['username']
        password = request_data['password']

        Log.info('request username is {}'.format(username))

        user_util = UserUtils(username, password)
        if(user_util.auto_login(request)):
            refresh = RefreshToken.for_user(user_util.get_user())
            return AuthResponseInfo(access=str(refresh.access_token), refresh=str(refresh)).GenResponse()
    except Exception as err:
        Log.exception('access_token post err:[' + str(err) + ']')
    return IoTErrorResponse.GenResponse(error_msg='internal error')

@require_POST
def refresh_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        Log.info('got request info is {}'.format(request_data))
        return IoTSuccessResponse().GenResponse(data={'access': str(RefreshToken(token=request_data['refresh']).access_token)})
    except Exception as err:
        Log.exception('refresh_token post err:[' + str(err) + ']')
        return IoTErrorResponse.GenResponse(error_msg='internal error')

def dashboard(request):
    return redirect('forbidden')

def forbidden(request):
    return render(request, 'forbidden.html', {})