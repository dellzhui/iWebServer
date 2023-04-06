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
        '''
        {
            "type": "mqtt",
            "data": {
                "topic": "xxx",
                "payload": {
                    "RequestId": "KlDLdSudRpTV",
                    "RmsResult": {
                        "code": 0,
                        "extras": {
                            "publisherType": "webrtc",
                            "webrtc": {
                                "GroupId": "0000000001_0242ac110001",
                                "UserId": "0000000001",
                                "local_mac": "20:a1:da:23:11:39",
                                "privateId": 1184013529,
                                "publisherId": 8979568362539330,
                                "roomId": 2013,
                                "roomJoinPin": "K8FtAOikRVuSLd2f",
                                "stb_mac": "00:00:00:00:00:00"
                            }
                        },
                        "msg": "OK"
                    }
                }
            }
        }
        '''
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
