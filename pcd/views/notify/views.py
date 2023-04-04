import json
from interface.utils.log_utils import loggerr
from django.views.decorators.http import require_POST
from interface.datatype.datatype import IoTErrorResponse, IoTSuccessResponse
from interface.utils.tools import ParasUtil
from interface.views import iwebserver_logger_f
from pcd.utils.notify_handlers import NotifyHandler

Log = loggerr(__name__).getLogger()


@require_POST
@iwebserver_logger_f
def notify_webrtc(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))

        if (ParasUtil.is_missing_paras(request_data, ['type', 'data'])):
            return IoTErrorResponse.GenParasErrorResponse()

        type = request_data['type']
        data = request_data['data']

        notify_handler = NotifyHandler()
        if(notify_handler.notify(type, data)):
            return IoTSuccessResponse().GenResponse()
        Log.error('notify error, type:{}, data:{}'.format(type, data))
        return IoTErrorResponse.GenResponse('notify error')
    except Exception as err:
        Log.exception('notify webrtc event err:[' + str(err) + ']')
    return IoTErrorResponse.GenResponse()
