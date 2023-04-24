import json

from rest_framework_simplejwt.tokens import RefreshToken

from interface.config import iWebServerBaseConfig
from interface.utils.UserControlUtils import UserUtils
from interface.utils.log_utils import loggerr
from django.views.decorators.http import require_POST
from interface.datatype.datatype import IoTErrorResponse, AuthResponseInfo
from interface.views import iwebserver_logger_f
from pcd.utils.auth_utils import AuthRequestUtil

Log = loggerr(__name__).getLogger()


@require_POST
@iwebserver_logger_f
def refresh_token(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        Log.info('got request info is {}'.format(request_data))
        if ('jsessionId' not in request_data):
            return IoTErrorResponse.GenParasErrorResponse()

        # https://www.wolai.com/yang_ids/e5UPobHGfhX85QEiW4fkQa#haYXk8pb7sMGR5Hjmk3NAX
        jsessionId = request_data['jsessionId']
        host = request.META['HTTP_HOST'].split(':')[0]
        user = AuthRequestUtil().get_user(jsessionId=jsessionId, host=host)
        if(user == None):
            return IoTErrorResponse.GenResponse(error_code=iWebServerBaseConfig.IWEBSERVER_ERROR_CODE_USER_NOT_PRESENCED, error_msg='user not presenced')
        refresh = RefreshToken.for_user(user)
        return AuthResponseInfo(access=str(refresh.access_token), refresh=str(refresh), isAdmin=UserUtils.is_admin(user), userName=user.username).GenResponse()
    except Exception as err:
        Log.exception('refresh_token post err:[' + str(err) + ']')
    return IoTErrorResponse.GenResponse()
